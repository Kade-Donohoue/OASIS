import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Player import Player
from Team import Team

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)

class SpreadSheet:
    sheetBook = client.open_by_url("https://docs.google.com/spreadsheets/d/1EoOP4WUVbKmhO1rtiYeRgHTlubRuaUzxW6EGy6zPWm8/edit#gid=0") #test sheet
    playerSheet = sheetBook.get_worksheet(1)
    teamSheet = sheetBook.get_worksheet(0)

    def __init__(self, sheetURL):
        self.sheetBook = client.open_by_url(sheetURL)
        self.playerSheet = self.sheetBook.get_worksheet(1)
        self.teamSheet = self.sheetBook.get_worksheet(0)

    #sets the teams score
    def updateTeamScore(self, team, week):
        team.updateScore()
        print(team.teamNumber, "Got", team.teamScore)
        self.teamSheet.update_cell(team.teamRow, week+1, str(team.teamScore))

    #creates a Team objects with its players and the teams name. returns array of Team objects
    def getTeams(self):
        playerCols = self.playerSheet.col_values(2)+self.playerSheet.col_values(4)+self.playerSheet.col_values(6)+self.playerSheet.col_values(8)+self.playerSheet.col_values(10)
        print(playerCols)
        teams = []
        for i in range(0,len(playerCols)-1):
            if (("team" in playerCols[i]) or ("TEAM" in playerCols[i])):
                teamNum = self.getNumFromStr(playerCols[i])
                teamPlayers= []
                for k in range(i+1, len(playerCols)-1):
                    if (("team" in playerCols[k]) or ("TEAM" in playerCols[k])):
                        i=k-1
                        print(playerCols[k])
                        teams.append(Team(teamNum, teamPlayers))
                        break
                    else:
                        teamPlayers.append(Player(playerCols[k].lower()))  
                teams.append(Team(teamNum, teamPlayers))
        self.getTeamSpot(teams)
        return teams
            
    #finds what row the team is on in the first sheet. Team number must be first then team name can follow with a space between them. 
    def getTeamSpot(self, teams):
        playerTeam = self.teamSheet.col_values(1)
        for i in range(1,len(playerTeam)):
            currentTeam = playerTeam[i].split(" ")
            try:
                teamNum = int(currentTeam[0])
                # print(" ".join(currentTeam[2:])) #prints team name
                for team in teams:
                    if team.teamNumber == teamNum:
                        team.teamRow = i+1 #saves the row that the team is on
                        # print(teamNum, i+1) 
            except:
                print("[Warning]: Team name not in propper format. Found: \"" + playerTeam[i] + "\"")

    #gets first number from a string and returns it. returns -1 if none found
    def getNumFromStr(self, string):
        teamNum = -1
        x = string.split()
        for i in x:
            if i.isnumeric():
                teamNum = int(i)
                break
        return teamNum