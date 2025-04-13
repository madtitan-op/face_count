import face_recognition
import cv2
import csv
import ast
import numpy as np
from reader import reader


def cam_read():
    rows = reader.csv_read()
    
        

        # Initialize webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if ret:
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find faces and their encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            # print(face_locations)

            # Draw rectangles around the faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            count = False
            # Ensure there is at least one face encoding from the known image and the current frame
            for j in range(len(rows)):
                row = rows[j]
                known_image_encode = row['face_encodings']
                # print(face_encodings)
                if len(known_image_encode) > 0 and len(face_encodings) > 0:
                    
                    
                    known_face_encode = known_image_encode  # direct geting numpy array 
                    unknown_face_encode = face_encodings[0]  # First face encoding from the current frame, here we list of np array that why we have to use 0 

                    # Compare the known face encoding with the unknown face encoding
                    result = face_recognition.compare_faces([known_face_encode], unknown_face_encode, tolerance=0.4)

                    # Display matching result
                    # print(result)
                    if result[0]:
                        cv2.putText(frame, f"{row['name']}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        count = True
                        return row['roll']
        
            if not count and len(face_locations) > 0:
                cv2.putText(frame, "Not Matched", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)   

            
            # Show the frame with the face recognition result
            cv2.imshow("Face Recognition", frame)
            
            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the video capture object and close all OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

    



# # for unknown image
# image_path = r'images/srk.png'
# u_image = face_recognition.load_image_file(image_path)
# u_image_location = face_recognition.face_locations(u_image)
# u_image_encode = face_recognition.face_encodings(u_image)



# if len(known_image_encode)>0 and len(u_image_encode)>0:

#     known_encode = known_image_encode[0]
#     unknown_encode = u_image_encode[0]

#     result = face_recognition.compare_faces([known_encode],unknown_encode,0.6)

#     if result[0]:
#         print("data matched")
    
#     else:
#         print("data not matched")

# else:
#     print("No face found in one or both face")