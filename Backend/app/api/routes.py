from fastapi import APIRouter
from pydantic import BaseModel
from app.services.pipeline import run_pipeline

router = APIRouter()


class ProcessRequest(BaseModel):
    source: str
    language: str


@router.get("/")
def home():
    return {"message": "AI Meeting Assistant API Running"}


@router.post("/process")
def process_video(request: ProcessRequest):

    result = run_pipeline(
        request.source
    )

    return result