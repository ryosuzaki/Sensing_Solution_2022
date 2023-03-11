# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 08:46:56 2022

@author: n1201023
"""

import cv2
import mediapipe as mp
from PIL import Image
import numpy as np
import serial

img_path = "D:/input_image.jpg"
out_path="C:/"

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

yubisaki=[]

def detect_color(posx,posy):
    B,G,R=image[int(posy[8]*2-posy[7]),int(posx[8]*2-posx[7]),:]
    if B>=G & B>=R:
        return "blue"
    elif G>=B & G>=R:
        return "green"
    else:
        return "red"

ser = serial.Serial('COM3',115200)
#ser.readline();
while(True):
    #val=ser.readline();
    val = int(repr(val.decode())[1:-5])
    line = ser.readline()
    line = line.rstrip().decode('utf-8')
    print(line)
    if val>=0:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5) as hands:
            
            img_path = "D:/input_images/"+str(val)+".jpg"
            print(img_path)
            #USBMSCで画像にアクセス
            image = cv2.imread(img_path)
            while image is None:
                image = cv2.imread(img_path)
            print("read")
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks is not None:
                landmarks=results.multi_hand_landmarks[0].landmark
                print("landmarks")
                posx=[landmark.x*image_width for landmark in landmarks]
                posy=[landmark.y*image_height for landmark in landmarks]
                ser.write(bytes([1]))
                ser.write(bytes([int(posx[8])]))
                ser.write(bytes([int(posy[8])]))
                print(1)
            else:
                ser.write(bytes([0]))
                print(0)

            
            
        
    
