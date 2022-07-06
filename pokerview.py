from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtSvgWidgets import *
import sys
import os


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("1v1 Texas hold 'em")

        self.left = 500
        self.top = 200
        self.width = 500
        self.height = 500

        self.CreateGraphicView()
        self.ActionButtons()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle("1v1 Texas Hold 'em")
        #self.setWindowIcon(QIcon("/Users/benjaminjonsson/Programmering/Comp3/cards/table.png"))
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.show()


    def ActionButtons(self):    
        check = QPushButton("Check",self)
        check.setGeometry(QRect(75,450,100,50))

        fold = QPushButton("Fold",self)
        fold.setGeometry(QRect(200,450,100,50))

        bet = QPushButton("Bet: ",self)
        bet.setGeometry(QRect(325,450,150,50))

        allIn = QPushButton("All in", self)
        allIn.setGeometry(QRect(325,400,100,50))
    
    def CreateGraphicView(self):
        self.scene = QGraphicsScene()
        self.title = QPixmap("/Users/benjaminjonsson/Programmering/Comp3/cards/table.png")
        self.scene.setBackgroundBrush(QBrush(self.title))

        graphicView = QGraphicsView(self.scene,self)
        graphicView.setGeometry(0,0,600,600)




app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())