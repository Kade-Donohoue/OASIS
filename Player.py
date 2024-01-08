class Player:
    score = 0
    name = ''

    def __init__(self, name, score = 0):
        self.score = score
        self.name = name
    
    def changeScore(self, newValue):
        self.score = newValue