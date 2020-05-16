# import the necessary packages
import ctypes
import time

import cv2
import imutils
from imutils.video import VideoStream
import configparser

config = configparser.ConfigParser()
config.read('tracking.ini')

videoSource = config.getint('tracking', 'videoSource')
color1LowerBound = tuple(map(int, config['tracking']['color1LowerBound'].split(",")))
color1UpperBound = tuple(map(int, config['tracking']['color1UpperBound'].split(",")))
color2LowerBound = tuple(map(int, config['tracking']['color2LowerBound'].split(",")))
color2UpperBound = tuple(map(int, config['tracking']['color2UpperBound'].split(",")))
applyFullHdFix = config.getboolean('tracking', 'applyFullHdFix')
showCameraSettings = config.getboolean('tracking', 'showCameraSettings')
scaleFrameWidth = config.getint('tracking', 'scaleFrameWidth')

###########################
# Mouse movement
###########################

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def move_mouse_to(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))

    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


###########################
# Tracking
###########################

# Open video stream
vs = VideoStream(src=videoSource + cv2.CAP_DSHOW).start()
if applyFullHdFix:
    # Enable Full HD
    vs.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vs.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # Enable compression
    vs.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
if showCameraSettings:
    # Open webcam settings window
    vs.stream.set(cv2.CAP_PROP_SETTINGS, 1)

# Allow camera to warm up
time.sleep(2.0)

# Previous tracked center
prevCenter = None
# Minimum tracking radius
minRadius = 5

while True:
    # Grab the current frame
    frame = vs.read()

    # If there is no frame, exit
    if frame is None:
        break

    # Resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=scaleFrameWidth)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Construct a masks for the colors "green"
    hammerMask = cv2.inRange(hsv, color1LowerBound, color1UpperBound)
    ballMask = cv2.inRange(hsv, color2LowerBound, color2UpperBound)

    # Combine 2 masks
    mask = cv2.bitwise_or(hammerMask, ballMask)

    # Perform a series of dilations and erosions to
    # remove any small blobs left in the mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask and initialize the current
    # (x, y) center of the ball
    contours = cv2.findContours(mask.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    # Only proceed if at least one contour was found
    if len(contours) > 0:
        # Find the largest contour in the mask, then use it
        # to compute the minimum enclosing circle and centroid
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius meets a minimum size
        if radius > minRadius:
            if prevCenter is not None:
                move_mouse_to(int((prevCenter[0] - center[0]) * 3.2), -int((prevCenter[1] - center[1]) * 3.2))

            prevCenter = center

            # Draw the circle and centroid on the frame,
            # Then update the list of tracked points.
            cv2.circle(frame, (int(x), int(y)), int(radius), (204, 204, 204), 2)

    # Show images
    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)

    # If the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Otherwise, release the camera
vs.stop()

# Close all windows
cv2.destroyAllWindows()
