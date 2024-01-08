import cv2 as cv
import numpy as np
import pytesseract
from time import time
import grabScreenShotArea
import PySimpleGUI as sg
pytesseract.pytesseract.tesseract_cmd="Tesseract-OCR\\tesseract.exe" #Path to Tesseract OCR. change this to your install location

def getScreenShotArea2(defaultTeamsNum):
    layout1 = [
        [sg.Text("How Many Teams? ")],
        [sg.Slider(range=(1,24),orientation='horizontal', default_value=defaultTeamsNum ,key='-teamsNum-')],
        [sg.Button("Next")]
    ]
    
    layout = [[sg.Column(layout1, key='-COL1-')]]

    window = sg.Window("O.A.S.I.S.", layout)
    numTeams = 0
    while True:
            event, values = window.read()
            if event == "Next":
                numTeams = int(values['-teamsNum-'])
                break
    window.close()
    
    for i in range(0,numTeams):
        grabScreenShotArea.start()
    print("All selections made!")
    return grabScreenShotArea.getTeamCaptures()

def textFromImageSimple(teamCapList):
    textArray = []
    loopTime = time()
    for i in range(0, len(teamCapList)):
        screenshot = teamCapList[i].screenshotByPos("./temp/temp.jpg")
        img = cv.imread("./temp/temp.jpg", cv.IMREAD_GRAYSCALE)

        (thresh, im_bw) = cv.threshold(img, 60, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        cv.imwrite('bw_image.png', im_bw)
        kernal = np.ones((4, 4), np.uint8)

        im_erode = cv.dilate(im_bw, kernal)
        cv.imwrite("Erode.jpg", im_erode)

        text = pytesseract.image_to_string(im_erode)
        print(text)
        savePath = "recognized" + str(i) + ".txt"
        file = open(savePath, "w+")
        file.write(text)
        textArray.extend(text.split())
    print('Seconds Per Frame {}'.format((time()-loopTime)))
    return textArray