from VideoGet import VideoGet
from VideoShow import VideoShow
import face_recognition
import cv2
import numpy as np
import math
import pickle
from pathlib import Path
import rfid

encodings_location = Path("output/encodings.isiot")

def face_confidence(face_distance, face_match_threshold=0.6):
    '''
    This function is made to calculate the confidence of face recognition
    '''
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

def main(source=0):
    face_locations = []
    face_encodings = []
    face_names = []
    process_current_frame = True
    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        # Only process every other frame of video to save time
        if process_current_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            with encodings_location.open(mode="rb") as f:
                loaded_encodings = pickle.load(f)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(loaded_encodings["encodings"], face_encoding)
                name = "Unknown"
                confidence = '???'

                # Calculate the shortest distance to face
                face_distances = face_recognition.face_distance(loaded_encodings["encodings"], face_encoding)

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = loaded_encodings["names"][best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

                face_names.append(f'{name} ({confidence})')

        process_current_frame = not process_current_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Create the frame with the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        video_shower.frame = frame
        rfid.main()

if __name__ == "__main__":
    main(source=0)