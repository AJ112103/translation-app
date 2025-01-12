from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import schemas
import crud
import models
from utils import perform_translation
from sqlalchemy.orm import Session
from database import get_db, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate", response_model=schemas.TaskResponse)
def translate(
    request: schemas.TranslationRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    task = crud.create_translation_task(db, request.text, request.languages)
    background_tasks.add_task(
        perform_translation, 
        task.id, 
        request.text, 
        request.languages, 
        db
    )
    return {"task_id": task.id}

@app.get("/translate/{task_id}", response_model=schemas.TranslationStatus)
def get_translate(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
         
    return {
        "task_id": task.id,         
        "status": task.status,
        "translations": task.translations
    }

@app.get("/translate/{task_id}/content", response_model=schemas.TranslationStatus)
def get_translate_content(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = crud.get_translation_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="task not found") 
        
    return {
    "task_id": task.id,
    "status": task.status,
    "translations": task.translations
}