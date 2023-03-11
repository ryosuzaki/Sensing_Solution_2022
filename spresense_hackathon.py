# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:05:16 2022

@author: ryo suzaki
"""

import cv2
import mediapipe as mp
from PIL import Image
import numpy as np
import serial
import time
#メモリ使用量測定
#from memory_profiler import profile


def detect_color(img,posx,posy):
    B,G,R=img[int(posy[8]*2-posy[7]),int(posx[8]*2-posx[7]),:]
    if B>=G and B>=R:
        return "B"
    elif G>=B and G>=R:
        return "G"
    else:
        return "R"

#@profile
def detect_finger():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    
    counter=0
    img_num=128
    with serial.Serial('COM3',115200) as ser:
        #setupが済むまで待つ
        while ser.readline().rstrip().decode('utf-8') != "setup completed":
            continue
        
        with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.5) as hands:
            
            while True:
                time_sta1 = time.time()
                
                img_path="D:input_images/"+str(counter)+".jpg"
                print(img_path)
                #img_num枚分間隔を持たせる
                counter=(counter+1)%img_num
                
                time_sta2 = time.time()
                while cv2.imread(img_path) is None:
                    continue
                time_end2 = time.time()
                
                img = cv2.imread(img_path)
    
                img_height, img_width, _ = img.shape
                # Convert the BGR image to RGB before processing.
                results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
                time_end1 = time.time()
                total_time1=time_end1- time_sta1
                total_time2=time_end2- time_sta2
                
                if results.multi_hand_landmarks is not None:
                    #print("detected")
                    landmarks=results.multi_hand_landmarks[0].landmark
                    pred_x=[landmark.x*img_width for landmark in landmarks]
                    pred_y=[landmark.y*img_height for landmark in landmarks]
                    ser.write(b"detected,"+(str(pred_x[8])+","+str(pred_y[8])+","+detect_color(img,pred_x,pred_y)).encode('utf-8'))
                    
                    print("全体処理時間："+str(total_time1))
                    print("画像読み込み処理時間："+str(total_time2))
                    print("AI推論時間："+str(total_time1-total_time2))
                else:
                    ser.write(b"not detected")
                #print(ser.readline().rstrip().decode('utf-8'))
                #print(ser.readline().rstrip().decode('utf-8'))
                
     
detect_finger()
                                