import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QHeaderView, QCheckBox,
                             qApp,QMessageBox, QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QProgressBar,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout)
from PyQt5.QtWidgets import (QWidget, QCalendarWidget,
                             QLabel, QApplication, QVBoxLayout)
from PyQt5.QtCore import QDate,QTimer
import time
from configparser import ConfigParser
import logging
import cv2

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal,pyqtSlot
from time import sleep
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtWidgets import QLabel
import sys

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    # def __init__(self):
    #     self.timer = QtCore.QTimer()
    #     self.timer.timeout.connect(self.nextFrameSlot)
    
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
    
    def nextFrameSlot(self):
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap.fromImage(image)
        self.changePixmap.emit(image)
        print("Signal")
        # self.label.setPixmap(pixmap)

    def run(self):
        # while True:
        # self.openCamera()

        self.vc = cv2.VideoCapture(0)
        # vc.set(5, 30)  #set FPS
        self.vc.set(3, 640) #set width
        self.vc.set(4, 480) #set height
        while True:
            rval, frame = self.vc.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            # pixmap = QPixmap.fromImage(image)
            self.changePixmap.emit(image)


        # cap = cv2.VideoCapture(0)
        # while True:
        #     ret, frame = cap.read()
        #     if ret:
        #         # https://stackoverflow.com/a/55468544/6622587
        #         rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         h, w, ch = rgbImage.shape
        #         bytesPerLine = ch * w
        #         convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        #         p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        #         self.changePixmap.emit(p)

                
