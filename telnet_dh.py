import atexit
import sys
import os
from threading import Thread
import shutil
import struct
import tty
import termios
import signal
import zlib
import platform
from netstring_dh import NetstringWrapperProtocol

try:
    from twisted.internet.protocol import Protocol, ClientFactory
    from twisted.internet import reactor, defer
    from twisted.internet.error import ConnectionDone
    from twisted.conch.telnet import TelnetProtocol, TelnetTransport, IAC, IP, LINEMODE_EOF, ECHO, SGA, MODE, LINEMODE, \
        NAWS, TRAPSIG, LINEMODE_SLC
except ImportError:
    print("Ce client python dépend du module ``twisted''. Pour l'installer, faites :")
    print("        python3 -m pip install --user twisted")
    print("Puis ré-essayez de lancer ce programme.")
    sys.exit(1)

BINARY = bytes([0])
PLUGIN = b'U'
PLUGIN_DATA = bytes([0])
PLUGIN_CODE = bytes([1])
TTYPE = bytes([24])
TTYPE_IS = bytes([0])
TTYPE_SEND = bytes([1])


class TelnetClient(TelnetProtocol):
    def connectionMade(self):
        """
        This function is invoked once the connection to the telnet server
        is established.
        """
        # negociate telnet options
        self.transport.negotiationMap[LINEMODE] = self.telnet_LINEMODE
        self.transport.negotiationMap[PLUGIN] = self.telnet_PLUGIN
        self.transport.negotiationMap[TTYPE] = self.telnet_TTYPE
        try:
            self.dispatcher = Dispatcher(self.transport)
        except NameError:
            self.dispatcher = None
        self.transport.will(LINEMODE)
        self.transport.do(SGA)
        self.transport.will(NAWS)
        self.transport.will(TTYPE)
        self.NAWS()
        self._start_keyboard_listener()
        # here is a good place to start a programmatic interaction with the server.

    def dataReceived(self, data):
        """
        #Invoked when data arrives from the server. We just print it.
        """
        sys.stdout.buffer.write(data)
        sys.stdout.flush()

    def _start_keyboard_listener(self):
        """
        Start a thread that listen to the keyboard.
        The terminal is put in CBREAK mode (no line buffering).
        Keystrokes are sent to the telnet server.
        """

        def keyboard_listener(transport):
            # put terminal in CBREAK mode
            original_stty = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin, termios.TCSANOW)
            # restore normal mode when the client exits
            atexit.register(lambda: termios.tcsetattr(sys.stdin, termios.TCSANOW, original_stty))
            while True:
                try:
                    chars = os.read(sys.stdin.fileno(), 1000)
                    if chars == b'\x04':  # catch CTRL+D, send special telnet command
                        transport.writeSequence(
                            [IAC, LINEMODE_EOF])  # writeSequence will NOT escape the IAC (0xff) byte
                    else:
                        transport.write(chars)
                except OSError:
                    pass

        Thread(target=keyboard_listener, args=[self.transport], daemon=True).start()

    def _start_keyboard_listener(self):
        """
        Start a thread that listen to the keyboard.
        The terminal is put in CBREAK mode (no line buffering).
        Keystrokes are sent to the telnet server.
        """

        def keyboard_listener(transport):
            # put terminal in CBREAK mode
            original_stty = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin, termios.TCSANOW)
            # restore normal mode when the client exits
            atexit.register(lambda: termios.tcsetattr(sys.stdin, termios.TCSANOW, original_stty))
            while True:
                try:
                    chars = os.read(sys.stdin.fileno(), 1000)
                    if chars == b'\x04':  # catch CTRL+D, send special telnet command
                        transport.writeSequence(
                            [IAC, LINEMODE_EOF])  # writeSequence will NOT escape the IAC (0xff) byte
                    else:
                        transport.write(chars)
                except OSError:
                    pass

        Thread(target=keyboard_listener, args=[self.transport], daemon=True).start()

    # PAS UTILE
    def NAWS(self):
        """
        Send terminal size information to the server.
        """
        stuff = shutil.get_terminal_size()
        payload = struct.pack('!HH', stuff.columns, stuff.lines)
        self.transport.requestNegotiation(NAWS, payload)

    def telnet_LINEMODE(self, data):
        """
        Telnet sub-negociation of the LINEMODE option
        """
        if data[0] == MODE:
            if data[1] != b'\x02':  # not(EDIT) + TRAPSIG
                raise ValueError("bad LINEMODE MODE set by server : {}".format(data[1]))
            self.transport.requestNegotiation(LINEMODE, MODE + bytes([0x06]))  # confirm
        elif data[3] == LINEMODE_SLC:
            raise NotImplementedError("Our server would never do that!")

    def telnet_PLUGIN(self, data):
        """
        Telnet sub-negociation of the PLUGIN option
        """
        if len(data) == 0:
            return
        payload = b''.join(data[1:])
        if data[0] == PLUGIN_CODE:
            exec(zlib.decompress(payload))
        if data[0] == PLUGIN_DATA and self.dispatcher is not None:
            self.dispatcher.dataReceived(payload)

    def telnet_TTYPE(self, data):
        """
        Telnet sub-negociation of the TTYPE option
        """
        if data[0] == TTYPE_SEND:
            if platform.system() == 'Windows' and self._init_descriptor is not None:
                import curses
                ttype = curses.get_term(self._init_descriptor)
            else:
                ttype = os.environ.get('TERM', 'dumb')
            self.transport.requestNegotiation(TTYPE, TTYPE_IS + ttype.encode())  # respond

    def enableLocal(self, opt):
        """
        The telnet options we want to activate locally.
        """
        return opt in {SGA, NAWS, LINEMODE, PLUGIN, TTYPE, BINARY}

    def enableRemote(self, opt):
        """
        The telnet options we want the remote host to activate.
        """
        return opt in {ECHO, SGA, BINARY}


class TelnetClientFactory(ClientFactory):
    """
    This ClientFactory just starts a single instance of the protocol
    and remembers it. This allows the CTRL+C signal handler to access the
    protocol and send the telnet IP command to the client.
    """

    def doStart(self):
        self.protocol = None

    def buildProtocol(self, addr):
        self.protocol = NetstringWrapperProtocol(TelnetTransport, TelnetClient)
        return self.protocol

    def write(self, data, raw=False):
        if raw:
            self.protocol.writeSequence(data)
        else:
            self.protocol.write(data)

    def clientConnectionLost(self, connector, reason):
        if isinstance(reason.value, ConnectionDone):
            print('Connection closed by foreign host.')
        else:
            print('Connection lost.')
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason.value)
        reactor.stop()


######################### main code


factory = TelnetClientFactory()


def SIGINTHandler(signum, stackframe):
    """
    UNIX Signal handler. Invoked when the user hits CTRL+C.
    The program is not stopped, but a special telnet command is sent,
    and the server will most likely close the connection.
    """
    factory.write([IAC, IP], raw=True)


signal.signal(signal.SIGINT, SIGINTHandler)  # register signal handler

# connect to the server and run the reactor
reactor.connectTCP('crypta.sfpn.net', 6024, factory)
reactor.run()
