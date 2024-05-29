#voice


import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the unauthorized alert sound
unauthorized_alert_sound = pygame.mixer.Sound("Unauthorized_alert.mp3")

# Define the path to images for attendance
path_to_images = "ImageAttendence"
images = []
classNames = []
myList = os.listdir(path_to_images)
for cl in myList:
    curImg = cv2.imread(f'{path_to_images}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def find_encodings(images):
    """Find encodings for a list of images."""
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def mark_attendance(name, authorized=True):
    """Mark attendance for a recognized face."""
    log_message = f'{name} in at {datetime.now().strftime("%H:%M:%S")}'
    if not authorized:
        log_message = f'UNAUTHORIZED: {log_message}'
        # Play the unauthorized alert sound
        unauthorized_alert_sound.play()
    
    with open('attendance.csv', 'a') as f:
        f.write(f'{log_message}\n')

    print(log_message)

encodelist_known = find_encodings(images)
print('Encoding complete')

def face_attendance(frame):
    """Function to process a frame and mark attendance."""
    # Resize frame and convert to RGB
    small_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    # Find face locations and encodings in the current frame
    faces_current_frame = face_recognition.face_locations(rgb_frame)
    encodes_current_frame = face_recognition.face_encodings(rgb_frame, faces_current_frame)
    
    # Iterate through each face found in the frame
    for encode_face, faceloc in zip(encodes_current_frame, faces_current_frame):
        # Compare current face encodings with known encodings
        matches = face_recognition.compare_faces(encodelist_known, encode_face)
        face_dis = face_recognition.face_distance(encodelist_known, encode_face)
        match_index = np.argmin(face_dis)
        
        # If a match is found
        if matches[match_index]:
            name = classNames[match_index].upper()
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # Draw a green rectangle and text around the recognized face
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1 - 35), (x2, y2), (0, 255, 0), 1)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # Mark attendance for the recognized face (authorized entry)
            mark_attendance(name, authorized=True)
        else:
            # If the face is not recognized, mark as unauthorized
            unauthorized_name = "UNAUTHORIZED"
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # Draw a red rectangle and text around the unrecognized face
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y1 - 35), (x2, y2), (0, 0, 255), 1)
            cv2.putText(frame, unauthorized_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # Mark attendance for the unrecognized face (unauthorized entry)
            mark_attendance(unauthorized_name, authorized=False)
    
    return frame





# working code


# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime

# # Define the path to images for attendance
# path_to_images = "ImageAttendence"
# images = []
# classNames = []
# myList = os.listdir(path_to_images)
# for cl in myList:
#     curImg = cv2.imread(f'{path_to_images}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])

# def find_encodings(images):
#     """Find encodings for a list of images."""
#     encodelist = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodelist.append(encode)
#     return encodelist

# def mark_attendance(name, authorized=True):
#     """Mark attendance for a recognized face."""
#     log_message = f'{name} in at {datetime.now().strftime("%H:%M:%S")}'
#     if not authorized:
#         log_message = f'UNAUTHORIZED: {log_message}'
    
#     with open('attendance.csv', 'a') as f:
#         f.write(f'{log_message}\n')

#     print(log_message)

# encodelist_known = find_encodings(images)
# print('Encoding complete')

# def face_attendance(frame):
#     """Function to process a frame and mark attendance."""
#     # Resize frame and convert to RGB
#     small_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
#     rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
#     # Find face locations and encodings in the current frame
#     faces_current_frame = face_recognition.face_locations(rgb_frame)
#     encodes_current_frame = face_recognition.face_encodings(rgb_frame, faces_current_frame)
    
#     # Iterate through each face found in the frame
#     for encode_face, faceloc in zip(encodes_current_frame, faces_current_frame):
#         # Compare current face encodings with known encodings
#         matches = face_recognition.compare_faces(encodelist_known, encode_face)
#         face_dis = face_recognition.face_distance(encodelist_known, encode_face)
#         match_index = np.argmin(face_dis)
        
#         # If a match is found
#         if matches[match_index]:
#             name = classNames[match_index].upper()
#             y1, x2, y2, x1 = faceloc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             # Draw a green rectangle and text around the recognized face
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(frame, (x1, y1 - 35), (x2, y2), (0, 255, 0), 1)
#             cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#             # Mark attendance for the recognized face (authorized entry)
#             mark_attendance(name, authorized=True)
#         else:
#             # If the face is not recognized, mark as unauthorized
#             unauthorized_name = "UNAUTHORIZED"
#             y1, x2, y2, x1 = faceloc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             # Draw a red rectangle and text around the unrecognized face
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#             cv2.rectangle(frame, (x1, y1 - 35), (x2, y2), (0, 0, 255), 1)
#             cv2.putText(frame, unauthorized_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#             # Mark attendance for the unrecognized face (unauthorized entry)
#             mark_attendance(unauthorized_name, authorized=False)
    
#     return frame


#twilio


# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime
# from twilio.rest import Client

# # Twilio credentials
# account_sid = 'AC0fa70e7639a40e71c7e3c6a894578148'
# auth_token = '15eeb878741f9e32e9332599f61ef5bb'
# twilio_phone_number = '+15752135806'
# recipient_number = '+919581448192'

# # Initialize Twilio client
# client = Client(account_sid, auth_token)

# # Define the path to images for attendance
# path_to_images = "ImageAttendence"
# images = []
# classNames = []
# myList = os.listdir(path_to_images)
# for cl in myList:
#     curImg = cv2.imread(f'{path_to_images}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])

# def find_encodings(images):
#     """Find encodings for a list of images."""
#     encodelist = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodelist.append(encode)
#     return encodelist

# def mark_attendance(name, authorized=True):
#     """Mark attendance for a recognized face."""
#     log_message = f'{name} in at {datetime.now().strftime("%H:%M:%S")}'
#     if not authorized:
#         log_message = f'UNAUTHORIZED: {log_message}'
    
#     with open('attendance.csv', 'a') as f:
#         f.write(f'{log_message}\n')

#     print(log_message)

#     # Send message if unauthorized
#     if not authorized:
#         client.messages.create(
#             to=recipient_number,
#             from_=twilio_phone_number,
#             body=f'UNAUTHORIZED PERSON DETECTED: {name} entered at {datetime.now().strftime("%H:%M:%S")}'
#         )

# encodelist_known = find_encodings(images)
# print('Encoding complete')

# def face_attendance(frame):
#     """Function to process a frame and mark attendance."""
#     # Resize frame and convert to RGB
#     small_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
#     rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
#     # Find face locations and encodings in the current frame
#     faces_current_frame = face_recognition.face_locations(rgb_frame)
#     encodes_current_frame = face_recognition.face_encodings(rgb_frame, faces_current_frame)
    
#     # Iterate through each face found in the frame
#     for encode_face, faceloc in zip(encodes_current_frame, faces_current_frame):
#         # Compare current face encodings with known encodings
#         matches = face_recognition.compare_faces(encodelist_known, encode_face)
#         face_dis = face_recognition.face_distance(encodelist_known, encode_face)
#         match_index = np.argmin(face_dis)
        
#         # If a match is found
#         if matches[match_index]:
#             name = classNames[match_index].upper()
#             y1, x2, y2, x1 = faceloc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             # Draw a green rectangle and text around the recognized face
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(frame, (x1, y1 - 35), (x2, y2), (0, 255, 0), 1)
#             cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#             # Mark attendance for the recognized face (authorized entry)
#             mark_attendance(name, authorized=True)
#         else:
#             # If the face is not recognized, mark as unauthorized
#             unauthorized_name = "UNAUTHORIZED"
#             y1, x2, y2, x1 = faceloc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             # Draw a red rectangle and text around the unrecognized face
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#             cv2.rectangle(frame, (x1, y1 - 35), (x2, y2), (0, 0, 255), 1)
#             cv2.putText(frame, unauthorized_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#             # Mark attendance for the unrecognized face (unauthorized entry)
#             mark_attendance(unauthorized_name, authorized=False)
    
#     return frame

