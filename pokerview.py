from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvg import *
from PyQt6.QtWidgets import *
from PyQt6.QtSvgWidgets import *
import sys
from abc import abstractmethod
from cardlib import *

class CardModel(QObject):
    new_cards = pyqtSignal()

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def flipped(self):
        pass


class HandModel(CardModel):
    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)
        # Additional state needed by the UI
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!


class Table(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.title = QPixmap('/cards/table.png')
        self.setBackgroundBrush(QBrush(self.title))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position

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
            all_cards[key] = QSvgRenderer('/Users/benjaminjonsson/Programmering/Comp3/cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    back_card = QSvgRenderer('/Users/benjaminjonsson/Programmering/Comp3/cards/Red_Back_2.svg')
    all_cards = read_cards()
    
    def __init__(self, card_model: CardModel, card_spacing: int = 250, padding: int = 10):
        self.scene = Table()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding
        self.model = card_model
        card_model.new_cards.connect(self.change_cards)

        self.change_cards()
    
    def change_cards(self):
        self.scene.clear()
        for i, card in enumerate(self.model):
            graphics_key = (card.get_value(), card.suit)
            renderer = self.back_card if self.model.flipped() else self.all_cards[graphics_key]
            c = CardItem(renderer,i)

            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5,5)
            shadow.setColor(QColor(0,0,0,180))
            c.setGraphicsEffect(shadow)
            c.setPos(c.position*self.card_spacing,0)
            self.scene(c)
        self.update_view()

    def update_view(self):
        scale = (self.viewport().height() -2*self.padding)/313
        self.resetTransform()
        self.scale(scale,scale)
        self.setSceneRect(-self.padding//scale,-self.padding//scale,
                            self.viewport().width()//scale, self.viewport().height()//scale)
        
    def resizeEvene(self,painter):
        self.update_view()
        super().resizeEvent(painter)


app = QApplication(sys.argv)
card_view = CardView(CardModel)
box = QVBoxLayout()
box.addWidget(card_view)
player_view = QGroupBox("player1")
player_view.setLayout(box)
player_view.show()

app.exec()