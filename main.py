import sys
from login import *

if __name__ == "__main__":

    adresse = '14-15/4' if len(sys.argv) == 1 else sys.argv[1]

    guide = Login()
    guide.goto(adresse)
    guide.interact()
