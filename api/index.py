from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from api.peopleCounter import PeopleCounter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

UPLOAD_DIRECTORY = "./uploads"
ANNOTATED_DIRECTORY = "./annotated"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    person_count, annotated_filepath = PeopleCounter(file_path)
    return JSONResponse(content={"filename": file.filename, 
                                 "personCount": person_count,
                                 "annotatedImage": f"http://localhost:8000/annotated/{file.filename}"}, )

app.mount("/annotated", StaticFiles(directory=ANNOTATED_DIRECTORY), name="annotated")