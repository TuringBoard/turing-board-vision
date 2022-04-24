# Author: Sahaj Amatya

import cv2
import cv2.aruco as aruco
import numpy as np
import os
# import pyrealsense2
import sys
from realsense_depth import *

sys.path.insert(0, '../../turing-board-controls/src/Communication')

from uart0Communication import *
from communicate import SerialCommunication
'''
[[ 14.   7.]
 [ 94.   7.]
 [100.  83.]
 [ 20.  84.]]
'''


def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(
        imgGray, arucoDict, parameters=arucoParam)
    # Corners: [top right, bottom right, bottim left, top left]
    return corners, ids


class FollowMe:
    def __init__(self, serial_port='/dev/ttyACM1'):
        self.turningMechanism = SerialCommunication(port=serial_port, baudrate=115200)
        self.dc = DepthCamera()
        # cap = cv2.VideoCapture(3)
        # This file should really be passed in as an argument to the class parameters
        self.camera_matrix = np.loadtxt("cameraMatrix_webcam.txt", delimiter=',')
        self.camera_distortion = np.loadtxt(
            "cameraDistortion_webcam.txt", delimiter=',')
        self.key = None

        # from uart0comms.py
        self.previous = 50
        self.prevMode = 3
        
    def follow_me(self, move_callback, duty_cycle, distance_until_follow_me_on):
        ret, depth_frame, color_frame = self.dc.get_frame()

        img = color_frame
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids = findArucoMarkers(img)


        # Intel Realsense Resolution: 1920x1080
        # MBP FaceTime camera Resolution: 1280x720
        deadZoneWidth = 150
        rectX = int((640/2)-(deadZoneWidth/2))
        rectY = int((480/2)-(deadZoneWidth/2))
        rectW = int(rectX + deadZoneWidth)
        rectH = int(rectY + deadZoneWidth)
        cv2.rectangle(imgGray, (rectX, 0),
                      (rectW, 480), (255, 255, 255), 2)

        if len(corners) > 0:
            ret = aruco.estimatePoseSingleMarkers(
                corners, 6, self.camera_matrix, self.camera_distortion)
            rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]
            
            storage = []
            distance = 0

            # drawing white frame around detected markers
            for corner in corners:
                corners = corner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners

                width = int(abs(topRight[0] - topLeft[0]))
                height = int(abs(bottomLeft[1]-topLeft[1]))
                x_mid = int(topLeft[0] + (width/2))
                y_mid = int(topLeft[1] + (height/2))
                # print(topLeft[1], width)
                for i in range(int(topLeft[0]+(width/4)), int(topRight[0]-(width/4))):
                    for j in range(int(topLeft[1]+(height/4)), int(bottomLeft[1]-(height/4))):
                        distance = depth_frame[j, i]
                        if distance > 0: 
                            storage.append(distance)
                # print(storage)
                cv2.circle(img, (x_mid, y_mid), 10, (0,0,255))
                cv2.circle(imgGray, (x_mid, y_mid), 4, (0,0,255))
                cv2.line(imgGray, (x_mid, 0), (x_mid, 480), (255,255,255), 1)
                cv2.line(imgGray, (0, y_mid), (640, y_mid), (255,255,255), 1)
                cv2.putText(imgGray, 'Optimized Distance: {}mm'.format(distance), (450, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                cv2.line(img, topLeft, topRight, (0, 255, 0), 4)
                cv2.line(img, topRight, bottomRight, (0, 255, 0), 4)
                cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 4)
                cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 4)

                cv2.line(imgGray, topLeft, topRight, (255, 255, 255), 4)
                cv2.line(imgGray, topRight, bottomRight, (255, 255, 255), 4)
                cv2.line(imgGray, bottomRight, bottomLeft, (255, 255, 255), 4)
                cv2.line(imgGray, bottomLeft, topLeft, (255, 255, 255), 4)
                    
                # aruco.drawAxis(img, self.camera_matrix,
                #                self.camera_distortion, rvec, tvec, 10)
            
            if len(storage) > 0: 
                distance = int(min(storage)) + 10
            else: 
                distance = 0
                       
            if distance > distance_until_follow_me_on:
                move_callback(-duty_cycle)
                cv2.putText(imgGray, 'MOVE FORWARD'.format(distance), (450, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                if x_mid < rectX:
                    cv2.putText(imgGray, f'KEEP LEFT', (450, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), )
                    self.updateAngle(20)

                elif x_mid > (rectX+deadZoneWidth):
                    cv2.putText(imgGray, f'KEEP RIGHT', (450, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    self.updateAngle(80)

                else: 
                    self.updateAngle(50)

            else:
                move_callback(0)
                cv2.putText(imgGray, 'STOPPED'.format(distance), (450, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # Controls the turning mechanism
            

    
        # if len(corners) <= 0:
        #     move_callback(0)
        # cv2.putText(imgGray, f'TODO: DEPTH CALCULATION FOR FORWARD PROPULSION',
        #             (900, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # cv2.namedWindow("BGR", cv2.WINDOW_NORMAL)
        cv2.namedWindow("arUco", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('BGR', 640, 480)
        cv2.resizeWindow('arUco', 640, 480)
        cv2.imshow("arUco", imgGray)
        self.key = cv2.waitKey(1)

    def close_follow_me(self):
        cv2.destroyAllWindows()

    def updateAngle(self, angle1): 
        # print("update command sent", angle1)

        data = []
        data.append(1 & 0xFF)  
        data.append(int(angle1) & 0xFF)
        direction = 2
        if angle1 > 50:
            direction = 1
        elif angle1 < 50: 
            direction = 0
        if angle1 == 50: 
            direction = 2
        data.append(int(direction) & 0xFF)
        rate = 0
        data.append(int(rate) & 0xFF)
        if angle1 != self.previous:
            # print("data:",data)
            toSend = bytearray(data)
            # print("bytearray:", toSend)
            self.turningMechanism.push(toSend)
            # print("b4", toSend)
            self.turningMechanism.send()
            # print("after")
        self.previous = angle1

"""
                # cv2.putText(imgGray, 'Unoptimized Distance: {}mm'.format(depth_frame[y_mid, x_mid]), (450, 140),
                #                     cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
                # if True:
                    # Controls the duty cycle of the wheels.
                    # If the distance happens to be greater the given distance, move the wheels forward,
                    # otherwise, stop!

                if distance > distance_until_follow_me_on:
                    move_callback(-duty_cycle)
                    cv2.putText(imgGray, 'MOVE FORWARD'.format(distance), (450, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    move_callback(0)
                    cv2.putText(imgGray, 'STOPPED'.format(distance), (450, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    printName("import successful")
                    updateAngle(20)
                    
                # Controls the turning mechanism
                if x_mid < rectX:
                    cv2.putText(imgGray, f'KEEP LEFT', (450, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), )
                    
                elif x_mid > (rectX+deadZoneWidth):
                    cv2.putText(imgGray, f'KEEP RIGHT', (450, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
"""