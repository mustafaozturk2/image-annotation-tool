import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QPushButton, QFileDialog,\
    QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem
from PyQt5.QtCore import QRect, Qt, QRectF, QThread, pyqtSlot
from PyQt5.Qt import QMainWindow, QWidget, QPixmap, QSize, QTransform
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QIcon, QImage

from models import MediaPlayer, Frame, Label
#from Thread import Thread


class AppWindow( QMainWindow):
    
        
    
    def __init__(self):
        super().__init__()
        loadUi('design.ui', self)
        self.showMaximized()
        self.setWindowTitle("Image Annotation Tool v0.1")
        self.setFixedSize(self.size())
        self.myPixmap = QtGui.QPixmap()
        #=======================================================================
        # self.th = Thread(self)
        #=======================================================================
        #boolean for image
        self.IMAGE_LOADED = False
        self.scene = QtWidgets.QGraphicsScene(0, 0, 500, 555)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.installEventFilter(self)
        self.graphicsView.setHorizontalScrollBarPolicy(1)
        self.graphicsView.setVerticalScrollBarPolicy(1)
        self.graphicsView.setGeometry(QRect(0, 0, 475, 514))
        
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.pixmap_item.mousePressEvent = self.mousePressedImage
        self.pixmap_item.mouseMoveEvent = self.mouseMoveImage
        self.pixmap_item.mouseReleaseEvent = self.mouseReleasedImage
       
        self.loadImgBtn.clicked.connect(self.set_frame)
        self.saveBtn.clicked.connect(self.saveTxt)
        self.undoBtn.clicked.connect(self.undo)
        #=======================================================================
        # self.playPauseBtn.clicked.connect(self.playPause)
        #=======================================================================
        
        self.frame = Frame(0 , 0, "/")
        #first coordinates
        self.FIRST_X = 0
        self.FIRST_Y = 0
        
        #last coordinates
        self.SECOND_X = 0
        self.SECOND_Y = 0
        
        self.xMin = 0
        self.xMax = 0
        self.yMin = 0
        self.yMax = 0
        self.width = 0
        self.height = 0
        
        self.labelList = []
        self.listWidget.itemSelectionChanged.connect(self.itemSelected)
        
        self.tempRect = QGraphicsRectItem(0, 0, 1, 1)
        self.tempRect2 = QGraphicsRectItem(0, 0, 1, 1)
        
        self.colorDict = {}
     
    
    def itemSelected(self):
        print("item selected: ", self.listWidget.currentItem().text())
    
    #===========================================================================
    # def playPause(self):
    #     self.th.playPause();
    #     self.th.start()
    #===========================================================================
    
    def openDialog(self):
        labelSet = Dialog()
        result = labelSet.exec_()
        print(result)
    
    #===========================================================================
    # @pyqtSlot(QImage)
    # def setImage(self, image):
    #     self.pixmap_item.setPixmap(QPixmap.fromImage(image))
    #     self.scene.setSceneRect(self.pixmap_item.boundingRect())
    #     self.scale = width / pixmap_item.rect().width()
    #===========================================================================
        
    
    def undo(self):
        self.scene.removeItem(self.frame.labelList[-1].rect)
        self.frame.labelList.pop()
        self.scene.removeItem(self.labelList[-1])
        self.labelList.pop()
        self.listWidget.takeItem(self.listWidget.count()-1)
        #=======================================================================
        # self.th.changePixmap.connect(self.setImage)
        # self.th.setViewSize(self.graphicsView.size())
        # self.th.start()
        # self.IMAGE_LOADED = True
        #=======================================================================
        
        
    def set_frame(self):
        frame, height, width, imgPath = MediaPlayer.get_frame(self)
        self.myPixmap = QtGui.QPixmap(frame)
        self.frame = Frame(width, height, imgPath)
        self.IMAGE_LOADED = True
        #myScaledPixmap = self.myPixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        ratio = height / width

        pix = self.myPixmap.scaled(self.graphicsView.size(), QtCore.Qt.KeepAspectRatio)
        self.pixmap_item.setPixmap(pix)
        self.scale = width / pix.rect().width()
        #self.graphicsView.setGeometry(self.pixmap_item.boundingRect().toRect())
        self.scene.setSceneRect(self.pixmap_item.boundingRect())
        
    
    def draw(self, event):
        print("oldu mu", self.scene.itemAt(event.scenePos().x(), event.scenePos().y(), QTransform()))
        #self.scene.removeItem(self.scene.itemAt(event.scenePos().x(), event.scenePos().y(), QTransform()))
    
    def mousePressedImage(self, event):
        self.FIRST_X = int(event.pos().x())
        self.FIRST_Y = int(event.pos().y())
    
    
    def changeRectColor(self):
        pass
        
    
    def mouseMoveImage(self, event):
        """
        When mouse pressed on image and keeps moving
        """
        self.SECOND_X = int(event.pos().x())
        self.SECOND_Y = int(event.pos().y())
        if self.IMAGE_LOADED:
            if self.FIRST_X != int(event.pos().x()) and self.FIRST_Y != int(event.pos().y()):
                if self.SECOND_X <= self.pixmap_item.boundingRect().width() and self.SECOND_X > 0:
                    if self.SECOND_Y <= self.pixmap_item.boundingRect().height() and self.SECOND_Y > 0:
                        if self.tempRect:
                            self.scene.removeItem(self.tempRect)
                        #print("Released at: ", self.SECOND_X, self.SECOND_Y)
                        # kordinatları resim üzerine scale et
                        
                        if self.FIRST_X > self.SECOND_X:
                            self.xMin = self.SECOND_X
                            self.xMax = self.FIRST_X
                        else:
                            self.xMin = self.FIRST_X
                            self.xMax = self.SECOND_X
                        
                        if self.FIRST_Y > self.SECOND_Y:
                            self.yMin = self.SECOND_Y
                            self.yMax = self.FIRST_Y
                        else:
                            self.yMin = self.FIRST_Y
                            self.yMax = self.SECOND_Y
                        
                        self.width = self.xMax - self.xMin
                        self.height = self.yMax - self.yMin

                    
                        self.tempRect = QGraphicsRectItem(self.xMin, self.yMin, self.width, self.height)
                        self.tempRect.setFlag(QGraphicsItem.ItemIsMovable, True)
                        #item.mousePressEvent = self.draw
                        #item.setBrush(QBrush(QColor(255, 0, 0, 100)))
                        self.tempRect.prepareGeometryChange()
                        self.tempRect.setPen(QPen(QColor(250, 0, 0), 2.0, Qt.SolidLine))
                        
                        self.scene.addItem(self.tempRect)
            else:
                return
        else:
            print("No image was loaded")
    
    
    def mouseReleasedImage(self, event):
        
        if self.IMAGE_LOADED:
            self.SECOND_X = int(event.pos().x())
            self.SECOND_Y = int(event.pos().y())
            if self.IMAGE_LOADED:
                if self.FIRST_X != int(event.pos().x()) and self.FIRST_Y != int(event.pos().y()):
                    if self.SECOND_X <= self.pixmap_item.boundingRect().width() and self.SECOND_X > 0:
                        if self.SECOND_Y <= self.pixmap_item.boundingRect().height() and self.SECOND_Y > 0:
                            dialog = Dialog()
                            result = dialog.exec_()
                            if result == 1:
                                self.scene.removeItem(self.tempRect)
                                labelName = dialog.lineEdit.text()
                                if labelName == "":
                                    labelName = "null"
                                self.frame.labelList.append(Label(labelName
                                                  , int(self.xMin*self.scale)
                                                  , int(self.xMax* self.scale)
                                                  , int(self.yMin* self.scale)
                                                  , int(self.yMax* self.scale)))
                                self.listWidget.addItem(self.frame.labelList[-1].labelName)
                                self.frame.labelList[-1].rect = QGraphicsRectItem(self.xMin, self.yMin, self.width, self.height)
                                self.frame.labelList[-1].rect.prepareGeometryChange()
                                self.frame.labelList[-1].rect.setPen(QPen(QColor(250, 250, 0), 2.0, Qt.SolidLine))
                                self.scene.addItem(self.frame.labelList[-1].rect)
                                label = QGraphicsTextItem()
                                label.setPos(self.xMin, self.yMin)
                                label.setHtml("<div style='background-color:red; color: white'>" + dialog.lineEdit.text() + "</div>")
                                self.labelList.append(label)
                                self.scene.addItem(self.labelList[-1])
                            else:
                                self.scene.removeItem(self.tempRect)
                        else:
                            self.scene.removeItem(self.tempRect)
                    else:
                        self.scene.removeItem(self.tempRect)
            else:
                #self.scene.removeItem(self.tempRect)
                pass
        else:
            print("No image was loaded")
        
    
    
    def saveTxt(self):
        self.frame.save_locations()
            
        
class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        loadUi('dialog.ui', self)
        self.setWindowTitle("Set Label Name")
        
    
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("app.png"))
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
