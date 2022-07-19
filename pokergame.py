from pokermodel import *
from pokerview import *
import sys

def main():
    """Runs the main program and initializes the GUI which in turns 
        initializes the logic and library for the game
    """
    app = QApplication(sys.argv)
    back = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    """Determines that this file is the runnable file
    """
    main()