import numpy as np
import cv2
from PyQt5.QtWidgets import QFileDialog, QGraphicsRectItem
from PyQt5.QtGui import QImage
from numpy.lib.type_check import _getmaxmin

class MediaPlayer:
    def __init__(self):
        print("Media Player has been initialized.")
        self.frameFormat = ""
    
    def get_frame(self):
        self.qfd = QFileDialog()
        self.imagePath = QFileDialog.getOpenFileName(self.qfd, 'Open file', '/home/yasir/eclipse-workspace/PhotoEditor/editor',"Image files (*.jpg *.gif *.png *.webp)")
        # get the image format
        lst = self.imagePath[0].split(".")
        self.frameFormat = lst[-1]
        
        self.img = cv2.imread(self.imagePath[0])        
        height, width, channels = self.img.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return qImg, height, width , self.imagePath[0]
        
    def __str__(self):
        print("Camera")
        
    def save_frame(self, pixmap):
        qfd = QFileDialog()
        path = QFileDialog.getSaveFileName(qfd, 'Save File')
        pixmap.save(path[0] + "." + self.frameFormat , self.frameFormat, 1)    
        

class Frame:
    def __init__(self, width, height, imgPath):
        self.width = width
        self.height = height
        self.imgPath = imgPath
        #List of Label object for mor than one labeling in one frame
        self.labelList = []
        
        
    def check_values(self):
        if self.width < 0:
            self.width = self.width * -1 
            self.x = self.x - self.width
        if self.height < 0:
            self.height = self.height * -1 
            self.y = self.y - self.height
    
    def save_locations(self):
        qfd = QFileDialog()
        path = QFileDialog.getSaveFileName(qfd, 'Save File')
        f = open(path[0], "a")
        text = self.imgPath + " " + str(self.width) + " " + str(self.height) + "\n"
        f.write(text)
        for lbl in self.labelList:
            txt = lbl.labelName + " " + str(lbl.xMin) + " " + str(lbl.xMax) + " " + str(lbl.yMin) + " " + str(lbl.yMax) + "\n"
            f.write(txt)
        f.close()
        

class Label:
    def __init__(self, labelName, xMin, xMax, yMin, yMax):
        self.labelName = labelName
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.rect = QGraphicsRectItem()
    
        