class VerificationPage(QDialog):

    def __init__(self):

        super().__init__()
        self.config = ConfigParser()
        self.config.read('verificationUI.properties')
        self.sleep_time = self.config.get(
            'verification_page_ui', 'time_sleep')
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
        
        self.blink_threshold = int(self.config.get(
            'verification_page_ui', 'blink_threshold'))
        self.accept_message = self.config.get(
            'verification_page_ui', 'accept_message')
        self.reject_message_1 = self.config.get(
            'verification_page_ui', 'reject_message_1')
        self.reject_message_2 = self.config.get(
            'verification_page_ui', 'reject_message_2')
        self.accept_image = self.config.get(
            'verification_page_ui', 'accept_image')
        self.reject_image = self.config.get(
            'verification_page_ui', 'reject_image')
        self.fingerprint_quality_match = self.config.get(
                'verification_page_ui', 'fingerprint_quality_match')
        self.canteen_closed_message = self.config.get(
            'verification_page_ui', 'canteen_closed_message')
        self.default_message = self.config.get(
            'verification_page_ui', 'default_message')
        self.no_meal_message = self.config.get(
            'verification_page_ui', 'no_meal_message')
        self.buzzer_sound = int(self.config.get(
            'verification_page_ui', 'buzzer_sound'))
        self.database_error = self.config.get(
            'verification_page_ui', 'database_error')
        self.employee_second_swipe_message = self.config.get(
            'verification_page_ui', 'employee_second_swipe_message')
        self.device_config_message = self.config.get(
            'verification_page_ui', 'device_config_message')
        self.device_conn_message = self.config.get(
            'verification_page_ui', 'device_conn_message')
        self.device_properties_message = self.config.get(
            'verification_page_ui', 'device_properties_message')
        self.employee_second_swipe_sub = self.config.get(
            'verification_page_ui', 'employee_second_swipe_sub')
        self.next_meal_available = self.config.get(
            'verification_page_ui', 'next_meal_available')
        self.contact_hr_message = self.config.get(
            'verification_page_ui', 'contact_hr_message')
        self.contact_admin_message = self.config.get(
            'verification_page_ui', 'contact_admin_message')
        self.reconnect_error_message = self.config.get(
            'verification_page_ui', 'reconnect_error_message')
        self.employee_second_swipe_sub = self.config.get(
            'verification_page_ui', 'employee_second_swipe_sub')
        self.try_again_message = self.config.get(
            'verification_page_ui', 'try_again_message')


        self.title = self.window_title
        self.left = 10
        self.top = 10
        self.buzzer = 4
        self.buzzer_flag = True
        self.width = self.window_width
        self.height = self.window_height
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.move(550, 200)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setStyleSheet('''
        QMessageBox{background-color:white;}QMessageBox QPushButton{font:bold;width:60px;height:25px;border:none;margin-left:15px;margin-top:5px;background: transparent; border: 2px solid #0099CC;border-radius:6px;color: black;font-size:18}QPushButton:hover{background-color: #008CBA;color: white;}
        QDialog{background-color:white;}''')

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.nextFrameSlot)

        self.lab = QSpacerItem(30, 20, QSizePolicy.Expanding,
                               QSizePolicy.Fixed)

        label = QtWidgets.QLabel(self)
        label.move(200, 5)
        pixmap = QtGui.QPixmap(self.landingpage_image)
        pixmap = pixmap.scaled(280, 50)
        label.setPixmap(pixmap)

        main_layout = QVBoxLayout()
        QLabel.show(label)
        details_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 60, 10, 10)
        self.employee_detail_section()
        self.employee_detail_section_1()
        details_layout.addWidget(self.employee_details_groupbox)
        # details_layout.addItem(self.lab)
        details_layout.addWidget(self.employee_details_groupbox_1)
        # details_layout.addItem(self.lab)
        main_layout.addLayout(details_layout,1)
        self.setLayout(main_layout)
        self.center_screen()
        # self.showFullScreen()
        self.resize(648, 650)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()
        # self.openCamera()

    @pyqtSlot(QImage)
    def setImage(self, image):
        print('reaching here')
        self.label.setPixmap(QPixmap.fromImage(image))

    def employee_detail_section(self):
        self.employee_details_groupbox = QGroupBox('')
        self.employee_details_groupbox.setStyleSheet(
            "QGroupBox {font: bold;border: 2px solid #0099CC;border-radius: 6px;margin-top: 4px;}QGroupBox::title {color:#017ea8; subcontrol-origin: margin; left: 7px;bottom:5px; padding: 0px 5px 40px 5px; }")
        self.employee_details_groupbox.setFont(
            QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        layout = QVBoxLayout()
        # self.employee_details_groupbox.setAlignment(Qt.AlignCenter)
        # self.lab = QSpacerItem(30, 20, QSizePolicy.Expanding,
        #                        QSizePolicy.Fixed)

        # self.space = QSpacerItem(30, 20, QSizePolicy.Expanding,
        #                        QSizePolicy.Fixed)

        self.label = QLabel()
        self.label.setFixedSize(600, 400)
        
        layout.addWidget(self.label)
        # layout.addStretch(1)
        self.employee_details_groupbox.setLayout(layout)
    
    def employee_detail_section_1(self):
        self.employee_details_groupbox_1 = QGroupBox('Message')
        self.employee_details_groupbox_1.setStyleSheet(
            "QGroupBox {font: bold;border: 2px solid #0099CC;border-radius: 6px;margin-top: 4px;}QGroupBox::title {color:#017ea8; subcontrol-origin: margin; left: 7px;bottom:5px; padding: 0px 5px 40px 5px; }")
        self.employee_details_groupbox_1.setFont(
            QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        layout = QHBoxLayout()
        self.employee_details_groupbox_1.setAlignment(Qt.AlignCenter)
        self.lab = QSpacerItem(30, 20, QSizePolicy.Expanding,
                               QSizePolicy.Fixed)

        self.space = QSpacerItem(30, 20, QSizePolicy.Expanding,
                               QSizePolicy.Fixed)
        
        self.label_1 = QtWidgets.QLabel(self)
        self.status = QtWidgets.QLabel("          "+self.default_message)
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

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    @QtCore.pyqtSlot(str, int)
    def handle_status(self, data, status):
        if(status == 4):
             msg = "\t"+self.fingerprint_quality_match+"\n\t          "+self.try_again_message
             self.status.setText(msg)
             self.status.setStyleSheet("QLabel{color: red}")
             QTimer.singleShot(3000, self.reset_screen)
             
        elif(status == 111):
             self.reset_screen()
             
        elif(status == 666):
            data = data.split(',')
            if len(data[2]) <15:
                msg = ("      "+self.employee_second_swipe_message+"\n\t"+self.employee_second_swipe_sub).format(data[0].lower(),data[1],data[2].lower())
            else:
                msg = ("      "+self.employee_second_swipe_message+"\n      "+self.employee_second_swipe_sub).format(data[0].lower(),data[1],data[2].lower())
            self.handle_error(data,status,msg)
            
        elif(status == 0):
            msg = "      "+self.reject_message_1+"\n          "+self.reject_message_2
            self.handle_error(data,status,msg)

        elif(status == 9):
             self.status.setText("    "+self.device_conn_message+"\n    "+self.reconnect_error_message)
             self.status.setStyleSheet("QLabel{color: red}")
                
        elif(status == 8):
             self.status.setText("        "+self.device_config_message+"\n\t  "+self.contact_admin_message)
             self.status.setStyleSheet("QLabel{color: red}")
        
        elif(status == 6):
             self.status.setText("    "+self.database_error+"\n\t"+self.contact_admin_message)
             self.status.setStyleSheet("QLabel{color: red}")
             QTimer.singleShot(self.blink_threshold, self.reset_screen)
             
        elif(status == 2):
             data=data.split(',')
             if len(data[0]) >7:
                 msg = "\t        "+self.canteen_closed_message+"\n   "+self.next_meal_available.format(data[0].lower(),data[1])
             else:
                 msg = "\t        "+self.canteen_closed_message+"\n       "+self.next_meal_available.format(data[0].lower(),data[1])
             self.status.setText(msg)
             self.status.setStyleSheet("QLabel{color: red}")
             QTimer.singleShot(3000, self.reset_screen)
             
        elif(status == 3):
             self.status.setText("\t"+self.no_meal_message)
             self.status.setStyleSheet("QLabel{color: red}")
             QTimer.singleShot(3000, self.reset_screen)
             
        else:
            self.call_blink(data,status)
            QTimer.singleShot(self.blink_threshold, lambda:self.clear(status))
   
    def call_blink(self,data,status):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda:self.blink(data,status))
        self.timer.start(300)
        self.index = 1
        
    def handle_error(self,data,status,msg):
        self.index = 1
        self.status.setText(msg)
        self.status.setStyleSheet("QLabel{color: red}")
        QTimer.singleShot(7000, self.reset_screen)
        
        #Uncomment the below code to allow beeping for error codes#
        ###########################################################
        
        QTimer.singleShot(2000, self.stop_beep)
        self.timer = QTimer()
        self.timer.timeout.connect(lambda:self.beep(data,status))
        self.timer.start(300)
       
        
    def beep(self,data,status):
        if(self.index %2 ==0):
            if(self.buzzer_flag and self.buzzer_sound == 1):
                return
        else:
            if(self.buzzer_sound == 1):
                return
        self.index += 1
               
    def blink(self,data,status):
        if(self.index %2 ==0):
            if(status == 1):
                self.pixmap = QtGui.QPixmap(self.accept_image)
                self.status.setText(self.accept_message.format(data))
                self.status.setStyleSheet("QLabel{color: green}")
                if(self.buzzer_flag and self.buzzer_sound == 1):
                    self.buzzer_flag = False
                         
                    
            elif(status == 0):
                self.pixmap = QtGui.QPixmap(self.reject_image)
                self.status.setText(self.reject_message)
                self.status.setStyleSheet("QLabel{color: red}")
                if(self.buzzer_flag and self.buzzer_sound == 1):
                    return
                    
            elif(status == 666):
                if(self.buzzer_flag and self.buzzer_sound == 1):
                    return 
                    
            elif(status == 777):
                self.pixmap = QtGui.QPixmap(self.reject_image)
                self.status.setText(self.employee_validation_active_message+"\n\t"+self.contact_hr_message)
                self.status.setStyleSheet("QLabel{color: red}")
                if(self.buzzer_flag and self.buzzer_sound == 1):
                    return
            
        else:
            self.pixmap = QtGui.QPixmap('')
            self.status.setText('')
            if(self.buzzer_sound == 1):
                return

        self.pixmap = self.pixmap.scaled(200, 200)
        self.label.setPixmap(self.pixmap)
        self.index += 1
        
    def reset_screen(self):
        self.verify.is_start = True
        self.verify.resume()
        self.status.setText("          "+self.default_message)
        self.status.setStyleSheet("QLabel{color: purple}")
        
    def stop_beep(self):
        self.timer.stop()
        if(self.buzzer_sound == 1):
            self.buzzer_flag = True
            
    def clear(self,status):
        if(status == 6 or status == 666):
            self.reset_screen()
        if(status == 1 or status == 0 or status == 777): 
            self.timer.stop()
            self.pixmap = QtGui.QPixmap('')
            self.pixmap = self.pixmap.scaled(200, 200)
            self.label.setPixmap(self.pixmap)
            self.reset_screen()
        if(self.buzzer_sound == 1):
            self.buzzer_flag = True

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
