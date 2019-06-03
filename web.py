
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QThread, pyqtSignal,pyqtSlot
# from time import sleep
# from PyQt5 import Qt
# from PyQt5.QtGui import QImage, QPixmap
# import cv2
# from PyQt5.QtWidgets import QLabel
# import sys


# class Thread(QThread):
#     changePixmap = pyqtSignal(QImage)

#     def run(self):
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             if ret:
#                 # https://stackoverflow.com/a/55468544/6622587
#                 rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = rgbImage.shape
#                 bytesPerLine = ch * w
#                 convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
#                 p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
#                 self.changePixmap.emit(p)


# class App(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 Video'
#         self.left = 100
#         self.top = 100
#         self.width = 640
#         self.height = 480
#         self.initUI()

#     @pyqtSlot(QImage)
#     def setImage(self, image):
#         self.label.setPixmap(QPixmap.fromImage(image))

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.resize(900, 600)
#         # create a label
#         self.label = QLabel(self)
#         self.label.move(280, 120)
#         self.label.resize(640, 480)
#         th = Thread(self)
#         th.changePixmap.connect(self.setImage)
#         th.start()
#         self.show()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal,pyqtSlot
from time import sleep
from PyQt5 import Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtWidgets import QLabel
import sys

# import dbr
import os

class UI_Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # The default barcode image.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, 'image.tif')

        # Create a timer.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        # Create a layout.
        layout = QtWidgets.QVBoxLayout()

        # Add a button
        self.btn = QtWidgets.QPushButton("Load an image")
        self.btn.clicked.connect(self.pickFile)
        layout.addWidget(self.btn)

        # Add a button
        button_layout = QtWidgets.QHBoxLayout()

        btnCamera = QtWidgets.QPushButton("Open camera")
        btnCamera.clicked.connect(self.openCamera)
        button_layout.addWidget(btnCamera)

        btnCamera = QtWidgets.QPushButton("Stop camera")
        btnCamera.clicked.connect(self.stopCamera)
        button_layout.addWidget(btnCamera)

        layout.addLayout(button_layout)

        # Add a label
        self.space = QLabel()
        self.space.setFixedSize(50, 50)
        layout.addWidget(self.space)

        self.label = QLabel()
        self.label.setFixedSize(640, 640)
        pixmap = self.resizeImage(filename)
        self.label.setPixmap(pixmap)
        layout.addWidget(self.label)

        # Add a text area
        self.results = QtWidgets.QTextEdit()
        self.readBarcode(filename)
        layout.addWidget(self.results)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("Dynamsoft Barcode Reader")
        self.setFixedSize(800, 800)
        self.count = 1

    # https://stackoverflow.com/questions/1414781/prompt-on-exit-in-pyqt-application
    def closeEvent(self, event):
    
        msg = "Close the app?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', 
                        msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.stopCamera()
        else:
            event.ignore()

    def readBarcode(self, filename):
        # dbr.initLicense("Your License")
        # results = dbr.decodeFile(filename, 0x3FF | 0x2000000 | 0x4000000 | 0x8000000 | 0x10000000)

        # out = ''
        # index = 0
        # for result in results:
        #     out += "Index: " + str(index) + "\n"
        #     out += "Barcode format: " + result[0] + '\n'
        #     out += "Barcode value: " + result[1] + '\n'
        #     out += '-----------------------------------\n'
        #     index += 1

        # self.results.setText(out)
        return

    def resizeImage(self, filename):
        pixmap = QPixmap(filename)
        lwidth = self.label.maximumWidth()
        pwidth = pixmap.width()
        lheight = self.label.maximumHeight()
        pheight = pixmap.height()

        wratio = pwidth * 1.0 / lwidth
        hratio = pheight * 1.0 / lheight

        if pwidth > lwidth or pheight > lheight:
            if wratio > hratio:
                lheight = pheight / wratio
            else:
                lwidth = pwidth / hratio

            scaled_pixmap = pixmap.scaled(lwidth, lheight)
            return scaled_pixmap
        else:
            return pixmap

    def pickFile(self):
        self.stopCamera()
        # Load an image file.
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                               'E:\\Program Files (x86)\\Dynamsoft\\Barcode Reader 6.5.2\\Images', "Barcode images (*)")
        # Show barcode images
        pixmap = self.resizeImage(filename[0])
        self.label.setPixmap(pixmap)

        # Read barcodes
        self.readBarcode(filename[0])

    def openCamera(self):
        self.vc = cv2.VideoCapture(0)
        # vc.set(5, 30)  #set FPS
        self.vc.set(3, 640) #set width
        self.vc.set(4, 480) #set height

        if not self.vc.isOpened(): 
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

        self.timer.start(1000./24)
    
    def stopCamera(self):
        self.timer.stop()

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        # results = dbr.decodeBuffer(frame, 0x3FF | 0x2000000 | 0x4000000 | 0x8000000 | 0x10000000)
        # out = ''
        # index = 0
        # for result in results: 
        #     out += "Index: " + str(index) + "\n"
        #     out += "Barcode format: " + result[0] + '\n'
        #     out += "Barcode value: " + result[1] + '\n'
        #     out += '-----------------------------------\n'
        #     index += 1

        # self.results.setText(out)
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = UI_Window()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()