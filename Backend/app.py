import fastapi
from pydantic import BaseModel
from handlePrompts import read
from handleImageGen import generate_image_with_google
from json import dumps
from handleVideoGen import generate_content
from handleLastFrame import save_last_frame
from main import concat_videos
app = fastapi.FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Video Script Generator API YOU ARE WELCOME!!!"}


class VideoMakeRequest(BaseModel):
    prompt: str


@app.post("/VideoMake")
async def video_make(req : VideoMakeRequest):
    print(req.prompt, "\n>>>Recieved Prompt, now we shall generate Video Script.", flush=True)
    Scin = read(req.prompt)
    print(Scin, "\n>>>This is Video Prompt, now generating Video Image.", flush=True)
    Scene1 = Scin[0]
    Scene2 = Scin[1]
    Scene3 = Scin[2]
    Scene4 = Scin[3]
    generate_image_with_google(prompt=Scene1["description"], output_file="gens/scene1.png")
    print("\n>>>Generated image for Scene 1", flush=True)
    print(">>>Now generating video for Scene 1", flush=True)
    generate_content(prompt = Scene1["description"], image_path="gens/scene1.png", output_file="gens/clip1.mp4")
    print("\n>>>Generated video for Scene 1", flush=True)
    print(">>>Now Generating video for Scene 2", flush=True)
    save_last_frame(video_path="gens/clip1.mp4", output_path="gens/last_frame1.png")
    print("\n>>>Saved last frame for Scene 1", flush=True)
    generate_content(prompt = Scene2["description"], image_path="gens/last_frame1.png", output_file="gens/clip2.mp4")
    print("\n>>>Generated video for Scene 2", flush=True)
    print(">>>Now Generating video for Scene 3", flush=True)
    save_last_frame(video_path="gens/clip2.mp4", output_path="gens/last_frame2.png")
    print("\n>>>Saved last frame for Scene 2", flush=True)
    generate_content(prompt = Scene3["description"], image_path="gens/last_frame2.png", output_file="gens/clip3.mp4")
    print("\n>>>Generated video for Scene 3", flush=True)
    print(">>>Now Generating video for Scene 4", flush=True)
    save_last_frame(video_path="gens/clip3.mp4", output_path="gens/last_frame3.png")
    print("\n>>>Saved last frame for Scene 3", flush=True)
    generate_content(prompt = Scene4["description"], image_path="gens/last_frame3.png", output_file="gens/clip4.mp4")
    print("\n>>>Generated video for Scene 4", flush=True)
    concat_result = concat_videos("gens/clip1.mp4", "gens/clip2.mp4", "gens/clip3.mp4", "gens/clip4.mp4")
    print(f"\n>>>Concatenation result: {concat_result}", flush=True)

    return {"message": "Video generation complete", "details": "All scenes processed and concatenated."}

    
    