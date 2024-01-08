import tkinter
from customtkinter import *
import windowCaptureV2
win = CTk()

#trasparent grayish background
board = tkinter.Toplevel(win)

# hide window unitl selecting region
board.withdraw()
canvas = None

startX,startY=None,None #track starting pos
curX,curY=None,None #track mouse cur pos

# rectangle for showing user selection
snipRect = None

restartFlag = False

teamCaptures = []

def start():
    global canvas
    win.withdraw()
    board.deiconify()
    canvas = tkinter.Canvas(board,cursor='cross',bg='grey11')
    canvas.pack(fill=BOTH, expand=YES)
    canvas.bind("<ButtonPress-1>", mousePress)
    canvas.bind("<B1-Motion>", mouseMove)
    canvas.bind("<ButtonRelease-1>", mouseRelease)
    board.bind("<Escape>", restartSnipMode)
    board.lift()
    board.attributes('-fullscreen', True)
    board.attributes('-alpha', 0.25)
    board.attributes("-topmost", True)
    
    win.wait_window(canvas) #waits until the selection is made ensuring program doesnt move on before ready. 
    
#moves a corner of the selection rectangle with the mouse    
def mouseMove(event):
    global snipRect,startX,startY,curX,curY
    startX,startY = (event.x, event.y)
    # expand rectangle as you drag the mouse
    canvas.coords(snipRect, startX, startY, curX, curY)
    return 'break'

#creates rectangle for selection and record where user first selected
def mousePress(event):
    global snipRect,startX,startY,curX,curY
    startX=curX=canvas.canvasx(event.x)
    startY=curY=canvas.canvasy(event.y)
    snipRect = canvas.create_rectangle(startX,startY, 2, 2, outline='red', width=3, fill="white")
    return 'break'

#ends selection
def escapeSnipMode(_):
    canvas.destroy()
    board.withdraw()
    win.deiconify()

#removes rectangle and allows user to stop clicking and restart    
def restartSnipMode(_):
    global snipRect, restartFlag
    canvas.delete(snipRect)
    restartFlag = True

#gets where users end pos is and creates a windowCapture object with it. 
def mouseRelease(event):
    global startX,startY,curX,curY,teamCaptures, restartFlag
    
    # print(restartFlag)
    if restartFlag:
        restartFlag = False
        print("skipped for restart")
        return 'break'
    
    # supports left-down, right-up, right-down and left-up selections
    elif startX <= curX and startY <= curY:
        teamCaptures.append(windowCaptureV2.winCapture(int(startX), int(curX), int(startY), int(curY)))
    elif startX >= curX and startY >= curY:
        teamCaptures.append(windowCaptureV2.winCapture(int(curX), int(startX), int(curY), int(startY)))
    elif startX >= curX and startY <= curY:
        teamCaptures.append(windowCaptureV2.winCapture(int(curX), int(startX), int(startY), int(curY)))
    elif startX <= curX and startY >= curY:
        teamCaptures.append(windowCaptureV2.winCapture(int(startX), int(curX), int(curY), int(startY)))
    escapeSnipMode(0)
    print("Saving Section")
    return 'break'

def getTeamCaptures():
    global teamCaptures
    return teamCaptures