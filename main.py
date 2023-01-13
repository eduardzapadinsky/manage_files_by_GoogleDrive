"""
Manage files in Google Drive by sending get, post, put requests using FastApi.
To start app and try requests enter "uvicorn main:app --reload" and go to
http://127.0.0.1:8000/docs

"""

import shutil
from fastapi import FastAPI, UploadFile, File
import os

import google_drive

app = FastAPI()


def buffer_file(file):
    """Buffer temporary file"""
    file_name = file.filename
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_dir = os.path.abspath(file_name)
    google_drive.gd_upload_file(file_name, file_dir)
    os.remove(file_name)


@app.post("/post/")
def upload_file(file: UploadFile = File(...)):
    """Upload file"""
    buffer_file(file)
    return {"file_name": file.filename}


@app.get("/")
def show_file(file_name):
    """Show file information"""
    answer = google_drive.gd_show_file(file_name)
    return answer


@app.get("/all/")
def show_all_files():
    """Show information about all the files"""
    answer = google_drive.gd_show_all_files()
    return answer


@app.get("/download/")
def download_file(file_name):
    """Download file my name"""
    google_drive.gd_download_file(file_name)
    return {"file_name": file_name}


@app.put("/put/")
def update_file(file: UploadFile = File(...)):
    """Change file"""
    file_name = file.filename
    google_drive.gd_delete_file(file_name)
    buffer_file(file)
    return {"file_name": file.filename}
