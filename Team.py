class Team:
    teamNumber = -1
    playerList = []
    teamScore = 0
    teamRow = 0
    teamName = ""

    def __init__(self, teamNumber, playerList = [], score = 0):
        self.teamNumber = teamNumber
        self.playerList = playerList
        self.teamScore = score

    def checkPlayer(self, playerName):
        for player in self.playerList:
            if (player.name == playerName):
                return True
        return False
    
    def getPlayer(self, playerName):
        for player in self.playerList:
            if (player.name == playerName):
                return player
        return None
    
    def updateScore(self):
        self.teamScore = 0
        for player in self.playerList:
            self.teamScore += player.score