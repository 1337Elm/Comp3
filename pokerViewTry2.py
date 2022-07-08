from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtSvgWidgets import *
import os
from pokermodel import *

class Background(QGraphicsScene):
    def __init__(self):
        super().__init__()

        path = os.path.abspath(os.getcwd())
        self.background = QPixmap(path + '/Comp3/cards/table.png')
        self.setBackgroundBrush(QBrush(self.background))

class Window(QGraphicsView):
    signal = pyqtSignal()

    def __init__(self,player,game):
        self.scene = Background()
        super().__init__(self.scene)
        self.player = player
        self.game = game
        
        self.UiInit()
        self.Buttons()
        self.showCards()

    def UiInit(self):
        self.setWindowTitle("1v1 Texas Hold 'em")
        self.setGeometry(100,100,1500,1000)

        self.show()
    
    def Buttons(self):
        self.vbox = QVBoxLayout()
        self.vbox.addStretch(2)
        
        check = QPushButton("Check",self)
        check.setFixedWidth(100)
        check.clicked.connect(self.player.check)

        fold = QPushButton("Fold",self)
        fold.setFixedWidth(100)
        fold.clicked.connect(self.player.fold)
        
        bet = QPushButton("Bet",self)
        bet.setFixedWidth(100)

        betLine = QLineEdit(self)
        betLine.setFixedWidth(100)
        
        allIn = QPushButton("All in",self)
        allIn.setFixedWidth(100)
        allIn.clicked.connect(lambda: self.game.Allin(self.player))

        self.vbox.addWidget(check)
        self.vbox.addWidget(fold)
        self.vbox.addWidget(bet)
        self.vbox.addWidget(betLine)
        self.vbox.addWidget(allIn)


        self.setLayout(self.vbox)
    
    def showCards(self):
        path = os.path.abspath(os.getcwd())
        file = os.path.join(path + '/Comp3/cards/Red_Back_2.svg')

        item = QGraphicsSvgItem(file)
        self.scene.addItem(item)
        item.setPos(1200,0)

        cards = read_cards()
        self.scene.addItem(cards[2,0])
        card = cards[14,3]
        self.scene.addItem(card)
        card.setPos(750,500)


    def cardsInHand(self):
        pass


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    for suit_file, suit in zip('HDSC', range(4)):  # Check the order of the suits here!!!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit_file
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QGraphicsSvgItem('/Users/benjaminjonsson/Programmering/Comp3/cards/' + file + '.svg')
    return all_cards