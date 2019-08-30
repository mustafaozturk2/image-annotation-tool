import cv2
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, QSize
from PyQt5 import QtCore, QtGui, Qt

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    viewsize = QSize(100, 100)
    play = True
    scale = 0
    
    def setViewSize(self, viewSize):
        self.viewSize = viewSize
        
    def getScale(self):
        return self.scale
    
    def playPause(self):
        self.play = not self.play
    
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
           if self.play:
                ret, frame = cap.read()
                if ret:
                    # https://stackoverflow.com/a/55468544/6622587
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(self.viewSize, QtCore.Qt.KeepAspectRatio)
                    self.scale = w / p.rect().width()
                    self.changePixmap.emit(p)
                    
                    
                    