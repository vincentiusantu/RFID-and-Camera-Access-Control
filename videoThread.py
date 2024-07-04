import cv2
from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import face_recognition
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import time

encodings_location = Path("output/encodings.isiot")


class VideoThread(QThread):
    face_locations = []
    face_encodings = []
    face_names = []
    process_current_frame = True
    
    # Initialize for emit the signal
    change_name_signal = pyqtSignal(str)
    change_status_signal = pyqtSignal(str)
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        
        # Default value
        name = "Unknown"
        status = "Denied"
        cv_img = plt.imread("default.jpg")
        
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                    small_frame = cv2.resize(cv_img, (0, 0), fx=0.25, fy=0.25)
                    with encodings_location.open(mode="rb") as f:
                        loaded_encodings = pickle.load(f)

                    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                    rgb_small_frame = small_frame[:, :, ::-1]

                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(loaded_encodings["encodings"], face_encoding)
                        name = "Unknown"

                        # Calculate the shortest distance to face
                        face_distances = face_recognition.face_distance(loaded_encodings["encodings"], face_encoding)

                        # Finding the name based on encoded face data
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = loaded_encodings["names"][best_match_index]
                        else:
                            name = "Unknown"
                    if name == 'Unknown':
                        status = 'Denied'
                        cv_img = plt.imread("default.jpg")
                        self.change_name_signal.emit(name)
                        self.change_status_signal.emit(status)
                        self.change_pixmap_signal.emit(cv_img)
                    else:
                        status = 'Granted'
                        self.change_name_signal.emit(name)
                        self.change_status_signal.emit(status)
                        self.change_pixmap_signal.emit(cv_img)
                        time.sleep(5)
                    
                self.process_current_frame = not self.process_current_frame
                name = "Unknown"
                status = "Denied"
                cv_img = plt.imread("default.jpg")
            else:
                self.change_name_signal.emit(name)
                self.change_status_signal.emit(status)
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()