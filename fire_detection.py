#for voice
import cv2
import numpy as np
import torch
import datetime
import csv
import os
import pygame
from ultralytics import YOLO

# Load YOLO model
model = YOLO("fire_best.pt")

# Initialize pygame mixer
pygame.mixer.init()

# Load the fire alert sound
fire_alert_sound = pygame.mixer.Sound("Fire_alert.mp3")

def fire_detection1(frame, camera_name, room_name):
    # Perform object detection
    results = model(frame)
    result = results[0]

    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = round(box.conf[0].item(), 2)
        print("Object type:", class_id)
        print("Coordinates:", cords)
        print("Probability:", conf)
        print("---")
        if conf > 0.35:
            # Fire detected, take appropriate action
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            date = timestamp.split('_')[0]
            save_folder = os.path.join('detected_fires', date)
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, f"{camera_name}_{timestamp}.jpg")  # Added .jpg file extension
            # Draw bounding box
            xmin, ymin, xmax, ymax = cords
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
            # Add text label with confidence score
            label = f"{class_id}: {conf}"
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
            cv2.imwrite(save_path, frame)
            
            # Logging into CSV file
            with open('detection_logs.csv', 'a', newline='') as csvfile:
                fieldnames = ['Timestamp', 'Camera Name', 'Room Name', 'Video Link','Event Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writerow({'Timestamp': timestamp, 'Camera Name': camera_name, 'Room Name': room_name, 'Video Link': save_path})
                
            # Play the fire alert sound
            fire_alert_sound.play()
            
    return frame




#working code



# import cv2
# import numpy as np
# import torch
# import datetime
# import csv
# import os
# #from ultralytics.yolo.engine.model import YOLO
# from ultralytics import YOLO

# # Load YOLO model
# model = YOLO("fire_best.pt")


# def fire_detection1(frame, camera_name, room_name):
#     # Perform object detection
#     results = model(frame)
# # Perform object detection
#     results = model.predict(frame)
#     print(results)
#     result=results[0]
#     #frame_with_boxes = frame.copy()  # Make a copy of the frame to draw boxes on

# # print(result[0])
#     for box in result.boxes:
#         class_id = result.names[box.cls[0].item()]
#         cords = box.xyxy[0].tolist()
#         cords = [round(x) for x in cords]
#         conf = round(box.conf[0].item(), 2)
#         print("Object type:", class_id)
#         print("Coordinates:", cords)
#         print("Probability:", conf)
#         print("---")
#         if conf > 0.35:
#             # Fire detected, take appropriate action
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             date = timestamp.split('_')[0]
#             save_folder = os.path.join('detected_fires', date)
#             os.makedirs(save_folder, exist_ok=True)
#             save_path = os.path.join(save_folder, f"{camera_name}_{timestamp}.jpg")  # Added .jpg file extension
#             # Draw bounding box
#             xmin, ymin, xmax, ymax = cords
#             cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
#             # Add text label with confidence score
#             label = f"{class_id}: {conf}"
#             cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
#             cv2.imwrite(save_path, frame)
            
#             # Logging into CSV file
#             with open('detection_logs.csv', 'a', newline='') as csvfile:
#                 fieldnames = ['Timestamp', 'Camera Name', 'Room Name', 'Video Link','Event Type']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
#                 writer.writerow({'Timestamp': timestamp, 'Camera Name': camera_name, 'Room Name': room_name, 'Video Link': save_path})
                
#     return frame



#twilio


# import cv2
# import numpy as np
# import torch
# import datetime
# import csv
# import os
# from twilio.rest import Client
# from ultralytics import YOLO

# # Twilio credentials
# account_sid = 'AC0fa70e7639a40e71c7e3c6a894578148'
# auth_token = '15eeb878741f9e32e9332599f61ef5bb'
# twilio_number = '+15752135806'
# recipient_number = '+919581448192'

# # Initialize Twilio client
# client = Client(account_sid, auth_token)

# # Load YOLO model
# model = YOLO("fire_best.pt")


# def send_sms(message):
#     # Send SMS using Twilio
#     client.messages.create(
#         body=message,
#         from_=twilio_number,
#         to=recipient_number
#     )


# def fire_detection1(frame, camera_name, room_name):
#     # Perform object detection
#     results = model.predict(frame)
#     result = results[0]

#     for box in result.boxes:
#         class_id = result.names[box.cls[0].item()]
#         cords = box.xyxy[0].tolist()
#         cords = [round(x) for x in cords]
#         conf = round(box.conf[0].item(), 2)

#         if conf > 0.35 and class_id == 'fire':
#             # Fire detected, take appropriate action
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             date = timestamp.split('_')[0]
#             save_folder = os.path.join('detected_fires', date)
#             os.makedirs(save_folder, exist_ok=True)
#             save_path = os.path.join(save_folder, f"{camera_name}_{timestamp}.jpg")

#             # Draw bounding box
#             xmin, ymin, xmax, ymax = cords
#             cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

#             # Add text label with confidence score
#             label = f"{class_id}: {conf}"
#             cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             cv2.imwrite(save_path, frame)

#             # Logging into CSV file
#             with open('detection_logs.csv', 'a', newline='') as csvfile:
#                 fieldnames = ['Timestamp', 'Camera Name', 'Room Name', 'Video Link']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 writer.writerow({'Timestamp': timestamp, 'Camera Name': camera_name, 'Room Name': room_name,
#                                  'Video Link': save_path})

#             # Send SMS notification
#             message = f"Fire detected in {room_name} at {timestamp}"
#             send_sms(message)

#     return frame
