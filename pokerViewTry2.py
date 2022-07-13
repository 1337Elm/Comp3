from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtSvgWidgets import *
import os
from pokermodel import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.left = 500
        self.top = 200
        self.width = 500
        self.height = 500
        
        self.CreateGraphicView()
        self.buttons()

        self.setWindowTitle("1v1 Texas Hold 'em")
        self.setGeometry(self.left,self.top,self.width,self.height)

        self.show
    
    def buttons(self):
        self.box = QGridLayout()
        self.label1 = QLabel("Player 1 name")
        self.label2 = QLabel("Player 2 name")

        self.name1 = QLineEdit(self)
        self.name2 = QLineEdit(self)

        self.submit = QPushButton("Submit names")
        self.submit.clicked.connect(self.initGames)

        self.box.addWidget(self.label1,0,0)
        self.box.addWidget(self.label2,0,1)
        self.box.addWidget(self.name1,1,0)
        self.box.addWidget(self.name2,1,1)
        self.box.addWidget(self.submit,2,2)
    
    def initGames(self):
        player1 = Player(self.name1.text())
        player2 = Player(self.name2.text())
        game = Game(player1,player2)
        self.close()
        Window(player1,player2,game)
    
    def CreateGraphicView(self):
        path2background = os.path.abspath(os.getcwd())
        backgroundFile = os.path.join(path2background + '/Comp3/cards/table.png')

        self.scene = QGraphicsScene()
        self.title = QPixmap(backgroundFile)
        self.scene.setBackgroundBrush(QBrush(self.title))
    
        graphicView = QGraphicsView(self.scene,self)
        graphicView.setGeometry(0,0,1000,1000)


