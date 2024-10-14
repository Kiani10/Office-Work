import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

# Function to browse and select a video file
def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if filepath:
        play_video(filepath)

# Function to detect red objects and draw bounding boxes
def detect_red_objects(frame):
    # Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper range for the color red in HSV space
    lower_red1 = np.array([0, 120, 50])    # Adjusted lower red range (lighter reds)
    upper_red1 = np.array([10, 255, 255])  # Adjusted upper red range
    lower_red2 = np.array([170, 120, 50])  # Adjusted second lower red range (darker reds)
    upper_red2 = np.array([180, 255, 255]) # Adjusted second upper red range

    # Create masks to detect red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine both masks to cover full red range
    mask = mask1 + mask2

    # Optional: Display the mask for debugging purposes (comment this out if not needed)
    # cv2.imshow('Red Mask', mask)

    # Find contours in the mask (red areas)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected red objects
    for contour in contours:
        if cv2.contourArea(contour) > 200:  # Lowered contour area threshold for smaller objects
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

# Function to play the selected video and detect red objects
def play_video(filepath):
    cap = cv2.VideoCapture(filepath)
    
    paused = False

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect red objects in the frame and draw bounding boxes
            red_detected_frame = detect_red_objects(frame)

            # Display the frame with red object detection and bounding boxes
            cv2.imshow('Video Player - Red Object Detection', red_detected_frame)
        
        key = cv2.waitKey(10)
        if key == ord('p'):  # Press 'p' to pause
            paused = True
        elif key == ord('s'):  # Press 's' to start/resume
            paused = False
        elif key == 27:  # Press 'ESC' to exit
            break

        # Check if the OpenCV window was manually closed
        if cv2.getWindowProperty('Video Player - Red Object Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to close the GUI properly
def on_closing():
    root.quit()
    root.destroy()

# Set up GUI
root = tk.Tk()
root.title("Video Player with Red Object Detection")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Select a video file to play:")
label.pack()

browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack()

# Proper handling of the "X" button on the GUI window
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
