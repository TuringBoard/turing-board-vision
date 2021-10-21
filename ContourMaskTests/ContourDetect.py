import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture(2)
    while True:
        _, frame = cap.read()
        # cv2.imshow("Webcam", frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        low_red = np.array([81, 0, 132])
        high_red = np.array([101, 66, 212])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)

        cv2.imshow("Contours", red_mask)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
