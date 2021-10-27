import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture(2)
    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # low_red = np.array([ 133,93,40]) # purples 2
        # high_red = np.array([153,164,130])
        low_red = np.array([52, 115, 44])
        high_red = np.array([82, 255, 153])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)

        contours, _ = cv2.findContours(
            red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(
            contours, key=lambda x: cv2.contourArea(x), reverse=True)
        x_mid, y_mid = 0, 0
        w = 0
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            x_mid = int((x+x+w)/2)
            y_mid = int((y+y+h)/2)
            break

        rectX = int((1280/2)-100)
        rectY = int((720/2)-100)
        rectW = int(rectX + 200)
        rectH = int(rectY + 200)
        cv2.rectangle(red_mask, (rectX, 0),
                      (rectW, 720), (255, 255, 255), 2)

        if w > 10:
            if x_mid < rectX:
                cv2.putText(red_mask, f'KEEP LEFT', (900, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            elif x_mid > (rectX+400):
                cv2.putText(red_mask, f'KEEP RIGHT', (900, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # cv2.putText(red_mask, f'TODO: DEPTH CALCULATION FOR FORWARD PROPULSION',
        #             (900, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.line(frame, (x_mid, 0), (x_mid, 1080), (0, 0, 255), 2)
        cv2.line(frame, (0, y_mid), (1920, y_mid), (0, 0, 255), 2)

        cv2.namedWindow("BGR", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('BGR', 800, 450)
        cv2.resizeWindow('Contours', 800, 450)

        cv2.putText(red_mask, f'Center coordinates: ({x_mid}, {y_mid})', (
            900, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("BGR", frame)
        cv2.imshow("Contours", red_mask)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
