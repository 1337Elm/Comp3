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
        :type self: Objectrt5
        """
        super().__init__()

        path = os.path.abspath(os.getcwd())
        self.background = QPixmap(path + '/Comp3/cards/table.png')
        self.setBackgroundBrush(QBrush(self.background))


class MainWindow(QGraphicsView):
    """The class representing the log-in screen
    
    :param QGraphicsView: The type of object
    :type QGraphicsView: object
    """
    def __init__(self):
        """Initiating the window with a background and set size
        
        :param self: The class object
        :type self: object
        """
        self.scene = Background()
        super().__init__(self.scene)

        self.left = 500
        self.top = 200
        self.width = 300
        self.height = 200
        
        self.buttons()

        self.setWindowTitle("1v1 Texas Hold 'em")
        self.setGeometry(self.left,self.top,self.width,self.height)

        self.show()
    
    def buttons(self):
        """Creating the buttons in order to enter the names of the players
        
        :param self: The class object
        :type self: object
        """
        self.box = QVBoxLayout()
        self.label1 = QLabel("Player 1 name")
        self.label2 = QLabel("Player 2 name")

        self.name1 = QLineEdit(self)
        self.name2 = QLineEdit(self)

        self.submit = QPushButton("Submit names")
        self.submit.clicked.connect(self.initGames)

        self.box.addWidget(self.label1)
        self.box.addWidget(self.name1)

        self.box.addWidget(self.label2)
        self.box.addWidget(self.name2)
        self.box.addWidget(self.submit)
        
        self.setLayout(self.box)

    def initGames(self):
        """When names are entered the players are initialized aswell as the game
        
        :param self: The class object
        :type self: object
        """
        player1 = Player(self.name1.text())
        player2 = Player(self.name2.text())
        game = Game(player1,player2)
        Window(player1,player2,game)


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

        self.boardCards = self.game.BoardCards()

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
        if self.game.turns() == 0:
            if self.player1.Role == "Dealer":
                self.vbox = QVBoxLayout()
                self.vbox.addStretch(2)
                self.Deal1 = QPushButton("Deal",self)
                self.Deal1.setFixedWidth(100)
                self.Deal1.clicked.connect(self.game.deal)
                self.Deal1.clicked.connect(self.showHand)
                self.Deal1.clicked.connect(self.OpponentButton)


                self.label1 = QLabel(f"{self.player1.name}'s money: {self.player1.Money}")
                self.label2 = QLabel(f"{self.player2.name}'s money: {self.player2.Money}")
                self.label3 = QLabel(f"Pot: {self.game.Pot}")
                self.vbox.addWidget(self.label3)
                self.vbox.addWidget(self.label1)
                self.vbox.addWidget(self.label2)
                self.vbox.addWidget(self.Deal1)
                self.setLayout(self.vbox)
        
        elif self.game.turns() == 1:
            self.vbox.removeWidget(self.Deal1)
            self.BigBlindBet = QPushButton("Bet big blind",self)
            self.BigBlindBet.setFixedWidth(100)
            self.BigBlindBet.clicked.connect(lambda: self.game.bet(self.player1,20))
            self.BigBlindBet.clicked.connect(self.updateMoney)
        
        elif self.game.turns() == 2:
            self.vbox.removeWidget(self.BigBlindBet)
            self.BigBlindBet.deleteLater()

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player1,20))
            self.Call.clicked.connect(self.CardsOnBoard)
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.OpponentButton)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player1))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player1,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.CardsOnBoard)
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player1))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.CardsOnBoard)
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 3:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player1,20))
            self.Call.clicked.connect(self.CardsOnBoard)
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.OpponentButton)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player1))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player1,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player1))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 4:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()
    
            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player1))
            self.Check.clicked.connect(self.updateMoney)   
            self.Check.clicked.connect(self.FourthCard)
            self.Check.clicked.connect(self.OpponentButton) 

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player1,20))
            self.Call.clicked.connect(self.CardsOnBoard)
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.FourthCard)
            self.Call.clicked.connect(self.OpponentButton)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player1))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player1,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.FourthCard)
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player1))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.FourthCard)
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 5:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player1))
            self.Check.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.Check.clicked.connect(self.updateMoney)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player1))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player1,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player1))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 6:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player1))
            self.Check.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.Check.clicked.connect(self.updateMoney)
            self.Check.clicked.connect(self.River)
            self.Check.clicked.connect(self.showWinner)
            self.Check.clicked.connect(self.OpponentButton)

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player1,20))
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.River)
            self.Call.clicked.connect(self.OpponentButton)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player1))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player1,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.River)
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player1))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.River)
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 7:
            self.vbox.removeWidget(self.Call)
            self.Call.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player1,20))
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.OpponentButton)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player1))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player1,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player1))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 8:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player1))
            self.Check.clicked.connect(self.showWinner)
            self.Check.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.Check.clicked.connect(self.updateMoney)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player1))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player1,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.showWinner)
            self.bet.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player1))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
    
    def OpponentButton(self):
        if self.game.turns() == 0:
            if self.player2.Role == "Dealer":
                self.vbox = QVBoxLayout()
                self.vbox.addStretch(2)
                self.Deal1 = QPushButton("Deal",self)
                self.Deal1.setFixedWidth(100)
                self.Deal1.clicked.connect(self.game.deal)
                self.Deal1.clicked.connect(self.showHand)

        elif self.game.turns() == 1:
            self.vbox.removeWidget(self.Deal1)
            self.Deal1.deleteLater()

            self.BigBlindBet = QPushButton("Bet big blind",self)
            self.BigBlindBet.setFixedWidth(100)
            self.BigBlindBet.clicked.connect(lambda: self.game.bet(self.player2,20))
            self.BigBlindBet.clicked.connect(self.updateMoney)
            self.BigBlindBet.clicked.connect(self.Buttons)

            self.vbox.addWidget(self.BigBlindBet)
        
        elif self.game.turns() == 2:
            self.vbox.removeWidget(self.BigBlindBet)
            self.BigBlindBet.deleteLater()

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player2,20))
            self.Call.clicked.connect(self.CardsOnBoard)
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.Buttons)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player2))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player1,self.player2))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player2,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.CardsOnBoard)
            self.bet.clicked.connect(self.Buttons)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player2))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.CardsOnBoard)
            self.allIn.clicked.connect(self.Buttons)

            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 3:
            self.vbox.removeWidget(self.Call)
            self.Call.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()
    
            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player2))
            self.Check.clicked.connect(self.Buttons)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player2))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player1,self.player2))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player2,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.Buttons)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player2))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.Buttons)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)

        elif self.game.turns() == 4:
            self.vbox.removeWidget(self.Call)
            self.Call.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player2))
            self.Check.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.Check.clicked.connect(self.updateMoney)
            self.Check.clicked.connect(self.FourthCard)
            self.Check.clicked.connect(self.Buttons)
    
            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player2,20))
            self.Call.clicked.connect(self.CardsOnBoard)
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.FourthCard)
            self.Call.clicked.connect(self.Buttons)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player2))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player1,self.player2))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player2,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.FourthCard)
            self.bet.clicked.connect(self.Buttons)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player2))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.conenct(self.FourthCard)
            self.allIn.clicked.connect(self.Buttons)

            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 5:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Call)
            self.Call.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player2))
            self.Check.clicked.connect(self.Buttons)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player2))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player1,self.player2))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player2,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.Buttons)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player2))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.Buttons)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 6:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()
    
            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player2))
            self.Check.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.Check.clicked.connect(self.updateMoney)
            self.Check.clicked.connect(self.River)
            self.Check.clicked.connect(self.showWinner)
            self.Check.clicked.connect(self.Buttons)

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(100)
            self.Call.clicked.connect(lambda: self.game.bet(self.player2,20))
            self.Call.clicked.connect(self.CardsOnBoard)
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(self.FourthCard)
            self.Call.clicked.connect(self.Buttons)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player2))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player1,self.player2))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player2,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.River)
            self.bet.clicked.connect(self.Buttons)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player2))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.River)
            self.allIn.clicked.connect(self.Buttons)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
        
        elif self.game.turns() == 7:
            self.vbox.removeWidget(self.Call)
            self.Call.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player2))
            self.Check.clicked.connect(self.Buttons)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player2))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player1,self.player2))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player2,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.Buttons)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player2))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.Buttons)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)

        elif self.game.turns() == 8:
            self.vbox.removeWidget(self.Check)
            self.Check.deleteLater()
            self.vbox.removeWidget(self.Fold)
            self.Fold.deleteLater()
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.bet.deleteLater()
            self.betLine.deleteLater()
            self.vbox.removeWidget(self.allIn)
            self.allIn.deleteLater()

            self.Check = QPushButton("Check",self)
            self.Check.setFixedWidth(100)
            self.Check.clicked.connect(lambda: self.game.check(self.player2))
            self.Check.clicked.connect(self.showWinner)
            self.Check.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.Check.clicked.connect(self.updateMoney)

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(100)
            self.Fold.clicked.connect(lambda: self.game.fold(self.player2))
            self.Fold.clicked.connect(lambda: self.game.roundOver(self.player2,self.player1))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(100)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(100)
            self.bet.clicked.connect(lambda: self.game.bet(self.player2,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(self.showWinner)
            self.bet.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.bet.clicked.connect(self.OpponentButton)

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(100)
            self.allIn.clicked.connect(lambda: self.game.Allin(self.player2))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(self.showWinner)
            self.allIn.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
            self.allIn.clicked.connect(self.OpponentButton)

            self.vbox.addWidget(self.Check)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)
    
    def switchTurn(self,player):
        if player.name == self.player1.name:
            self.vbox.removeWidget(self.check1)
            self.vbox.removeWidget(self.fold1)
            self.vbox.removeWidget(self.bet)
            self.vbox.removeWidget(self.betLine)
            self.vbox.removeWidget(self.allIn)

            self.OpponentButton()
            self.vbox.addWidget(self.check2)
            self.vbox.addWidget(self.fold2)
            self.vbox.addWidget(self.bet2)
            self.vbox.addWidget(self.betLine2)
            self.vbox.addWidget(self.allIn2)

        elif player.name == self.player2.name:
            self.vbox.addWidget(self.check1)
            self.vbox.addWidget(self.fold1)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)

            self.vbox.removeWidget(self.check2)
            self.vbox.removeWidget(self.fold2)
            self.vbox.removeWidget(self.bet2)
            self.vbox.removeWidget(self.betLine2)
            self.vbox.removeWidget(self.allIn2)
    
    def updateMoney(self):
        self.label1.setText(f"Money: {self.player1.Money}")
        self.label2.setText(f"Opponents Money: {self.player2.Money}")
        self.label3.setText(f"Pot: {self.game.Pot}")
    
    def resetBoard(self):
        self.updateMoney()
        self.scene.clear()
    
    def showHand(self):
        list = []
        for i in range(len(self.player1.hand.cards)):
            path = os.path.abspath(os.getcwd())
            render = QSvgRenderer(path + '/Comp3/cards/Red_Back_2.svg')
            position = i
            Card = cardsInHand(render,position)
            shadow = QGraphicsDropShadowEffect(Card)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            Card.setGraphicsEffect(shadow)
            Card.setPos(i*250 + 600, 500)
            self.scene.addItem(Card)
            list.append(Card)

            path = os.path.abspath(os.getcwd())
            oppRender = QSvgRenderer(path + '/Comp3/cards/Red_Back_2.svg')
            oppCard = cardsInHand(oppRender,position)
            shadow = QGraphicsDropShadowEffect(oppCard)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            oppCard.setGraphicsEffect(shadow)
            oppCard.setPos(i*250 + 1300,500)
            self.scene.addItem(oppCard)
        return list
    
    def CardsOnBoard(self):
        cardPic = read_cards()

        for i in range(3):
            renderer = cardPic[self.boardCards[i].get_value(),self.boardCards[i].suit.value]
            position = i
            c = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5,5)
            shadow.setColor(QColor(0,0,0,180))
            c.setGraphicsEffect(shadow)
            c.setPos(600+i*250,175)
            self.scene.addItem(c)

    def FourthCard(self):
        cardPic = read_cards()

        renderer = cardPic[self.boardCards[3].get_value(),self.boardCards[3].suit.value]
        position = 4
        c = cardsInHand(renderer,position)
        shadow = QGraphicsDropShadowEffect(c)
        shadow.setBlurRadius(10.)
        shadow.setOffset(5,5)
        shadow.setColor(QColor(0,0,0,180))
        c.setGraphicsEffect(shadow)
        c.setPos(1350,175)
        self.scene.addItem(c)
    
    def River(self):
        cardPic = read_cards()

        renderer = cardPic[self.boardCards[4].get_value(),self.boardCards[4].suit.value]
        position = 5
        c = cardsInHand(renderer,position)
        shadow = QGraphicsDropShadowEffect(c)
        shadow.setBlurRadius(10.)
        shadow.setOffset(5,5)
        shadow.setColor(QColor(0,0,0,180))
        c.setGraphicsEffect(shadow)
        c.setPos(1600,175)
        self.scene.addItem(c)
    
    def showWinner(self):
        cardPic = read_cards()
        cards = self.player2.hand.cards
        
        for i,card in enumerate(cards):
            ren = cardPic[self.player1.hand.cards[i].get_value(),self.player2.hand.cards[i].suit.value]
            position = i
            c1 = cardsInHand(ren,position)
            shadow1 = QGraphicsDropShadowEffect(c1)
            shadow1.setBlurRadius(10.)
            shadow1.setOffset(5,5)
            shadow1.setColor(QColor(0,0,0,180))
            c1.setGraphicsEffect(shadow1)
            c1.setPos(600 + 250*i,500)
            self.scene.addItem(c1)
            
            renderer = cardPic[card.get_value(),card.suit.value]
            c = cardsInHand(renderer,position)
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5,5)
            shadow.setColor(QColor(0,0,0,180))
            c.setGraphicsEffect(shadow)
            c.setPos(1300 + i*250,500)
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