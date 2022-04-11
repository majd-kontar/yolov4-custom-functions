import os
import shutil

from starlette.responses import FileResponse

import detect_video_endpoint
import detect_endpoint
import save_model_endpoint
import uvicorn
from fastapi import FastAPI, UploadFile

video_dir = './data/video/'
images_dir = './data/images/'
processed_dir = './detections/'
app = FastAPI()


def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/load_model")
async def load_model(weights: UploadFile):
    destination = './data/' + weights.filename
    try:
        buffer = open(destination, "wb")
        shutil.copyfileobj(weights.file, buffer)
        weights.file.close()
        save_model_endpoint.save_model(weights=destination)
        return {"Model Loaded": weights.filename}
    except:
        return {"Loading Failed"}
    finally:
        weights.file.close()


@app.post("/upload_video")
async def upload_video(video: UploadFile):
    destination = video_dir + video.filename
    try:
        buffer = open(destination, "wb")
        shutil.copyfileobj(video.file, buffer)
        return {"Uploaded filename": video.filename}
    except:
        return {"Upload Failed"}
    finally:
        video.file.close()


@app.get("/received_videos")
async def received_videos():
    try:
        files = os.listdir(video_dir)
        return {"Files Uploaded": files}
    except:
        return {"Message": "ERROR!"}


@app.get("/process_video")
async def process_video(file):
    try:
        detect_video_endpoint.detect(video=video_dir + file, output=processed_dir + '/videos/' + file)
        if os.path.exists(processed_dir + '/videos/' + file):
            return FileResponse(processed_dir + '/videos/' + file, media_type='application/octet-stream', filename=file)
    except:
        return {"Message": "File ERROR!"}


@app.get("/processed_videos")
async def processed_images():
    try:
        files = os.listdir(processed_dir + '/videos/')
        return {"Videos Processed": files}
    except:
        return {"Message": "ERROR!"}


@app.get("/get_processed_video")
async def get_processed_video(file):
    if os.path.exists(processed_dir + '/video/' + file):
        return FileResponse(processed_dir + '/video/' + file, media_type='application/octet-stream', filename=file)
    else:
        return {"Message": "File ERROR!"}


@app.post("/upload_image")
async def upload_image(image: UploadFile):
    destination = images_dir + image.filename
    try:
        buffer = open(destination, "wb")
        shutil.copyfileobj(image.file, buffer)
        return {"Uploaded filename": image.filename}
    except:
        return {"Upload Failed"}
    finally:
        image.file.close()


@app.get("/received_images")
async def received_images():
    try:
        files = os.listdir(images_dir)
        return {"Files Uploaded": files}
    except:
        return {"Message": "ERROR!"}


@app.get("/process_image")
async def process_image(file):
    try:
        detect_endpoint.detect(images=[images_dir + file], output=processed_dir + '/images/' + file)
        if os.path.exists(processed_dir + '/images/' + file):
            return FileResponse(processed_dir + '/images/' + file, media_type='application/octet-stream', filename=file)
        else:
            return {"Message": "File ERROR!"}
    except:
        return {"Message": "File ERROR!"}


@app.get("/processed_images")
async def processed_images():
    try:
        files = os.listdir(processed_dir + '/images/')
        return {"Images Processed": files}
    except:
        return {"Message": "ERROR!"}


@app.get("/get_processed_image")
async def get_processed_image(file):
    if os.path.exists(processed_dir + '/images/' + file):
        return FileResponse(processed_dir + '/images/' + file, media_type='application/octet-stream', filename=file)
    else:
        return {"Message": "File ERROR!"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)
