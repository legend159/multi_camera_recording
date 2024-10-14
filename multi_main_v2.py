# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 16:32:34 2023

@author: legend159
"""

import threading
import queue
import cv2
import time
import tkinter as tk
from tkinter import filedialog

# Initialize the root Tkinter window and hide it
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)  # This will make the selection window stay on top
# Let the user select a directory for saving the output files
selected_directory = filedialog.askdirectory(title="Select Directory for Video and Time Files")
if not selected_directory:
    raise Exception("No directory selected!")

# Number of cameras
num_cameras = 2
# Set recording time outside the record_video function
recording_time = 10  # in seconds

# Construct file paths using the selected directory
output_paths = [f"{selected_directory}/camera_{i}_video.avi" for i in range(num_cameras)]
output_path2 = [f"{selected_directory}/camera_{i}_time.txt" for i in range(num_cameras)]
winname = [f"usb_{i}" for i in range(num_cameras)]

# Initialize a queue for each camera
image_queues = [queue.Queue() for _ in range(num_cameras)]

def record_video(cam_index, output_file, output_path2, winname, image_queue, stop_event, recording_time):
    video_capture = cv2.VideoCapture(cam_index)
    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_capture.set(cv2.CAP_PROP_FPS, 25)  # Set the frame rate

    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MJPG'), 25, size)
    timestamps = []

    frames_to_record = 25 * recording_time  # Calculate the total number of frames to record
    for frame in range(frames_to_record):
        ret, frame = video_capture.read()
        if not ret:
            break
        image_queue.put(frame)
        video_writer.write(frame)
        timestamps.append(time.time())
          
    stop_event.set()
    video_capture.release()
    video_writer.release()
    
    with open(output_path2, 'w') as f:
        for timestamp in timestamps:
            f.write(f"{timestamp}\n")

def main_thread(stop_event):
    while not stop_event.is_set():
        for i in range(num_cameras):
            if not image_queues[i].empty():
                processed_frame = image_queues[i].get()
                cv2.imshow(winname[i], processed_frame)
        if cv2.waitKey(1) == 27:  # Exit on ESC
            break
    cv2.destroyAllWindows()

# Create a threading.Event object
stop_event = threading.Event()

# Create and start the threads
threads = [
    threading.Thread(
        target=record_video,
        args=(i, output_paths[i], output_path2[i], winname[i], image_queues[i], stop_event, recording_time)
    ) for i in range(num_cameras)
]

for thread in threads:
    thread.start()

# Start the main thread
main_thread(stop_event)

# Wait for all threads to complete
for thread in threads:
    thread.join()