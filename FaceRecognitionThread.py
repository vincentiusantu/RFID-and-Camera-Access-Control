import face_recognition
import cv2
import numpy as np
import pickle
from pathlib import Path
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
from videoThread import VideoThread


encodings_location = Path("output/encodings.isiot")

class FaceRecognition(QThread):
    face_locations = []
    face_encodings = []
    face_names = []
    process_current_frame = True
    change_name_signal = pyqtSignal(str)
    change_status_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.run_recognition)
        self.thread.start()
        self.stopped = False

    @pyqtSlot(np.ndarray)
    def run_recognition(self, cv_img):
        name = "Unknown"
        status = "Denied"
        # Only process every other frame of video to save time
        while not self.stopped:
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

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = loaded_encodings["names"][best_match_index]
                    else:
                        name = "Unknown"
                        
                    if name == 'Unknown':
                        status = 'Denied'
                    else:
                        status = 'Granted'
                    
                    self.change_name_signal.emit(name)
                    self.change_status_signal.emit(status)
            self.process_current_frame = not self.process_current_frame
                    


    def stop(self):
        self.stopped = True
        self.thread.stop()
        self.wait()