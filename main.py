import time
import cv2 
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import win32gui
import win32ui
import win32con
import win32api
import keyboard
#####################
# SETTINGS for button to be pressed
#####################
npc = 's'
confidence = 0.6 # set higher if too much false positives, lower if too much false negatives, 0 to 1
sleepAfterSuccess = 0.06 # increase to reduce max combo count (0.06 may reach 3000 points)
# benchmarks:
# 0.2 for 1300 points
# 0.15 for 1650 points
# 0.06 for ~2800 points


noisyWaitTrigger = 2.5 #wait how many seconds after noisy prompt before crouching? (about 3 seconds max)
crouchDuringNoisySeconds = 3 #how many seconds to crouch during noisy prompt (2.5 usually, but if others get spotted, up to 3 seconds ish)

#####################
# SETTINGS for game
#####################
hwnds = []
#default size
w = 1366
h = 768

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        if (win32gui.GetWindowText(hwnd) == "MapleStory"):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
            hwnds.append(hwnd)

####################
# PREDICTION LOOP
####################
win32gui.EnumWindows( winEnumHandler, None )
hwnd = hwnds[0]
if (len(hwnds) > 1): #player has chat external
    hwnd = hwnds[1]

#get the correct size
# rect = win32gui.GetWindowRect(hwnd)
# x = rect[0]
# y = rect[1]
# w = rect[2] - x
# h = rect[3] - y

wDC = win32gui.GetWindowDC(hwnd)
dcObj=win32ui.CreateDCFromHandle(wDC)
cDC=dcObj.CreateCompatibleDC()
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
cDC.SelectObject(dataBitMap)

def start():
    #init yolov8
    model = YOLO('noisyArrow.pt')
    noisy = False
    noisyAt = time.time()
    while True: 
        start = time.time()
    # Capture frame-by-frame
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)

        # #4 channel to 3 channel
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h,w,4)
        # img = img[:shapeHeight, :w]
        frame = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        #second [135 128  51 255] blue??
        #second [103 122  76 255] yellow!?
        #second [126 104  76 255] red !?
        #second [103 128  69 255] GREEEEN?!?!?!

        #make the frame half size
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        
        # Press Q on keyboard to exit 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            cv2.destroyAllWindows() 
            break

        results = model(frame, verbose=False, conf=confidence)
        #get the result boxes
        for r in results:
            annotator = Annotator(frame)
            boxes = r.boxes
            #this is for debugging
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)])
                if model.names[int(c)] == "noisy" and not noisy:
                    print("Noisy detected")
                    noisy = True
                    noisyAt = time.time()
                #arrow_left, arrow_right, arrow_up, arrow_down
                if model.names[int(c)] == "arrow_left":
                    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x001E0001)
                    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0x001E0001)
                    print("LEFT")
                    time.sleep(sleepAfterSuccess)
                elif model.names[int(c)] == "arrow_right":
                    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x00200001)
                    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x00200001)
                    print("RIGHT")
                    time.sleep(sleepAfterSuccess)
                elif model.names[int(c)] == "arrow_up":
                    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0x001C0001)
                    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_UP, 0x001C0001)
                    print("UP")
                    time.sleep(sleepAfterSuccess)
                elif model.names[int(c)] == "arrow_down":
                    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0x001E0001)
                    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0x001E0001)
                    print("DOWN")
                    time.sleep(sleepAfterSuccess)

        #use numpy to check if img[468,706] pixel color is [135 128  51 255]
        # if np.array_equal(img[468,706], [135, 128, 51, 255]): #blue, right
        #     win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x00200001)
        #     win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x00200001)
        #     print("RIGHT")
        #     time.sleep(sleepAfterSuccess)
        
        # elif np.array_equal(img[468,706], [103, 122, 76, 255]): #yellow, up
        #     win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0x001C0001)
        #     win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_UP, 0x001C0001)
        #     print("UP")
        #     time.sleep(sleepAfterSuccess)

        
        # elif np.array_equal(img[468,706], [126, 104, 76, 255]): #red, down
        #     win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0x001E0001)
        #     win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_DOWN, 0x001E0001)
        #     print("DOWN")
        #     time.sleep(sleepAfterSuccess)

        
        # elif np.array_equal(img[468,706], [103, 128, 69, 255]): #green, left
        #     win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x001E0001)
        #     win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0x001E0001)
        #     print("LEFT")
        #     time.sleep(sleepAfterSuccess)


        frame = annotator.result()
        cv2.imshow('Frame', frame)
        end = time.time()
        #sleep for 1/60th of a second minus the time taken to capture the screen
        # sleeptime = 1/60 - (end-start)
        # if sleeptime > 0:
        #     time.sleep(sleeptime)
        
        if noisy:
            #if time now minus noisyAt has passed the noisyWaitTrigger in seconds, crouch
            if time.time() - noisyAt > noisyWaitTrigger:
                keyboard.press(npc)
                print("CROUCH")
                time.sleep(crouchDuringNoisySeconds)
                keyboard.release(npc)
                noisy = False
                print("STAND UP")

start()