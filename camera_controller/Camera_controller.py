from siyi_sdk import SIYISDK
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import time
import sys
import os
import threading

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)

sys.path.append(parent_directory)


cam = SIYISDK(server_ip="192.168.144.25", port=37260)
if not cam.connect():
    print("No connection ")
    exit(1)


# Initialize the camera
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("rtsp://192.168.144.25:8554/main.264")
width = int(cap.get(3))
height = int(cap.get(4))

# Initialize variables
zoom_factor = 1
timer = 0
started = False
camera_open = False
flip = False

cam_control = False
cam_control_counter = 0
yaw = 0.3
pitch = 1.4
old_yaw, old_pitch = yaw, pitch


def zoom(frame):
    global zoom_factor
    # Prepare the crop
    x1 = int(0.5*width*(1-1/zoom_factor))
    x2 = int(width-0.5*width*(1-1/zoom_factor))
    y1 = int(0.5*height*(1-1/zoom_factor))
    y2 = int(height-0.5*height*(1-1/zoom_factor))

    # Crop
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (width, height), fx=zoom_factor, fy=zoom_factor)


def camera_zoom_in():
    cam.requestZoomIn()
    time.sleep(1)
    cam.requestZoomHold()


def camera_zoom_out():
    cam.requestZoomIn()
    time.sleep(1)
    cam.requestZoomHold()

def zoom_in():
    global zoom_factor
    if zoom_factor < 10:
        zoom_factor /= 0.98


def zoom_out():
    global zoom_factor
    if zoom_factor > 1:
        zoom_factor *= 0.98


def zoom_reset():
    global zoom_factor
    zoom_factor = 1


def name():
    dt = datetime.datetime.now()
    return f"{dt.year}_{dt.month}_{dt.day}_{dt.hour}_{dt.minute}_{dt.second}"


def elapsed(timer):
    elapsed_time = time.time()-timer
    hrs, reminder = divmod(elapsed_time, 3600)
    mins, secs = divmod(reminder, 60)
    return f"{int(hrs):02d}:{int(mins):02d}:{int(secs):02d}"

# Function to start/stop camera and update button text/color
def toggle_camera():
    global camera_open, timer
    if camera_open:
        camera_open = False
        start_stop_button.configure(
            text="Start Recording", style="Red.TButton")
    else:
        camera_open = True
        timer = time.time()
        start_stop_button.configure(
            text="Stop Recording", style="Green.TButton")

# Function to capture and save a screenshot
def capture_screenshot():
    global frame
    screenshot_filename = f"screenshot_{name()}.png"
    cv2.imwrite(screenshot_filename, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    print(f"Screenshot saved as {screenshot_filename}")


# Function to continuously update the camera feed
def show_camera_feed():
    global frame, started, camera_open, writer, timer, cam_control, cam_control_counter, flip
    if flip:
        frame = zoom(cv2.flip(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB), 1))
    else:
        frame = zoom(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB))

    if camera_open:
        if not started:
            started = True
            print("Start recording")
            if (cam.getRecordingState() < 0):
                cam.requestRecording()
            writer = cv2.VideoWriter(f"video_{name()}.mp4", cv2.VideoWriter_fourcc(*"DIVX"), 30, (width, height))
            writer.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            writer.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            video_timer.configure(text=f"{elapsed(timer)}")
    else:
        if started:
            started = False
            print("Stop recording")
            if (cam.getRecordingState() == cam._record_msg.ON):
                cam.requestRecording()
            writer.release()

    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=img)
    camera_label.img = img
    camera_label.config(image=img)

    # Call itself to update the feed continuously
    camera_label.after(10, show_camera_feed)

def Flip():
    global flip
    flip ^= 1


def up():
    global pitch, yaw
    if yaw < 25:
        yaw += 5
        cam.setGimbalRotation(pitch, yaw)


def down():
    global pitch, yaw
    if yaw > -90:
        yaw -= 5
        cam.setGimbalRotation(pitch, yaw)


def right():
    global pitch, yaw
    if pitch > -45:
        pitch -= 5
        cam.setGimbalRotation(pitch, yaw)