class Background(QGraphicsScene):
    """The class responsible for the background of the window
    
    :param QGraphicsScene: The type of object
    :type QGraphicsScene: Object
    """
    def __init__(self):
        """Initializing of the background
        
        :param self: The QGraphicsScene object
        :type self: Objectrt5
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

    def __init__(self,player1,player2,game):
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
        self.player1 = player1
        self.player2 = player2
        self.game = game
        
        self.UiInit()
        self.Buttons()
        self.OpponentButton()

    def UiInit(self):
        """Initializes the window with tile and sizing
        
        :param self: The QGraphicsView
        :type self: object
        """
        self.setWindowTitle("1v1 Texas Hold 'em")
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
        check.clicked.connect(self.player1.check)

        fold = QPushButton("Fold",self)
        fold.setFixedWidth(100)
        fold.clicked.connect(self.player1.fold)
        fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
        fold.clicked.connect(self.resetBoard)
        
        betLine = QLineEdit(self)
        betLine.setFixedWidth(100)

        bet = QPushButton("Bet",self)
        bet.setFixedWidth(100)
        bet.clicked.connect(lambda: self.game.bet(self.player1,int(betLine.text())))
        
        allIn = QPushButton("All in",self)
        allIn.setFixedWidth(100)
        allIn.clicked.connect(lambda: self.game.Allin(self.player1))

        self.label1 = QLabel(f"{self.player1.name}'s money: {self.player1.Money}")
        self.label2 = QLabel(f"{self.player2.name}'s money: {self.player2.Money}")
        self.label3 = QLabel(f"Pot: {self.game.Pot}")
        bet.clicked.connect(self.updateMoney)

        self.vbox.addWidget(self.label3)
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(check)
        self.vbox.addWidget(fold)
        self.vbox.addWidget(bet)
        self.vbox.addWidget(betLine)
        self.vbox.addWidget(allIn)

        if self.player1.Role == "Dealer":
            Deal = QPushButton("Deal",self)
            Deal.setFixedWidth(100)
            Deal.clicked.connect(self.game.deal)
            Deal.clicked.connect(self.showHand)

            DealBoard = QPushButton("Deal, 2nd",self)
            DealBoard.setFixedWidth(100)
            DealBoard.clicked.connect(self.CardsOnBoard)
        
            DealFourth = QPushButton("Deal, 3rd",self)
            DealFourth.setFixedWidth(100)
            DealFourth.clicked.connect(self.FourthCard)

            DealRiver = QPushButton("Deal river",self)
            DealRiver.setFixedWidth(100)
            DealRiver.clicked.connect(self.River)
            DealRiver.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            DealRiver.clicked.connect(self.showWinner)

            self.vbox.addWidget(Deal)
            self.vbox.addWidget(DealBoard)
            self.vbox.addWidget(DealFourth)
            self.vbox.addWidget(DealRiver)

        self.setLayout(self.vbox)
    
    def OpponentButton(self):
        self.vboxOpp = QVBoxLayout()
        self.vboxOpp.addStretch(4)
        
        check = QPushButton("Check",self)
        check.setFixedWidth(100)
        check.clicked.connect(self.player2.check)

        fold = QPushButton("Fold",self)
        fold.setFixedWidth(100)
        fold.clicked.connect(self.player2.fold)
        fold.clicked.connect(lambda: self.game.roundOver(self.player1,self.player2))
        fold.clicked.connect(self.resetBoard)
        
        betLine = QLineEdit(self)
        betLine.setFixedWidth(100)

        bet = QPushButton("Bet",self)
        bet.setFixedWidth(100)
        bet.clicked.connect(lambda: self.game.bet(self.player2,int(betLine.text())))
        bet.clicked.connect(self.updateMoney)

        allIn = QPushButton("All in",self)
        allIn.setFixedWidth(100)
        allIn.clicked.connect(lambda: self.game.Allin(self.player2))

        self.vbox.addWidget(self.label3)
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(check)
        self.vbox.addWidget(fold)
        self.vbox.addWidget(bet)
        self.vbox.addWidget(betLine)
        self.vbox.addWidget(allIn)

        if self.player2.Role == "Dealer":
            Deal = QPushButton("Deal",self)
            Deal.setFixedWidth(100)
            Deal.clicked.connect(self.game.deal)
            Deal.clicked.connect(self.showHand)

            DealBoard = QPushButton("Deal, 2nd",self)
            DealBoard.setFixedWidth(100)
            DealBoard.clicked.connect(self.CardsOnBoard)
        
            DealFourth = QPushButton("Deal, 3rd",self)
            DealFourth.setFixedWidth(100)
            DealFourth.clicked.connect(self.FourthCard)

            DealRiver = QPushButton("Deal river",self)
            DealRiver.setFixedWidth(100)
            DealRiver.clicked.connect(self.River)
            DealRiver.clicked.connect(lambda: self.game.determineWinner(self.player2,self.player1))
            DealRiver.clicked.connect(self.showWinner)

            self.vbox.addWidget(Deal)
            self.vbox.addWidget(DealBoard)
            self.vbox.addWidget(DealFourth)
            self.vbox.addWidget(DealRiver)

        self.setLayout(self.vbox)
    
    def updateMoney(self):
        self.label1.setText(f"Money: {self.player1.Money}")
        self.label2.setText(f"Opponents Money: {self.player2.Money}")
        self.label3.setText(f"Pot: {self.game.Pot}")
    
    def resetBoard(self):
        self.updateMoney()
        self.flipCards()
        self.scene.clear()
    
    def showHand(self):
        cards = read_cards()
        list = []
        for i in range(len(self.player1.hand.cards)):
            renderer = cards[self.player1.hand.cards[i].get_value(),self.player1.hand.cards[i].suit.value]
            position =i
            d = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(d)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            d.setGraphicsEffect(shadow)
            d.setPos(i*250 + 1000, 500)
            self.scene.addItem(d)
            list.append(d)

            path = os.path.abspath(os.getcwd())
            oppRender = QSvgRenderer(path + '/Comp3/cards/Red_Back_2.svg')
            oppCard = cardsInHand(oppRender,position)
            shadow = QGraphicsDropShadowEffect(d)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            oppCard.setGraphicsEffect(shadow)
            oppCard.setPos(i*250 + 1000,-150)
            self.scene.addItem(oppCard)
        return list
    
    def CardsOnBoard(self):
        cardPic = read_cards()
        cards = self.game.BoardCards()

        for i in range(3):
            renderer = cardPic[cards[i].get_value(),cards[i].suit.value]
            position = i
            c = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5,5)
            shadow.setColor(QColor(0,0,0,180))
            c.setGraphicsEffect(shadow)
            c.setPos(900+i*250,175)
            self.scene.addItem(c)

    def FourthCard(self):
        cardPic = read_cards()
        cards = self.game.BoardCards()

        renderer = cardPic[cards[3].get_value(),cards[3].suit.value]
        position = 4
        c = cardsInHand(renderer,position)
        shadow = QGraphicsDropShadowEffect(c)
        shadow.setBlurRadius(10.)
        shadow.setOffset(5,5)
        shadow.setColor(QColor(0,0,0,180))
        c.setGraphicsEffect(shadow)
        c.setPos(1650,175)
        self.scene.addItem(c)
    
    def River(self):
        cardPic = read_cards()
        cards = self.game.BoardCards()

        renderer = cardPic[cards[4].get_value(),cards[4].suit.value]
        position = 5
        c = cardsInHand(renderer,position)
        shadow = QGraphicsDropShadowEffect(c)
        shadow.setBlurRadius(10.)
        shadow.setOffset(5,5)
        shadow.setColor(QColor(0,0,0,180))
        c.setGraphicsEffect(shadow)
        c.setPos(1900,175)
        self.scene.addItem(c)
        
    def flipCards(self):
        path = os.path.abspath(os.getcwd())
        file = os.path.join(path + '/Comp3/cards/Red_Back_2.svg')
        for i in range(len(self.player1.hand.cards)):
            renderer = QSvgRenderer(file)
            position = i
            c = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            c.setGraphicsEffect(shadow)
            c.setPos(i*250 + 1000, 500)
            self.scene.addItem(c)

    def showWinner(self):
        cardPic = read_cards()
        cards = self.player2.hand.cards
        
        for i,card in enumerate(cards):
            renderer = cardPic[card.get_value(),card.suit.value]
            position = i
            c = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5,5)
            shadow.setColor(QColor(0,0,0,180))
            c.setGraphicsEffect(shadow)
            c.setPos(1000 + i*250,-150)
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