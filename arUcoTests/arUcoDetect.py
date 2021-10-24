import cv2
import cv2.aruco as aruco
import numpy as np
import os


def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(
        imgGray, arucoDict, parameters=arucoParam)
    # Corners: [top right, bottom right, bottim left, top left]
    return corners, ids


'''
[[ 14.   7.]
 [ 94.   7.]
 [100.  83.]
 [ 20.  84.]] 
'''


def main():
    cap = cv2.VideoCapture(2)
    camera_matrix = np.loadtxt("cameraMatrix_webcam.txt", delimiter=',')
    camera_distortion = np.loadtxt(
        "cameraDistortion_webcam.txt", delimiter=',')

    while True:
        _, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids = findArucoMarkers(img)

        rectX = int((1280/2)-100)
        rectY = int((720/2)-100)
        rectW = int(rectX + 200)
        rectH = int(rectY + 200)
        cv2.rectangle(imgGray, (rectX, rectY),
                      (rectW, rectH), (255, 255, 255), 2)

        if len(corners) > 0:
            ret = aruco.estimatePoseSingleMarkers(
                corners, 6, camera_matrix, camera_distortion)
            rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]

            for corner in corners:
                corners = corner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners

                width = int(abs(topRight[0] - topLeft[0]))
                height = int(abs(bottomLeft[1]-topLeft[1]))
                x_mid = int(topLeft[0] + (width/2))
                y_mid = int(topLeft[1] + (height/2))

                if True:
                    if x_mid < rectX:
                        cv2.putText(imgGray, f'KEEP LEFT', (900, 80),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    elif x_mid > (rectX+200):
                        cv2.putText(imgGray, f'KEEP RIGHT', (900, 80),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

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
                aruco.drawAxis(img, camera_matrix,
                               camera_distortion, rvec, tvec, 10)
                break

        # cv2.putText(imgGray, f'TODO: DEPTH CALCULATION FOR FORWARD PROPULSION',
        #             (900, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.namedWindow("BGR", cv2.WINDOW_NORMAL)
        cv2.namedWindow("arUco", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('BGR', 800, 450)
        cv2.resizeWindow('arUco', 800, 450)

        cv2.imshow("BGR", img)
        cv2.imshow("arUco", imgGray)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
