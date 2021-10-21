# import cv2
# import numpy as np
# import time
# # A required callback method that goes into the trackbar function.
# def nothing(x):
#     pass

# # Initializing the webcam feed.
# cap = cv2.VideoCapture(2)
# cap.set(3,1280)
# cap.set(4,720)

# # Create a window named trackbars.
# cv2.namedWindow("Trackbars")

# # Now create 6 trackbars that will control the lower and upper range of
# # H,S and V channels. The Arguments are like this: Name of trackbar,
# # window name, range,callback function. For Hue the range is 0-179 and
# # for S,V its 0-255.
# cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
# cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
# cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

# while True:

#     # Start reading the webcam feed frame by frame.
#     ret, frame = cap.read()
#     if not ret:
#         break
#     # Flip the frame horizontally (Not required)
#     frame = cv2.flip( frame, 1 )

#     # Convert the BGR image to HSV image.
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # Get the new values of the trackbar in real time as the user changes
#     # them
#     l_h = cv2.getTrackbarPos("L - H", "Trackbars")
#     l_s = cv2.getTrackbarPos("L - S", "Trackbars")
#     l_v = cv2.getTrackbarPos("L - V", "Trackbars")
#     u_h = cv2.getTrackbarPos("U - H", "Trackbars")
#     u_s = cv2.getTrackbarPos("U - S", "Trackbars")
#     u_v = cv2.getTrackbarPos("U - V", "Trackbars")

#     # Set the lower and upper HSV range according to the value selected
#     # by the trackbar
#     lower_range = np.array([l_h, l_s, l_v])
#     upper_range = np.array([u_h, u_s, u_v])

#     # Filter the image and get the binary mask, where white represents
#     # your target color
#     mask = cv2.inRange(hsv, lower_range, upper_range)

#     # You can also visualize the real part of the target color (Optional)
#     res = cv2.bitwise_and(frame, frame, mask=mask)

#     # Converting the binary mask to 3 channel image, this is just so
#     # we can stack it with the others
#     mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

#     # stack the mask, orginal frame and the filtered result
#     stacked = np.hstack((mask_3,frame,res))

#     # Show this stacked frame at 40% of the size.
#     cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))

#     # If the user presses ESC then exit the program
#     key = cv2.waitKey(1)
#     if key == 27:
#         break

#     # If the user presses `s` then print this array.
#     if key == ord('s'):

#         thearray = [[l_h,l_s,l_v],[u_h, u_s, u_v]]
#         print(thearray)

#         # Also save this array as penval.npy
#         np.save('hsv_value',thearray)
#         break

# # Release the camera & destroy the windows.
# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import numpy as np


# cap = cv2.VideoCapture(2)


# def nothing(x):
#     pass


# # Creating a window for later use
# cv2.namedWindow('result')

# # Starting with 100's to prevent error while masking
# h, s, v = 100, 100, 100

# # Creating track bar
# cv2.createTrackbar('h', 'result', 0, 179, nothing)
# cv2.createTrackbar('s', 'result', 0, 255, nothing)
# cv2.createTrackbar('v', 'result', 0, 255, nothing)

# while(1):

#     _, frame = cap.read()

#     # converting to HSV
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # get info from track bar and appy to result
#     h = cv2.getTrackbarPos('h', 'result')
#     s = cv2.getTrackbarPos('s', 'result')
#     v = cv2.getTrackbarPos('v', 'result')

#     # Normal masking algorithm
#     lower_blue = np.array([h, s, v])
#     upper_blue = np.array([180, 255, 255])

#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     result = cv2.bitwise_and(frame, frame, mask=mask)

#     cv2.imshow('result', result)

#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:
#         break

# cap.release()

# cv2.destroyAllWindows()


import cv2
import sys
import numpy as np


def nothing(x):
    pass


useCamera = False

# Check if filename is passed
if (len(sys.argv) <= 1):
    print("'Usage: python hsvThresholder.py <ImageFilePath>' to ignore camera and use a local image.")
    useCamera = True

# Create a window
cv2.namedWindow('image')

# create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

# Output Image to display
if useCamera:
    cap = cv2.VideoCapture(2)
    # Wait longer to prevent freeze for videos.
    waitTime = 330
else:
    img = cv2.imread(sys.argv[1])
    output = img
    waitTime = 33

while(1):

    if useCamera:
        # Capture frame-by-frame
        ret, img = cap.read()
        output = img

    # get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')

    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)

    # Print if there is a change in HSV value
    if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
            hMin, sMin, vMin, hMax, sMax, vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # Display output image
    cv2.imshow('image', output)

    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(waitTime) & 0xFF == ord('q'):
        break

# Release resources
if useCamera:
    cap.release()
cv2.destroyAllWindows()
