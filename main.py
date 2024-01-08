import time
import pushGoogleSheet
import imageToText
import difflib
import PySimpleGUI as sg
import json

currentWeek = 1
numTeams = 3

botEmail = ""
sheetURL = ""
addedDelay = 0
spreadSheet = pushGoogleSheet.SpreadSheet

def main():
    global addedDelay, sheetURL, currentWeek, numTeams, botEmail
    botEmail = getBotEmail()
    savedProvidedData = getLastOptions()
    if savedProvidedData != None:
        currentWeek = savedProvidedData.get('currentWeek')
        sheetURL = savedProvidedData.get('sheetURL')
        addedDelay = savedProvidedData.get('updateDelay')
        numTeams = savedProvidedData.get('numTeams')
    
    results = startUI()
    currentWeek = results[0]
    sheetURL = results[1]
    
    #if user provides invalid delay default to 0 delay otherwise use provided delay
    try:
        addedDelay = int(results[2])
    except:
        addedDelay = 0
    
    print(sheetURL)
    spreadSheet = pushGoogleSheet.SpreadSheet(sheetURL)
    
    windowCaps = imageToText.getScreenShotArea2(numTeams)
    numTeams = len(windowCaps)
    previewLocations(numTeams, windowCaps)
    
    saveProvidedData(sheetURL, currentWeek , addedDelay, numTeams)
    teams = spreadSheet.getTeams() #Array of team objects
    updateAllTeamScores(teams, currentWeek)
    
    playerNames = getAllPlayerName(teams)
    print("Starting constant checks for score")
    while (True):
        imageToText.textFromImageSimple(windowCaps)
        getNamesFromFile(playerNames, teams, currentWeek) 
        time.sleep(addedDelay)


#start UI for startup of the program where it gets user input
def startUI():
    global addedDelay, sheetURL, currentWeek, numTeams
    layout1 = [
        [sg.Text("Welcome to the Online Automated System for Instant Stats(O.A.S.I.S.)", font="Arial 24")],
        [sg.Text("It uses screen capturing tech to automatically grab player usernames and eliminations in real time, and updates your spreadsheet instantly")],
        
    ]

    layout2 = [
        [sg.Text("What Week is it?")],
        [sg.Slider(range=(1,12),orientation='horizontal', default_value=currentWeek ,key='-week-')]
    ]
    
    layout3 = [
        [sg.Text("What is the URL for the sheet?")],
        [sg.Text("please ensure the google sheet is shared with " + botEmail)],
        [sg.Text("If the sheet is not shared or bot does not have edit access O.A.S.I.S. will not work")],
        [sg.InputText(sheetURL,key='-sheet-')]
    ]
    
    layout4 = [
        [sg.Text("How much delay do you want between new update requests?")],
        [sg.Text("Note time for image processing is not taken into account for the delay!")],
        [sg.Text("EX: time for getting score(time it take varies depending on your system) + inputted delay. ")],
        [sg.InputText(addedDelay, key='-delay-')]
    ]

    layout = [
        [sg.Column(layout1, key='-COL1-'), sg.Column(layout2, key='-COL2-', visible=False), sg.Column(layout3, key='-COL3-', visible=False), sg.Column(layout4, key='-COL4-', visible=False)],
        [sg.Button("OK"), sg.Button("Exit")]
    ]
    
    sg.theme('Dark Grey 13') 
    window = sg.Window("O.A.S.I.S.", layout)

    layout = 1
    currentWeek = 1
    
    #main control loop for start UI
    while True:
        event, values = window.read()
        if event == "OK":
            window[f'-COL{layout}-'].update(visible=False)
            if layout < 4:
                layout += 1
                window[f'-COL{layout}-'].update(visible=True)
            else:
                print("getDelay")
                addedDelay = values['-delay-']
                print(values['-delay-'])
                break
            if layout == 3: 
                print(values['-week-'])
                currentWeek = int(values['-week-'])
            if layout == 4: 
                print("getSheet")
                sheetURL = values['-sheet-']
                print(values['-sheet-'])
                
        if event in (None, "Exit", ):
            break
    window.close()
    return currentWeek, sheetURL, addedDelay

#Shows a preview of the selections the user made
def previewLocations(capNum, teamCapList):
    print("start preview")
    if capNum > 0:
        layout = [
            [],
            [sg.Button("Close")]
        ]
        print("layout created") #last output
        for i in range(capNum):
            print(f'preview{i}.png')
            teamCapList[i].screenshotByPos(f'preview{i}.png') #issue here
            print("screenshot saved!")
            layout[0].append([sg.Image(f'preview{i}.png')])
            print(f'preview{i}.png added to layout')
        print("images added to preview") #not reached
        window = sg.Window("O.A.S.I.S.", layout)
        print("window created")
        while True:
            event, values = window.read()
            if event == "Close" or event == sg.WIN_CLOSED:
                break
        window.close()

#Loads recognized text, figures out what players are captured, updates all matched players score. 
def getNamesFromFile(players, teams, week):
    for i in range(0, 3):
        file = "recognized"+str(i)+".txt"
        f=open(file,"r")
        for line in f:
            words=line.split()
            if words:
                likleyName = difflib.get_close_matches(words[0], players, 1)
                print(likleyName, words[0], words[len(words)-1])
                if (len(likleyName)>0):
                    try:
                        updateScore(teams, likleyName[0], int(words[len(words)-1]), week)
                    except:
                        continue
        f.close()

#has all teams update their score and pushes it to google sheets
def updateAllTeamScores(teams,week):
    startTime = time.time()
    for team in teams:
        spreadSheet.updateTeamScore(spreadSheet, team,week)
    print("Took", time.time()-startTime, "seconds")

#Updates score for team on google sheet based on a players score
def updateScore(teams, playerName, newScore, week):
    playerName = playerName.lower()
    team = findPlayerTeam(teams, playerName)
    # print(getPlayerFromTeam(teams, playerName))
    player = getPlayerFromTeam(teams, playerName)
    if (player != None):
        player.score = newScore
        print("updateing player score")
        spreadSheet.updateTeamScore(spreadSheet, team, week)
    else:
        print("Invalid Player")

#Returns the Team object that has a player matching the provided player name
def findPlayerTeam(teams, playerName):
    for team in teams:
        if (team.checkPlayer(playerName)):
            return team

#returns the Player object matching the provided player Name using the provided Team List
def getPlayerFromTeam(teams, playerName):
    for team in teams:
        if (team.checkPlayer(playerName)):
            return team.getPlayer(playerName)

#returns list of all player names from the provided Team list
def getAllPlayerName(teams):
    playerNames = []
    for team in teams:
        for player in team.playerList:
            playerNames.append(player.name)
    return playerNames


#saves users inputs so they can be autofilled on next run
def saveProvidedData(sheetURL, week, updateDelay, numTeams):
    print("WIP")
    
    data = {
        "sheetURL": sheetURL,
        "currentWeek": week,
        "updateDelay": updateDelay,
        "numTeams": numTeams
    }
    
    jsonData = json.dumps(data, indent=4)
    
    with open("./data/lastOptions.json", "w") as outfile:
        outfile.write(jsonData)

#returns dictionary of users last inputs
def getLastOptions():
    try:
        with open("./data/lastOptions.json", "r") as openFile:
            return json.load(openFile)
    except:
        return None
    
#returns client_email from client_key
def getBotEmail():
    try:
        with open("./client_key.json", "r") as openFile:
            data = json.load(openFile)
            return data.get('client_email')
    except:
        return "Please fill out client key!!!!"
    
main()