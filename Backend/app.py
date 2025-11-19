import fastapi
app = fastapi.FastAPI()
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Video Script Generator API YOU ARE BITCH!!!"}