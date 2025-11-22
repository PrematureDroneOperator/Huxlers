from fastapi import FastAPI, HTTPException
import requests
import os
import uuid
import ffmpeg

app = FastAPI()

BASE_DIR = "downloaded_videos"
os.makedirs(BASE_DIR, exist_ok=True)


def get_user_folder(user_id: str):
    folder = f"{BASE_DIR}/{user_id}"
    os.makedirs(folder, exist_ok=True)
    return folder


# # -------------------------------------------
# # 1️⃣ DOWNLOAD VIDEO FOR A USER
# # -------------------------------------------
# @app.get("/download-video")
# def download_video(user_id: str, url: str):

#     try:
#         user_folder = get_user_folder(user_id)

#         file_id = str(uuid.uuid4())
#         file_path = f"{user_folder}/{file_id}.mp4"

#         # Use ffmpeg to download both audio + video
#         (
#             ffmpeg
#             .input(url)      # fetch network stream
#             .output(file_path, acodec='copy', vcodec='copy')  # no re-encode
#             .run()
#         )

#         return {
#             "message": "Video downloaded with audio",
#             "user_id": user_id,
#             "file_path": file_path
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




# -------------------------------------------
# 2️⃣ CONCATENATE ALL VIDEOS OF A USER
# -------------------------------------------

def concat_videos(video1_path: str, video2_path: str, video3_path: str, video4_path: str):
    try:
        # List of video file paths from parameters
        videos = [video1_path, video2_path, video3_path, video4_path]

        # Filter out any empty or None paths (optional if user may pass less than 4)
        videos = [v for v in videos if v]

        if len(videos) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 videos to merge")

        # Extract the folder from the first video path to store the list.txt and output
        user_folder = os.path.dirname(videos[0])

        # Sort the videos for consistent concatenation order
        videos.sort()

        # Prepare list.txt file path inside the user folder
        list_file_path = os.path.join(user_folder, "list.txt")

        # Write the file names (not full paths) into list.txt
        with open(list_file_path, "w") as list_file:
            for video_path in videos:
                filename = os.path.basename(video_path)
                list_file.write(f"file '{filename}'\n")

        # Output path for the concatenated video
        output_path = os.path.join(user_folder, "final_output.mp4")

        # Run ffmpeg concat operation referencing list.txt
        ffmpeg.input(list_file_path, format="concat", safe=0).output(
            output_path, c="copy"
        ).run()

        return {
            "message": "Videos concatenated",
            "final_video": output_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
