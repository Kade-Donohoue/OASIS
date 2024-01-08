import numpy as np
from PIL import ImageGrab

class winCapture:
    x1, x2, y1, y2 = 0,0,0,0

    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y2 = y2
        self.y1 = y1

    def screenshotByPos(self, path):
        print("start screenshot", self.x1, self.y1, self.x2, self.y2)
        im = ImageGrab.grab(bbox=(self.x1, self.y1, self.x2, self.y2)) #issue caused here
        print("screenshot taken")
        im.save(path)
        print("screenshot saved")
        return np.array(im)