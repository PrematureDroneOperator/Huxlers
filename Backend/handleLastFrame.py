from fastapi import FastAPI
import cv2
import os


app = FastAPI()
def save_last_frame(video_path: str, output_path: str):

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$ Video file ka naammmm $$$$$$$$$$$$$$$$$$$$$$$$$$$

    # Check if video exists
    if not os.path.exists(video_path):
        return {"error": "Video file not found"}

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Error opening video file"}

    # Get total frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Move pointer to last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

    # Read the frame
    success, frame = cap.read()
    if not success:
        return {"error": "Unable to read last frame"}

    # Save as PNG
    cv2.imwrite(output_path, frame)

    cap.release()
    print("Last frame saved successfully!!!")
    return {
        "message": "Last frame saved successfully",
        "file_path": output_path
    }
