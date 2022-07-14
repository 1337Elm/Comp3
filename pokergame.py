from pokermodel import *
from pokerViewTry2 import *
import sys

def main():
    app = QApplication(sys.argv)
    #back = MainWindow()
    player1 = Player("Benjamin")
    player2 = Player("Karl")
    game = Game(player1,player2)
    back = Window(player1,player2,game)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()