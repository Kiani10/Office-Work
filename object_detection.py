import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

# A simple list of color names and their RGB values
color_names = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "brown": (165, 42, 42),
    "orange": (255, 165, 0),
    # Add more colors if needed
}

# Function to find the closest named color
def closest_color(requested_color):
    min_distances = {}
    for name, rgb in color_names.items():
        distance = np.sum((np.array(rgb) - np.array(requested_color)) ** 2)
        min_distances[distance] = name
    return min_distances[min(min_distances.keys())]

# Function to get the color name for a given BGR color
def get_color_name(bgr):
    rgb = (bgr[2], bgr[1], bgr[0])  # Convert BGR to RGB
    # Check if the RGB color matches any predefined color
    if rgb in color_names.values():
        return list(color_names.keys())[list(color_names.values()).index(rgb)]
    
    # If no exact match is found, get the closest color name
    return closest_color(rgb)

# Function to get the clicked color and display it
def get_color_on_click(event, x, y, flags, param):
    global paused
    if event == cv2.EVENT_LBUTTONDOWN:
        paused = True
        # Get the BGR color at the clicked position
        clicked_color = param[y, x]
        color_name = get_color_name(clicked_color)
        
        # Print color info (BGR, RGB, and the color name)
        print(f"Clicked Color (BGR): {clicked_color}")
        print(f"Clicked Color (RGB): {clicked_color[::-1]}")
        print(f"Color Name: {color_name}")
    
    elif event == cv2.EVENT_LBUTTONUP:
        paused = False

# Function to browse and select a video file
def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if filepath:
        play_video(filepath)

# Function to play the selected video
def play_video(filepath):
    cap = cv2.VideoCapture(filepath)

    # Resize the video player window
    desired_width = 640
    desired_height = 480

    global paused
    paused = False

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the video frame to a smaller size
            frame_resized = cv2.resize(frame, (desired_width, desired_height))

            # Display the resized frame
            cv2.imshow('Video Player - Click to Get Color', frame_resized)

            # Set the mouse callback for detecting clicks
            cv2.setMouseCallback('Video Player - Click to Get Color', get_color_on_click, frame_resized)
        
        key = cv2.waitKey(10)
        if key == 27:  # Press 'ESC' to exit
            break

        # Check if the OpenCV window was manually closed
        if cv2.getWindowProperty('Video Player - Click to Get Color', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to close the GUI properly
def on_closing():
    root.quit()
    root.destroy()

# Set up GUI
root = tk.Tk()
root.title("Video Player with Color Detection")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Select a video file to play:")
label.pack()

browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack()

# Proper handling of the "X" button on the GUI window
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
