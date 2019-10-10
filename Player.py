'''
Created on Jan 27, 2018

@author: Yishan McNabb
'''
class Player:
    def __init__(self,name,number):
        self.name = name
        self.number = number
        self.wins = []
        self.losses = []
        self.ties = []
        self.tiebreaker = ''
	
    def __str__(self):
        return "Player Name: " + str(self.name) + " Player Wins: " + str(self.wins) + " Player Losses: " + str(self.losses) + " Player Ties: " + str(self.ties)
	
    def get_number(self):
        return self.num_wins()
    
    def get_points(self):
        return len(self.wins)*3 + len(self.ties)
    
    def num_wins(self):
        return len(self.wins)
    
    def num_losses(self):
        return len(self.losses)
    
    def num_ties(self):
        return len(self.ties)
    
    def get_opponents(self):
        played = []
        for player in self.wins:
            if player != "BYE":
                played.append(player)
        
        for player in self.losses:
            played.append(player)
        
        for player in self.ties:
            played.append(player)
    
        return played
