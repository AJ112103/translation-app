from pydantic import BaseModel
from typing import Dict

class TranslationRequest(BaseModel):
    text: str
    languages: list[str]

class TaskResponse(BaseModel):
    task_id: int
    class Config:
        orm_mode = True

class TranslationStatus(BaseModel):
    task_id: int
    status: str
    translations: Dict[str, str]
