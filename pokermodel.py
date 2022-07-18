"""Logic of a game of Texas Hold 'em Poker

Author: Benjamin Elm Jonsson, 2022
"""
from cardlib import *
from PyQt6.QtCore import QObject, pyqtSignal

class Player(object):
    """Class representing the players of the game
    """
    def __init__(self, name):
        """Initializes the player object

        :param self: the player object
        :type self: object
        """
        self.name = name
        self.hand  = Hand()
        self.Money = 500
        self.Role = ""
        self.LastBet = 0
        self.CheckedCards = 0


class Game(object):
    """Class object representing the actual game
    """
    signal = pyqtSignal()
    def __init__(self,player1,player2):
        """Initializing the game and assigning initial roles for the players
        
        :param self: game object
        :type self: object
        """
        self.deck =  StandardDeck()
        self.deck.shuffle()

        self.player1 = player1
        self.player2 = player2
        self.Pot = 0
        self.roundCounter = 0
        self.Turn = 0

        if self.roundCounter % 2 == 0:
            self.player1.Role = "Dealer"
            self.player2.Role = "Big blind"
        elif self.roundCounter % 2 != 0:
            self.player1.Role = "Big blind"
            self.player2.Role = "Dealer"
    
    def turns(self):
        """Returns whos turn it is 
        
        :param self: game object
        :type self: object
        
        :return: int of turns that have taken place
        """
        return self.Turn
      
    def roundOver(self,winner,loser):
        """Resets the board aswell as cards for the next round
        
        :param self: game object
        :type sefl: object
        
        :param winner: the winning player of the round
        :type winner: object
        
        :param loser: the losing player of the round
        :type loser: object
        """
        winner.Money += self.Pot
        self.Pot = 0
        self.player1.hand.cards.clear()
        self.player2.hand.cards.clear()
        self.BoardCards().clear()
        self.deck = StandardDeck()
    
    def determineWinner(self,player1,player2):
        """Determines the winner of the two players
        
        :param self: the game object
        :type self: object
        
        :param player1: the first instance of the player class
        :type player1: object
        
        :param player2: the second instance of the player class
        :type player2: object
        
        :return: the winner of the round
        """
        ph1 = self.player1.hand.best_poker_hand(self.list)
        ph2 = self.player2.hand.best_poker_hand(self.list)

        if ph1 > ph2:
            print(f"The winner is {self.player1.name} with {ph1}")
            return self.player1
        elif ph2 > ph1:
            print(f"The winner is {self.player2.name} with {ph2}")
            return self.player2
        
        if self.player1.Money == 0:
            print(f"Game over {self.player2.name} wins!")
        elif self.player2.Money == 0:
            print(f"Game over {self.player1.name} wins!")

    def BoardCards(self):
        """Returns the cards on the board for the game
        
        :param self: the game object
        :type self: object

        :returns: list of cards
        """
        self.list = []
        for i in range(8):
            if i == 0 or i == 4 or i == 6:
                self.deck.draw()
            else:
                self.list.append(self.deck.draw())
        return self.list
    
    def deal(self):
        """Deals cards to the players
        
        :param self: the game object
        :type self: object
        """
        self.deck.draw()
        for i in range(2):
            for j in range(2):
                if j == 0:
                    self.player1.hand.add_card(self.deck.draw())
                elif j == 1:
                    self.player2.hand.add_card(self.deck.draw())

        self.Turn += 1
        return True
    
    def check(self,player):
        """If a player wants to check, call this method that then returns True
        
        :param self: player object
        :type self: object
        
        :return: number of times the function has been called
        """
        print(f"{player.name} has checked")
        self.Turn += 1
        return True

    def bet(self,player: object,OtherPlayer: object, ammount):
        """Method updates the pot and the players money when placing a bet
        
        :param self: game object
        :type self: object
        
        :param player: the player object that wants to bet
        :type player: object
        
        :param ammount: the ammount to bet
        :type ammount: int

        :return: True
        """
        if ammount < player.Money:
            if ammount >= OtherPlayer.LastBet:
                player.Money = player.Money - ammount
                player.LastBet += ammount
                self.Pot += ammount
                print(f"{player.name} has bet ${ammount}")
                self.Turn += 1
                return True
            else:
                print("You need to bet a larger ammount!")
                return False
        else:
            print("You don't have enough money, go all in to continue the round!")
    
    def Allin(self,player: object):
        """Updates the pot and players money when doing an all in
        
        :param self: game object
        :type self: object
        
        :param player: who is doing the all in
        :type player: object

        :return: True
        """
        self.Pot = player.Money
        player.Money = 0
        print(f"{player.name} has gone all in!")
        self.Turn += 1
        return True
    
    def fold(self,player): 
        """If a player wants to fold, call this method which returns True
        
        :param self: player object
        :type self: object

        :return: number of times the function has been called
        """
        print(f"{player.name} has folded")
        if player.name == self.player1.name:
            self.player2.Money += self.Pot
        else:
            self.player1.Money += self.Pot

        return True