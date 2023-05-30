# Cara pakai :
# 1. Masukkan nilai FPS
# 2. Klik open untuk memulai video
# 3. Apabila ingin menganti FPS, ketik pada Qline lalu klik start
# 4. Tekan space untuk keluar dari program


from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit , QLabel
from PyQt5.QtCore import QTimer
from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage , QPixmap
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets,uic

import sys, time,  cv2
import numpy as np
import time,imutils


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("ab.ui",self)
        self.show() # show the ui 
        
        self.filename = None
        self.webcam = cv2.VideoCapture(0) # Masukkin video default
        self.tmp = None
        self.started = False
        self.minH_now = 0
        self.minS_now = 0
        self.minV_now = 0
        self.maxH_now = 179
        self.maxS_now = 255
        self.maxV_now = 255
        self.lineFPS.setPlaceholderText('Masukkan nilai fPS')
        self.pushButton.clicked.connect(self.savePhoto)
        self.pushButton_2.clicked.connect(self.playtimer)
        self.pushButton_3.clicked.connect(self.stoptimer)
        self.pushButton_4.clicked.connect(self.loadImage)
        self.MinHSlider.valueChanged['int'].connect(self.minH_value)
        self.MinSSlider.valueChanged['int'].connect(self.minS_value)
        self.MinVSlider.valueChanged['int'].connect(self.minV_value)
        self.MaxHSlider.valueChanged['int'].connect(self.maxH_value)
        self.MaxSSlider.valueChanged['int'].connect(self.maxS_value)
        self.MaxVSlider.valueChanged['int'].connect(self.maxV_value)
        
        
        #Start our timer that calls camera functions
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.camera)
    
    def keyPressEvent(self,event) :
        if event.key() == Qt.Key_Escape:
            self.press()
    def press(self):
        sys.exit()
   


    def camera(self):
        #Sliders for HSV changing for lower limits
        minH = self.MinHSlider.value()
        minS = self.MinSSlider.value()
        minV = self.MinVSlider.value()
        #Sliders for HSV changing for upper limits
        maxH = self.MaxHSlider.value()
        maxS = self.MaxSSlider.value()
        maxV = self.MaxVSlider.value()
        
        image, self.imageFrame = self.webcam.read() 
        self.res = self.imageFrame
        self.imageFrame = cv2.cvtColor(self.imageFrame, cv2.COLOR_RGB2BGR) 
        hsvFrame = cv2.cvtColor(self.imageFrame, cv2.COLOR_BGR2HSV) 
        color_lower = np.array([minH, minS, minV], np.uint8) 
        color_upper = np.array([maxH, maxS, maxV], np.uint8) 
        color_mask = cv2.inRange(hsvFrame, color_lower, color_upper) 
        kernal = np.ones((5, 5), "uint8") 
        color_mask = cv2.dilate(color_mask, kernal) 
        frame = cv2.bitwise_and(self.imageFrame, self.imageFrame, mask = color_mask) 
        
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        img_temp = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        self.tmp = img_temp
        #Display image
        self.MainCam.setPixmap(QPixmap.fromImage(image))
        self.update()
        minValuesHSV= f"Min HSV values = {minH} | {minS} | {minV}"
        maxValuesHSV = f"Max HSV values = {maxH} | {maxS} | {maxV}"
        self.minhsv.setText(minValuesHSV)
        self.maxhsv.setText(maxValuesHSV)
        
    def loadImage(self):
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.webcam = cv2.VideoCapture(self.filename)
        fps = self.webcam.get(cv2.CAP_PROP_FPS)
        self.camera()
        self.timer.start(fps)

    def setPhoto(self,image):

        image = imutils.resize(image,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.tmp = image
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.MainCam.setPixmap(QtGui.QPixmap.fromImage(image))
        minValuesHSV= f"Min HSV values = {self.minH_now} | {self.minS_now} | {self.minV_now}"
        maxValuesHSV = f"Max HSV values = {self.maxH_now} | {self.maxS_now} | {self.maxV_now}"
        self.minhsv.setText(minValuesHSV)
        self.maxhsv.setText(maxValuesHSV)

    def minH_value(self,value):
        self.minH_now = value
        self.update()

    def minS_value(self,value):
        self.minS_now = value
        self.update()

    def minV_value(self,value):
        self.minV_now = value
        self.update()
    
    def maxH_value(self,value):
        self.maxH_now = value
        self.update()

    def maxS_value(self,value):
        self.maxS_now = value
        self.update()

    def maxV_value(self,value):
        self.maxV_now = value
        self.update()
        

    def changeHSV(self,img):

        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        color_lower = np.array([self.minH_now,self.minS_now,self.minV_now],np.uint8)
        color_upper = np.array([self.maxH_now,self.maxS_now,self.maxV_now],np.uint8)
        color_mask = cv2.inRange(hsv, color_lower, color_upper)
        kernal = np.ones((5, 5), "uint8") 
        color_mask = cv2.dilate(color_mask, kernal)
        res_color = cv2.bitwise_and(img, img, mask = color_mask) 
        
        return res_color



   
    def update(self):
        
        img = self.changeHSV(self.res)
        self.setPhoto(img)
        

    def stoptimer(self):
        self.camera()
        self.timer.stop()

    def playtimer(self):
        fps = int(self.lineFPS.text())
        res = 1000 / fps
        self.timer.start(res)


 
    def savePhoto(self):
        """ Menyimpan gambar """
        self.filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(self.filename,self.tmp)
        print('Image saved as:',self.filename)



      
app = QApplication(sys.argv)
window = UI()
app.exec_()