import cv2


cap = cv2.VideoCapture(2)
cap.set(3, 640)
cap.set(4, 480)
while True: 
    _, img = cap.read()
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 640, 480)
    cv2.imshow("image",img)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        cv2.destroyAllWindows()
        break