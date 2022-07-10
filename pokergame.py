from pokermodel import *
from pokerViewTry2 import *
import sys

def main():
    player1 = Player("Benjamin")
    player2 = Player("Karl")
    game = Game(player1,player2)

    app = QApplication(sys.argv)
    back = Window(player1,game)
    back2 = Window(player2,game)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()