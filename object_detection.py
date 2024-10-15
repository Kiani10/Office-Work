import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from sklearn.metrics import pairwise_distances_argmin

# Expanded list of color names and their RGB values for better precision
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
    "pink": (255, 192, 203),
    "purple": (128, 0, 128),
    "lime": (0, 255, 0),
    "navy": (0, 0, 128),
    "teal": (0, 128, 128),
    "olive": (128, 128, 0),
    "maroon": (128, 0, 0),
    "silver": (192, 192, 192),
    "gold": (255, 215, 0),
    "beige": (245, 245, 220),
    "indigo": (75, 0, 130),
    "violet": (238, 130, 238),
    "chocolate": (210, 105, 30),
    "coral": (255, 127, 80),
    "salmon": (250, 128, 114),
    "khaki": (240, 230, 140),
    "azure": (240, 255, 255),
    "ivory": (255, 255, 240),
    "lavender": (230, 230, 250),
    "turquoise": (64, 224, 208),
    "tan": (210, 180, 140),
}

# Function to find the closest named color using Euclidean distance
def closest_color(requested_color):
    colors = np.array(list(color_names.values()))
    requested_color = np.array(requested_color).reshape(1, -1)
    index = pairwise_distances_argmin(requested_color, colors)
    return list(color_names.keys())[index[0]]

# Function to get the color name for a given BGR color
def get_color_name(bgr):
    rgb = (bgr[2], bgr[1], bgr[0])  # Convert BGR to RGB
    # Directly check if the RGB color matches any predefined color
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
