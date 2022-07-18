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
        self.close()


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
        self.action = []

        self.boardCards = self.game.BoardCards()
        
        self.UiInit()
        
        self.initGame()

    def UiInit(self):
        """Initializes the window with tile and sizing
        
        :param self: The QGraphicsView
        :type self: object
        """
        self.setWindowTitle("1v1 Texas Hold 'em")
        self.setGeometry(100,100,1500,1000)

        self.show()

    def initGame(self):
        if self.player1.Role == "Dealer":
            self.Buttons(self.action,self.player1,self.player2)
        else:
            self.Buttons(self.action,self.player2,self.player1)   
    
    def Buttons(self,action,player,OtherPlayer):
        """Show the buttons that the (dealer) player has to choose from
            depending on situation and stage of the game
        
        :param self: window object
        :type self: object
        
        :param action: array of actions 
        :type action: array of strings
        
        :param player: player object
        :type player: object
        
        :param OtherPlayer: another player object
        :type OtherPlayer: object
        """
        if self.game.turns() == 0:
            self.vbox = QVBoxLayout()
            self.vbox.addStretch(2)
            self.Deal1 = QPushButton("Deal",self)
            self.Deal1.setFixedWidth(200)
            self.Deal1.clicked.connect(self.game.deal)
            self.Deal1.clicked.connect(self.showHand)
            self.Deal1.clicked.connect(lambda: self.OpponentButtons(self.action.append("Deal"),player,OtherPlayer))

            self.label1 = QLabel(f"{player.name}'s money: {player.Money}")
            self.label2 = QLabel(f"{OtherPlayer.name}'s money: {OtherPlayer.Money}")
            self.label3 = QLabel(f"Pot: {self.game.Pot}")
            self.vbox.addWidget(self.label3)
            self.vbox.addWidget(self.label1)
            self.vbox.addWidget(self.label2)
            self.vbox.addWidget(self.Deal1)
    
            self.setLayout(self.vbox)

        if self.game.turns() == 2:
            self.vbox.removeWidget(self.BigBlindBet)
            self.BigBlindBet.deleteLater()

            self.vbox.removeWidget(self.See)
            self.See.deleteLater()

            self.See = QPushButton("Look at your cards",self)
            self.See.setFixedWidth(200)
            self.See.clicked.connect(lambda: self.seeCards(player))

            self.Call = QPushButton("Call",self)
            self.Call.setFixedWidth(200)
            self.Call.clicked.connect(lambda: self.game.bet(player,OtherPlayer,OtherPlayer.LastBet))
            self.Call.clicked.connect(self.CardsOnBoard)
            self.Call.clicked.connect(self.updateMoney)
            self.Call.clicked.connect(lambda: self.OpponentButtons(self.action.append("Call"),player,OtherPlayer))

            self.Fold = QPushButton("Fold",self)
            self.Fold.setFixedWidth(200)
            self.Fold.clicked.connect(lambda: self.game.fold(player))
            self.Fold.clicked.connect(lambda: self.game.roundOver(OtherPlayer,player))
            self.Fold.clicked.connect(self.resetBoard)
            self.Fold.clicked.connect(self.updateMoney)

            self.betLine = QLineEdit(self)
            self.betLine.setFixedWidth(200)

            self.bet = QPushButton("Bet",self)
            self.bet.setFixedWidth(200)
            self.bet.clicked.connect(lambda: self.game.bet(player,OtherPlayer,int(self.betLine.text())))
            self.bet.clicked.connect(self.updateMoney)
            self.bet.clicked.connect(lambda: self.OpponentButtons(self.action.append("Bet"),player,OtherPlayer))

            self.allIn = QPushButton("All in",self)
            self.allIn.setFixedWidth(200)
            self.allIn.clicked.connect(lambda: self.game.Allin(player))
            self.allIn.clicked.connect(self.updateMoney)
            self.allIn.clicked.connect(lambda: self.OpponentButtons(self.action.append("All in"),player,OtherPlayer))

            self.vbox.addWidget(self.See)
            self.vbox.addWidget(self.Call)
            self.vbox.addWidget(self.Fold)
            self.vbox.addWidget(self.bet)
            self.vbox.addWidget(self.betLine)
            self.vbox.addWidget(self.allIn)

        elif self.game.turns() >= 4 and self.game.turns() % 2 == 0:
            if self.action[-1] == "Check":
                self.vbox.removeWidget(self.Check)
                self.Check.deleteLater()
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(player))
    
                self.Check = QPushButton("Check",self)
                self.Check.setFixedWidth(200)
                self.Check.clicked.connect(lambda: self.game.check(player))
                self.Check.clicked.connect(self.updateMoney)
                self.Check.clicked.connect(lambda: self.OpponentButtons(self.action.append("Check"),player,OtherPlayer))
                if self.game.turns() == 6:
                    self.Check.clicked.connect(self.FourthCard)
                elif self.game.turns() == 8:
                    self.Check.clicked.connect(self.River)
                elif self.game.turns() == 10:
                    self.Check.clicked.connect(self.showWinner)
                    self.Check.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
                else:
                    self.Check.clicked.connect(self.CardsOnBoard)
                    self.Check.clicked.connect(lambda: self.OpponentButtons(self.action.append("Check"),player,OtherPlayer))

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(player))
                self.Fold.clicked.connect(lambda: self.game.roundOver(OtherPlayer,player))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.betLine = QLineEdit(self)
                self.betLine.setFixedWidth(200)

                self.bet = QPushButton("Bet",self)
                self.bet.setFixedWidth(200)
                self.bet.clicked.connect(lambda: self.game.bet(player,int(self.betLine.text())))
                self.bet.clicked.connect(self.updateMoney)
                self.bet.clicked.connect(lambda: self.OpponentButtons(self.action.append("Bet"),player,OtherPlayer))

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(player))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.OpponentButtons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Check)
                self.vbox.addWidget(self.Fold)
                self.vbox.addWidget(self.bet)
                self.vbox.addWidget(self.betLine)
                self.vbox.addWidget(self.allIn)
            
            elif self.action[-1] == "Call":
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
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

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(player))

                self.Deal1 = QPushButton("Deal",self)
                self.Deal1.setFixedWidth(200)
                if self.game.turns() == 6:
                    self.Deal1.clicked.connect(self.FourthCard)
                    self.Deal1.clicked.connect(lambda: self.OpponentButtons(self.action.append("Deal"),player,OtherPlayer))
                elif self.game.turns() == 8:
                    self.Deal1.clicked.connect(self.River)
                    self.Deal1.clicked.connect(lambda: self.OpponentButtons(self.action.append("Deal"),player,OtherPlayer))
                elif self.game.turns() == 10:
                    self.Deal1.clicked.connect(self.showWinner)
                    self.Deal1.clicked.connect(lambda: self.game.determineWinner(self.player1,self.player2))
                else:
                    self.Deal1.clicked.connect(self.CardsOnBoard)
                    self.Deal1.clicked.connect(lambda: self.OpponentButtons(self.action.append("Deal"),player,OtherPlayer))
                    
                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(player))
                self.Fold.clicked.connect(lambda: self.game.roundOver(OtherPlayer,player))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.betLine = QLineEdit(self)
                self.betLine.setFixedWidth(200)

                self.bet = QPushButton("Bet",self)
                self.bet.setFixedWidth(200)
                self.bet.clicked.connect(lambda: self.game.bet(player,int(self.betLine.text())))
                self.bet.clicked.connect(self.updateMoney)
                self.bet.clicked.connect(lambda: self.OpponentButtons(self.action.append("Bet"),player,OtherPlayer))

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(player))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.OpponentButtons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Deal1)
                self.vbox.addWidget(self.Fold)
                self.vbox.addWidget(self.bet)
                self.vbox.addWidget(self.betLine)
                self.vbox.addWidget(self.allIn)

            elif self.action[-1] == "Bet":
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(player))

                self.Call = QPushButton("Call",self)
                self.Call.setFixedWidth(200)
                self.Call.clicked.connect(lambda: self.game.bet(player,OtherPlayer,OtherPlayer.LastBet) == True)
                self.Call.clicked.connect(self.updateMoney)
                self.Call.clicked.connect(lambda: self.OpponentButtons(self.action.append("Call"),player,OtherPlayer))

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(player))
                self.Fold.clicked.connect(lambda: self.game.roundOver(OtherPlayer,player))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.betLine = QLineEdit(self)
                self.betLine.setFixedWidth(200)

                self.bet = QPushButton("Bet",self)
                self.bet.setFixedWidth(200)
                self.bet.clicked.connect(lambda: self.game.bet(player,int(self.betLine.text())))
                self.bet.clicked.connect(self.updateMoney)
                self.bet.clicked.connect(lambda: self.OpponentButtons(self.action.append("Bet"),player,OtherPlayer))

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(player))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.OpponentButtons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Call)
                self.vbox.addWidget(self.Fold)
                self.vbox.addWidget(self.bet)
                self.vbox.addWidget(self.betLine)
                self.vbox.addWidget(self.allIn)

            elif self.action[-1] == "All in":
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(player))
                
                self.Call = QPushButton("Call",self)
                self.Call.setFixedWidth(200)
                self.Call.clicked.connect(lambda: self.game.bet(player,OtherPlayer,OtherPlayer.LastBet) == True)
                self.Call.clicked.connect(self.updateMoney)
                self.Call.clicked.connect(lambda: self.OpponentButtons(self.action.append("Call"),player,OtherPlayer))

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(player))
                self.Fold.clicked.connect(lambda: self.game.roundOver(OtherPlayer,player))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(player))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.OpponentButtons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Call)
                self.vbox.addWidget(self.Fold)

    def OpponentButtons(self,action,player,OtherPlayer):
        """Show the buttons that the (Big blind) player has to choose from
            depending on situation and stage of the game
        
        :param self: window object
        :type self: object
        
        :param action: array of actions 
        :type action: array of strings
        
        :param player: player object
        :type player: object
        
        :param OtherPlayer: another player object
        :type OtherPlayer: object
        """
        if self.game.turns() == 1:
            self.vbox.removeWidget(self.Deal1)
            self.Deal1.deleteLater()

            self.BigBlindBet = QPushButton("Bet big blind",self)
            self.BigBlindBet.setFixedWidth(200)
            self.BigBlindBet.clicked.connect(lambda: self.game.bet(OtherPlayer,player,20))
            self.BigBlindBet.clicked.connect(self.updateMoney)
            self.BigBlindBet.clicked.connect(lambda: self.Buttons("Big Blind",player,OtherPlayer))

            self.See = QPushButton("Look at your cards",self)
            self.See.setFixedWidth(200)
            self.See.clicked.connect(lambda: self.seeCards(OtherPlayer))

            self.vbox.addWidget(self.See)
            self.vbox.addWidget(self.BigBlindBet)

        elif self.game.turns() >= 3 and self.game.turns() % 2 != 0:
            if self.action[-1] == "Call":
                self.vbox.removeWidget(self.Call)
                self.Call.deleteLater()
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(OtherPlayer))
    
                self.Check = QPushButton("Check",self)
                self.Check.setFixedWidth(200)
                self.Check.clicked.connect(lambda: self.game.check(OtherPlayer))
                self.Check.clicked.connect(self.updateMoney)   
                self.Check.clicked.connect(lambda: self.Buttons(self.action.append("Check"),player,OtherPlayer)) 

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(OtherPlayer))
                self.Fold.clicked.connect(lambda: self.game.roundOver(OtherPlayer,player))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.betLine = QLineEdit(self)
                self.betLine.setFixedWidth(200)

                self.bet = QPushButton("Bet",self)
                self.bet.setFixedWidth(200)
                self.bet.clicked.connect(lambda: self.game.bet(OtherPlayer,int(self.betLine.text())))
                self.bet.clicked.connect(self.updateMoney)
                self.bet.clicked.connect(lambda: self.Buttons(self.action.append("Bet"),player,OtherPlayer))

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(OtherPlayer))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.Buttons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Check)
                self.vbox.addWidget(self.Fold)
                self.vbox.addWidget(self.bet)
                self.vbox.addWidget(self.betLine)
                self.vbox.addWidget(self.allIn)
            
            elif self.action[-1] == "Bet":
                self.vbox.removeWidget(self.Call)
                self.Call.deleteLater()
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(OtherPlayer))

                self.Call = QPushButton("Call",self)
                self.Call.setFixedWidth(200)
                self.Call.clicked.connect(lambda: self.game.bet(OtherPlayer,player,player.LastBet))
                self.Call.clicked.connect(self.updateMoney)
                self.Call.clicked.connect(lambda: self.Buttons(self.action.append("Call"),player,OtherPlayer))

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(OtherPlayer))
                self.Fold.clicked.connect(lambda: self.game.roundOver(player,OtherPlayer))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.betLine = QLineEdit(self)
                self.betLine.setFixedWidth(200)

                self.bet = QPushButton("Bet",self)
                self.bet.setFixedWidth(200)
                self.bet.clicked.connect(lambda: self.game.bet(OtherPlayer,int(self.betLine.text())))
                self.bet.clicked.connect(self.updateMoney)
                self.bet.clicked.connect(lambda: self.Buttons(self.action.append("Bet"),player,OtherPlayer))

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(OtherPlayer))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.Buttons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Call)
                self.vbox.addWidget(self.Fold)
                self.vbox.addWidget(self.bet)
                self.vbox.addWidget(self.betLine)
                self.vbox.addWidget(self.allIn)

            elif self.action[-1] == "All in":
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(OtherPlayer))
                
                self.Call = QPushButton("Call",self)
                self.Call.setFixedWidth(200)
                self.Call.clicked.connect(lambda: self.game.bet(OtherPlayer,player,player.LastBet) == True)
                self.Call.clicked.connect(self.updateMoney)
                self.Call.clicked.connect(lambda: self.Buttons(self.action.append("Call"),player,OtherPlayer))

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(OtherPlayer))
                self.Fold.clicked.connect(lambda: self.game.roundOver(player,OtherPlayer))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(OtherPlayer))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.Buttons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Call)
                self.vbox.addWidget(self.Fold)

            if self.action[-1] == "Check":
                self.vbox.removeWidget(self.Check)
                self.Check.deleteLater()
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(OtherPlayer))
    
                self.Check = QPushButton("Check",self)
                self.Check.setFixedWidth(200)
                self.Check.clicked.connect(lambda: self.game.check(OtherPlayer))
                self.Check.clicked.connect(self.updateMoney)
                self.Check.clicked.connect(lambda: self.Buttons(self.action.append("Check"),player,OtherPlayer))

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(OtherPlayer))
                self.Fold.clicked.connect(lambda: self.game.roundOver(player,OtherPlayer))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.betLine = QLineEdit(self)
                self.betLine.setFixedWidth(200)

                self.bet = QPushButton("Bet",self)
                self.bet.setFixedWidth(200)
                self.bet.clicked.connect(lambda: self.game.bet(OtherPlayer,int(self.betLine.text())))
                self.bet.clicked.connect(self.updateMoney)
                self.bet.clicked.connect(lambda: self.Buttons(self.action.append("Bet"),player,OtherPlayer))

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(OtherPlayer))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.Buttons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Check)
                self.vbox.addWidget(self.Fold)
                self.vbox.addWidget(self.bet)
                self.vbox.addWidget(self.betLine)
                self.vbox.addWidget(self.allIn)
            
            elif self.action[-1] == "Deal":
                self.vbox.removeWidget(self.Deal1)
                self.Deal1.deleteLater()
                self.vbox.removeWidget(self.See)
                self.See.deleteLater()
                self.vbox.removeWidget(self.Fold)
                self.Fold.deleteLater()
                self.vbox.removeWidget(self.bet)
                self.vbox.removeWidget(self.betLine)
                self.bet.deleteLater()
                self.betLine.deleteLater()
                self.vbox.removeWidget(self.allIn)
                self.allIn.deleteLater()

                self.See = QPushButton("Look at your cards",self)
                self.See.setFixedWidth(200)
                self.See.clicked.connect(lambda: self.seeCards(OtherPlayer))
    
                self.Check = QPushButton("Check",self)
                self.Check.setFixedWidth(200)
                self.Check.clicked.connect(lambda: self.game.check(OtherPlayer))
                self.Check.clicked.connect(self.updateMoney)
                self.Check.clicked.connect(lambda: self.Buttons(self.action.append("Check"),player,OtherPlayer))

                self.Fold = QPushButton("Fold",self)
                self.Fold.setFixedWidth(200)
                self.Fold.clicked.connect(lambda: self.game.fold(OtherPlayer))
                self.Fold.clicked.connect(lambda: self.game.roundOver(player,OtherPlayer))
                self.Fold.clicked.connect(self.resetBoard)
                self.Fold.clicked.connect(self.updateMoney)

                self.betLine = QLineEdit(self)
                self.betLine.setFixedWidth(200)

                self.bet = QPushButton("Bet",self)
                self.bet.setFixedWidth(200)
                self.bet.clicked.connect(lambda: self.game.bet(OtherPlayer,int(self.betLine.text())))
                self.bet.clicked.connect(self.updateMoney)
                self.bet.clicked.connect(lambda: self.Buttons(self.action.append("Bet"),player,OtherPlayer))

                self.allIn = QPushButton("All in",self)
                self.allIn.setFixedWidth(200)
                self.allIn.clicked.connect(lambda: self.game.Allin(OtherPlayer))
                self.allIn.clicked.connect(self.updateMoney)
                self.allIn.clicked.connect(lambda: self.Buttons(self.action.append("All in"),player,OtherPlayer))
                
                self.vbox.addWidget(self.See)
                self.vbox.addWidget(self.Check)
                self.vbox.addWidget(self.Fold)
                self.vbox.addWidget(self.bet)
                self.vbox.addWidget(self.betLine)
                self.vbox.addWidget(self.allIn)

    def updateMoney(self):
        """Re-prints the QLabels in order to display current pot and 
            the money each player has
            
        :param self: window object
        :type self: object
        """
        self.label1.setText(f"Money: {self.player1.Money}")
        self.label2.setText(f"Opponents Money: {self.player2.Money}")
        self.label3.setText(f"Pot: {self.game.Pot}")
    
    def resetBoard(self):
        """Resets the board, takes all cards away aswell as
            updates the money after a hand has been concluded
            
        :param self: window object
        :type self: object
        """
        self.updateMoney()
        self.scene.clear()
    
    def showHand(self):
        """Displays the face down cards for the 2 players
        
        :param self: window object
        :type self: object
        """
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

    def seeCards(self,player):
        """Turns cards around in order to see what cards are in your hand
        
        :param self: window object
        :type self: object
        
        :param player: the player whos cards are to be turned around
        :type player: object
        """
        if player.name == self.player1.name:
            if player.CheckedCards % 2 == 0:
                cardPic = read_cards()
                for i in range(len(self.player1.hand.cards)):
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
                player.CheckedCards += 1
            else:
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
                player.CheckedCards += 1
        else:
            if player.CheckedCards % 2 == 0:
                cardPic = read_cards()
                cards = self.player2.hand.cards

                for i, card in enumerate(cards):
                    renderer = cardPic[card.get_value(),card.suit.value]
                    position = i
                    c = cardsInHand(renderer,position)
                    if player.CheckedCards == 0:
                        shadow = QGraphicsDropShadowEffect(c)
                        shadow.setBlurRadius(10.)
                        shadow.setOffset(5,5)
                        shadow.setColor(QColor(0,0,0,180))
                        c.setGraphicsEffect(shadow)
                    c.setPos(1300 + i*250,500)
                    self.scene.addItem(c)
                player.CheckedCards += 1
            else:
                for i in range(len(self.player1.hand.cards)):
                    path = os.path.abspath(os.getcwd())
                    render = QSvgRenderer(path + '/Comp3/cards/Red_Back_2.svg')
                    position = i
                    Card = cardsInHand(render,position)
                    if player.CheckedCards == 1:
                        shadow = QGraphicsDropShadowEffect(Card)
                        shadow.setBlurRadius(10.)
                        shadow.setOffset(5, 5)
                        shadow.setColor(QColor(0, 0, 0, 180))
                        Card.setGraphicsEffect(shadow)
                    Card.setPos(i*250 + 1300, 500)
                    self.scene.addItem(Card)
                player.CheckedCards += 1

    def CardsOnBoard(self):
        """Displays the first 3 cards on the board
        
        :param self: the window object
        :type self: object
        """
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
        """Displays the fourth card to the board
        
        :param self: the window object
        :type self: object
        """
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
        """Displays the final card to the board
        
        :param self: window object
        :type self: object
        """
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
        """Displays the hands of both players to conclude a hand of poker
        
        :param self: window object
        :type self: object
        """
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
    """Helps render the cards
    """
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