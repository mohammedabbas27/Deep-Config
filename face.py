from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QHeaderView, QCheckBox,
                             qApp,QMessageBox, QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QProgressBar,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QWidget, QCalendarWidget,
                             QLabel, QApplication, QVBoxLayout)
from PyQt5.QtCore import Qt, QDate, QTimer, QThread, pyqtSignal,pyqtSlot
from time import sleep
from configparser import ConfigParser
import logging
import cv2
import sys

class VerificationPage(QDialog):

    def __init__(self):

        super().__init__()
        self.config = ConfigParser()
        self.config.read('verificationUI.properties')
        self.window_title = self.config.get(
            'verification_page_ui', 'window_title')
        self.window_width = int(self.config.get(
            'verification_page_ui', 'window_width'))
        self.window_height = int(self.config.get(
            'verification_page_ui', 'window_height'))

        self.label_font = self.config.get(
            'verification_page_ui', 'label_font')
        self.label_font_size = int(self.config.get(
            'verification_page_ui', 'label_font_size'))

        self.label_width = int(self.config.get(
            'verification_page_ui', 'label_width'))
        self.landingpage_image = self.config.get(
            'verification_page_ui', 'landingpage_image')
        
        self.default_message = self.config.get(
            'verification_page_ui', 'default_message')
        self.database_error = self.config.get(
            'verification_page_ui', 'database_error')
        self.contact_admin_message = self.config.get(
            'verification_page_ui', 'contact_admin_message')
        self.try_again_message = self.config.get(
            'verification_page_ui', 'try_again_message')


        self.title = self.window_title
        self.left = 10
        self.top = 10
        self.buzzer = 4
        self.buzzer_flag = True
        self.width = self.window_width
        self.height = self.window_height
        self.count = 1
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.move(550, 200)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setStyleSheet('''
        QMessageBox{background-color:white;}QMessageBox QPushButton{font:bold;width:60px;height:25px;border:none;margin-left:15px;margin-top:5px;background: transparent; border: 2px solid #0099CC;border-radius:6px;color: black;font-size:18}QPushButton:hover{background-color: #008CBA;color: white;}
        QDialog{background-color:white;}''')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        self.lab = QSpacerItem(30, 20, QSizePolicy.Expanding,
                               QSizePolicy.Fixed)

        label = QtWidgets.QLabel(self)
        label.move(200, 5)
        pixmap = QtGui.QPixmap(self.landingpage_image)
        # pixmap = pixmap.scaled(280, 50)
        label.setPixmap(pixmap)

        main_layout = QVBoxLayout()
        QLabel.show(label)
        details_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 60, 10, 10)
        self.camera_section()
        self.message_section()
        details_layout.addWidget(self.employee_details_groupbox)
        # details_layout.addItem(self.lab)
        details_layout.addWidget(self.employee_details_groupbox_1)
        # details_layout.addItem(self.lab)
        main_layout.addLayout(details_layout,1)
        self.setLayout(main_layout)
        self.center_screen()
        # self.showFullScreen()
        self.resize(648, 650)
        self.show()
        self.openCamera()

    def camera_section(self):
        self.employee_details_groupbox = QGroupBox('')
        self.employee_details_groupbox.setStyleSheet(
            "QGroupBox {font: bold;border: 2px solid purple;border-radius: 6px;margin-top: 4px;}QGroupBox::title {color:#017ea8; subcontrol-origin: margin; left: 7px;bottom:5px; padding: 0px 5px 40px 5px; }")
        self.employee_details_groupbox.setFont(
            QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setFixedSize(600, 400)
        
        layout.addWidget(self.label)
        self.employee_details_groupbox.setLayout(layout)
    
    def message_section(self):
        self.employee_details_groupbox_1 = QGroupBox('Message')
        self.employee_details_groupbox_1.setStyleSheet(
            "QGroupBox {font: bold;border: 2px solid purple;border-radius: 6px;margin-top: 4px;}QGroupBox::title {color:purple; subcontrol-origin: margin; left: 7px;bottom:5px; padding: 0px 5px 40px 5px; }")
        self.employee_details_groupbox_1.setFont(
            QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        layout = QHBoxLayout()
        self.employee_details_groupbox_1.setAlignment(Qt.AlignCenter)
        self.lab = QSpacerItem(30, 20, QSizePolicy.Expanding,
                               QSizePolicy.Fixed)

        self.space = QSpacerItem(30, 20, QSizePolicy.Expanding,
                               QSizePolicy.Fixed)
        
        self.label_1 = QtWidgets.QLabel(self)
        self.status = QtWidgets.QLabel("      "+self.default_message)
        self.status.setStyleSheet("QLabel{color: purple}")
        self.empty = QtWidgets.QLabel(self)
        self.empty.setFixedHeight(50)
        self.status.setFont(QtGui.QFont(self.label_font, self.label_font_size, QtGui.QFont.Bold))

        hbox = QHBoxLayout()
        layout.addStretch(1)
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.status)
        layout.addLayout(hbox)
        layout.addStretch(1)
        hbox = QVBoxLayout()
        hbox.addWidget(self.label_1)
        layout.addLayout(hbox)
        layout.addStretch(1)
        self.employee_details_groupbox_1.setLayout(layout)

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

    def nextFrameSlot(self):
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        if(self.count%40 == 0):
            # self.status.setText(str(self.count))
            pass
        self.count = self.count + 1

        
    def reset_screen(self):
        self.verify.is_start = True
        self.verify.resume()
        self.status.setText("          "+self.default_message)
        self.status.setStyleSheet("QLabel{color: purple}")
        
    def closeEvent(self,Event):
        Event.accept()
        self.close()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.close()

    def center_screen(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VerificationPage()
    sys.exit(app.exec_())
