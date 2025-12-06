from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi.responses import FileResponse

router = APIRouter(
    prefix='/file',
    tags=['files']
)

@router.post('/') #small file upload of bytes. like txt file
def get_file(file:bytes=File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    return{"lines": lines}

@router.post('/upload') #for larger files
def get_upload_file(upload_file:UploadFile = File(...)):
    #upload_file is a python file object. can use various methods on it, including storing locally
    path = f"files/{upload_file.filename}"
    with open(path, "w+b") as buffer: 
        shutil.copyfileobj(upload_file.file, buffer)
    return{"filename": path,
           "content_type": upload_file.content_type}

@router.get('/download/{name}', response_class=FileResponse) #shows the type of response we want
def download_file(name:str):
    path = f'files/{name}'
    return path #name is passed to file response to serve the file