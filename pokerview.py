"""GUI of a game of Texas Hold 'em Poker

Author: Benjamin Elm Jonsson, 2022
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtSvgWidgets import *
import sys
import os
from pokermodel import *


class Window(QMainWindow):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.left = 500
        self.top = 200
        self.width = 500
        self.height = 500

        self.CreateGraphicView()
        self.ActionButtons()
        self.showCards()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle("1v1 Texas Hold 'em")
        self.setGeometry(self.left,self.top,self.width,self.height)

        self.show()


    def ActionButtons(self):    
        check = QPushButton("Check",self)
        check.setGeometry(QRect(75,450,100,50))
        #check.clicked.connect(Player.check())

        fold = QPushButton("Fold",self)
        fold.setGeometry(QRect(200,450,100,50))
        #fold.clicked.connect(Player.fold())

        bet = QPushButton("Bet: ",self)
        bet.setGeometry(QRect(325,450,90,50))
        betLine = QLineEdit(self)
        betLine.setGeometry(425,455,50,40)

        #Connect QLineEdit to Bet button, Bet button should function as "Submit"
        #that then calls the bet function in pokermodel.py

        #betAmmount = betLine.returnPressed.connect()
        #bet.clicked.connect(Game.bet(self,betAmmount))

        allIn = QPushButton("All in", self)
        allIn.setGeometry(QRect(325,400,90,50))
        #allIn.clicked.connect(Game.Allin())
    
    def CreateGraphicView(self):
        path2background = os.path.abspath(os.getcwd())
        backgroundFile = os.path.join(path2background + '/Comp3/cards/table.png')

        self.scene = QGraphicsScene()
        self.title = QPixmap(backgroundFile)
        self.scene.setBackgroundBrush(QBrush(self.title))
    
        graphicView = QGraphicsView(self.scene,self)
        graphicView.setGeometry(0,0,1000,1000)

        #Retrieve the card from pokermodel
        #cards = self.read_cards() # Returning dic of [value,suit.value] to show it use, addItem()
        #self.scene.addItem(cards[2,0]) # How tf do I choose where this goes??? Again... -.-
    
    def showCards(self):
        path = os.path.abspath(os.getcwd())
        file = os.path.join(path + '/Comp3/cards/Red_Back_2.svg')

        self.scene.addItem(QGraphicsSvgItem(file)) #How tf do I choose where this goes???


    def read_cards(self):
        """
        Reads all the 52 cards from files.
        :return: Dictionary of SVG renderers
        """
        all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
        for suit_file, suit in zip('HDSC', range(4)):  # Check the order of the suits here!!!
            for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
                file = value_file + suit_file
                key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
                
                path = os.path.abspath(os.getcwd())
                all_cards[key] = QGraphicsSvgItem(path + '/Comp3/cards/' + file + '.svg')
        return all_cards



app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())