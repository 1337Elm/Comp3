from numpy import True_
from cardlib import *

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

    def fold(self):
        """If a player wants to fold, call this method which returns True
        
        :param self: player object
        :type self: object
        """
        return True

    def check(self):
        """If a player wants to check, call this method that then returns True
        
        :param self: player object
        :type self: object
        """
        return True


class Game(object):
    """Class object representing the actual game
    """
    def __init__(self,player1,player2):
        """Initializing the game
        
        :param self: game object
        :type self: object
        """
        self.deck =  StandardDeck()
        self.player1 = player1
        self.player2 = player2
        self.Pot = 0
        self.roundCounter = 0

    def round(self):
        """Defining a round of the game
        
        :param self: game object
        :type self: object
        
        returns: winner of the round
        """
        if self.roundCounter % 2 == 0:
            self.player1.Role = "Delar"
            self.player2.Role = "Big blind"
        elif self.roundCounter % 2 != 0:
            self.player1.Role = "Big blind"
            self.player2.Role = "Dealer"

        while True:
            self.deck.draw()
            for i in range(2):
                for j in range(2):
                    if j == 0:
                        self.player1.hand.add_card(self.deck.draw())
                    elif j == 1:
                        self.player2.hand.add_card(self.deck.draw())
            
            if self.player1.fold() == True:
                self.player2.Money += self.Pot
                return self.player2
            elif self.player2.fold() == True:
                self.player1.Money += self.Pot
                return self.player1

            if self.player1.Role ==  "Big blind":
                if self.bet(self.player1,20) == True:
                    pass
                elif self.player1.fold():
                    self.player2.Money += self.Pot
                    return self.player2
            elif self.player2.Rol == "Big blind":
                if self.bet(self.player2,20) == True:
                    pass
                elif self.player2.fold():
                    self.player1.Money += self.Pot
                    return self.player1
      
    def BoardCards(self):
        """Returns the cards on the board for the game
        
        :param self: the game object
        :type self: object

        :returns: list of cards
        """
        list = []
        for i in range(8):
            if i == 0 or i == 4 or i == 6:
                self.deck.draw()
            else:
                list.append(self.deck.draw())
        return list

    def bet(self,player: object, ammount):
        """Method updates the pot and the players money when placing a bet
        
        :param self: game object
        :type self: object
        
        :param player: the player object that wants to bet
        :type player: object
        
        :param ammount: the ammount to bet
        :type ammount: int

        :return: True
        """
        player.Money = player.Money - ammount
        self.Pot += ammount
        return True
    
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
        return True


 
def main():
    """Calls the classes and functions and methods above
    """
    pass


if __name__ == '__main__':
    """Shows that this file is runnable, runs the main method
    """
    main()