def left():
    global pitch, yaw
    if pitch < 45:
        pitch += 5
        cam.setGimbalRotation(pitch, yaw)


def center():
    global yaw, pitch, old_yaw, old_pitch
    cam.requestCenterGimbal()
    yaw = 0.3
    pitch = 1.4
    old_yaw, old_pitch = yaw, pitch


def setGimbalRotation(self: SIYISDK):
    global yaw, pitch, old_yaw, old_pitch
    while True:
        time.sleep(0.1)
        if old_yaw == yaw and old_pitch == pitch:
            continue
        self.requestGimbalAttitude()
        if self._att_msg.seq == self._last_att_seq:
            self.requestGimbalSpeed(0, 0)
            continue

        self._last_att_seq = self._att_msg.seq

        yaw_err = -yaw + self._att_msg.yaw
        pitch_err = pitch - self._att_msg.pitch

        if (abs(yaw_err) <= 1 and abs(pitch_err) <= 1):
            self.requestGimbalSpeed(0, 0)
            old_yaw, old_pitch = yaw, pitch
        else:
            self.requestGimbalSpeed(max(min(100, int(4*yaw_err)), -100), max(min(100, int(4*pitch_err)), -100))



# Create the main GUI window
root = tk.Tk()
root.title("Orabi SIYI Camera Control")

# Create a style for the buttons (to set colors)
style = ttk.Style()
style.configure("Red.TButton", foreground="black", background="red")
style.configure("Green.TButton", foreground="black", background="green")

# Create and configure the Start/Stop button
start_stop_button = ttk.Button(
    root, text="Start Recording", style="Red.TButton", command=toggle_camera)
start_stop_button.grid(column=10, row=1, columnspan=3)

# Create a label to display the camera feed
video_timer = tk.Label(root, text="00:00:00")
video_timer.grid(column=10, row=2, columnspan=3)

# Create the Screenshot button
screenshot_button = ttk.Button(
    root, text="Take Screenshot", command=capture_screenshot)
screenshot_button.grid(column=10, row=3, columnspan=3)

# Create the zoom in button
zoom_in_button = ttk.Button(root, text="Zoom +", command=zoom_in)
zoom_in_button.grid(column=10, row=4, columnspan=3)

# Create the zoom out button
zoom_out_button = ttk.Button(root, text="Zoom -", command=zoom_out)
zoom_out_button.grid(column=10, row=5, columnspan=3)

# Create the zoom reset button
zoom_reset_button = ttk.Button(root, text="Zoom Reset", command=zoom_reset)
zoom_reset_button.grid(column=10, row=6, columnspan=3)

# Create the up button
up_button = ttk.Button(root, text="Up", command=up)
up_button.grid(column=10, row=7, columnspan=3)

# Create the right button
right_button = ttk.Button(root, text="Right", command=right)
right_button.grid(column=12, row=8)

# Create the center button
right_button = ttk.Button(root, text="Center", command=center)
right_button.grid(column=11, row=8)

# Create the left button
left_button = ttk.Button(root, text="Left", command=left)
left_button.grid(column=10, row=8)

# Create the down button
down_button = ttk.Button(root, text="Down", command=down)
down_button.grid(column=10, row=9, columnspan=3)

# Create the Cam Zoom In button
right_button = ttk.Button(root, text="Cam Zoom +", command=camera_zoom_in)
right_button.grid(column=12, row=10)

# Create the Flip Cam button
left_button = ttk.Button(root, text="Flip Cam", command=Flip)
left_button.grid(column=11, row=10)

# Create the Cam Zoom Out button
left_button = ttk.Button(root, text="Cam Zoom -", command=camera_zoom_out)
left_button.grid(column=10, row=10)

# Create a label to display the camera feed
camera_label = tk.Label(root)
camera_label.grid(column=0, row=0, rowspan=40)

# Main loop to run the GUI
# threading.Thread(target=setGimbalRotation, args=(cam,)).start()
show_camera_feed()
root.mainloop()

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
