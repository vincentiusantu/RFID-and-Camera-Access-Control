from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
from videoThread import VideoThread


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 480
        self.display_height = 360
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # Set default picture for unknown faces
        self.image_label.setPixmap(QPixmap("default.jpg"))
        # create a text label
        self.textLabel = QLabel('Webcam')
        self.nameLabel = QLabel('Name: Unknown')
        self.statusLabel = QLabel('Status: Denied')

        # create a vertical box layout and add the three labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.image_label)
        
        # create a horizontal box layout and add vertical layout and status label
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.statusLabel)
        self.setLayout(hbox)
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.change_name_signal.connect(self.update_name)
        self.thread.change_status_signal.connect(self.update_status)
        # start the thread
        self.thread.start()
        

    def closeEvent(self, event):
        '''
        This function is used for handling exit button. So when the button clicked, the program will be stopped immediately
        '''
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        
    @pyqtSlot(str)
    def update_name(self, name):
        """Updates the nameLabel with the recognized name"""
        self.nameLabel.setText(f'Name: {name}')
        
    @pyqtSlot(str)
    def update_status(self, status):
        """Updates the statusLabel with the recognition status"""
        self.statusLabel.setText(f'Status: {status}')
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())