from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
from videoThread import VideoThread
from FaceRecognitionThread import FaceRecognition


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')
        self.nameLabel = QLabel('Name: Unknown')
        self.statusLabel = QLabel('Status: Denied')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.statusLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        
        self.faceRecognition = FaceRecognition()
        self.faceRecognition.change_name_signal.connect(self.update_name)
        self.faceRecognition.change_status_signal.connect(self.update_status)
        # self.faceRecognition.thread.change_pixmap_signal.connect(self.update_image)
        self.faceRecognition.start()

    def closeEvent(self, event):
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