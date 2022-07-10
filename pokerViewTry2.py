from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtSvgWidgets import *
import os
from pokermodel import *

class Background(QGraphicsScene):
    """The class responsible for the background of the window
    
    :param QGraphicsScene: The type of object
    :type QGraphicsScene: Object
    """
    def __init__(self):
        """Initializing of the background
        
        :param self: The QGraphicsScene object
        :type self: Object
        """
        super().__init__()

        path = os.path.abspath(os.getcwd())
        self.background = QPixmap(path + '/Comp3/cards/table.png')
        self.setBackgroundBrush(QBrush(self.background))

class Window(QGraphicsView):
    """The class for the window of the game
    :param QGraphicsView: The type of window
    :type QGraphicsview: Object
    """
    signal = pyqtSignal()

    def __init__(self,player,game):
        """Initializing the window with the table background, aswell as calling the other functions
        
        :param self: The QGraphicsView
        :type self: Object
        
        :param player: The player the instance is created for
        :type playaer: Object
        
        :param game: The game instance the GUI is created for
        :type game: Object
        """
        self.scene = Background()
        super().__init__(self.scene)
        self.player = player
        self.game = game
        
        self.UiInit()
        self.Buttons()

    def UiInit(self):
        """Initializes the window with tile and sizing
        
        :param self: The QGraphicsView
        :type self: object
        """
        self.setWindowTitle(f"1v1 Texas Hold 'em, {self.player.name}")
        self.setGeometry(100,100,1500,1000)

        self.show()
    
    def Buttons(self):
        """Creates all buttons needed for a game of poker
        
        :param self: The QGraphicsView
        :type self: object
        """
        self.vbox = QVBoxLayout()
        self.vbox.addStretch(2)
        
        check = QPushButton("Check",self)
        check.setFixedWidth(100)
        check.clicked.connect(self.player.check)

        fold = QPushButton("Fold",self)
        fold.setFixedWidth(100)
        fold.clicked.connect(self.player.fold)
        
        betLine = QLineEdit(self)
        betLine.setFixedWidth(100)

        bet = QPushButton("Bet",self)
        bet.setFixedWidth(100)
        bet.clicked.connect(lambda: self.game.bet(self.player,int(betLine.text())))
        
        allIn = QPushButton("All in",self)
        allIn.setFixedWidth(100)
        allIn.clicked.connect(lambda: self.game.Allin(self.player))

        self.vbox.addWidget(check)
        self.vbox.addWidget(fold)
        self.vbox.addWidget(bet)
        self.vbox.addWidget(betLine)
        self.vbox.addWidget(allIn)

        if self.player.Role == "Dealer":
            Deal = QPushButton("Deal",self)
            Deal.setFixedWidth(100)
            Deal.clicked.connect(self.game.deal)
            Deal.clicked.connect(self.showHand)
            Deal.clicked.connect(self.game.round)
            Deal.clicked.connect(self.CardsOnBoard)
            self.vbox.addWidget(Deal)

        self.setLayout(self.vbox)
    
    def showHand(self):
        cards = read_cards()
        for i in range(len(self.player.hand.cards)):
            renderer = cards[self.player.hand.cards[i].get_value(),self.player.hand.cards[i].suit.value]
            position =i
            c = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            c.setGraphicsEffect(shadow)
            c.setPos(i*250 + 1000, 500)
            self.scene.addItem(c)

            path = os.path.abspath(os.getcwd())
            oppRender = QSvgRenderer(path + '/Comp3/cards/Red_Back_2.svg')
            oppCard = cardsInHand(oppRender,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            oppCard.setGraphicsEffect(shadow)
            oppCard.setPos(i*250 + 1000,-150)
            self.scene.addItem(oppCard)
    
    def CardsOnBoard(self):
        cardPic = read_cards()
        cards = self.game.BoardCards()

        for i in range(len(cards)):
            renderer = cardPic[cards[i].get_value(),cards[i].suit.value]
            position = i
            c = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5,5)
            shadow.setColor(QColor(0,0,0,180))
            c.setGraphicsEffect(shadow)
            c.setPos(600+i*250,175)
            self.scene.addItem(c)


class  cardsInHand(QGraphicsSvgItem):
    def __init__(self,renderer,position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()
    for suit_file, suit in zip('HDSC', range(4)):
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit_file
            key = (value, suit)
            path = os.path.abspath(os.getcwd())
            all_cards[key] = QSvgRenderer(path + '/Comp3/cards/' + file + '.svg')
    return all_cards