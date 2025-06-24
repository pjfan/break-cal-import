from fastapi import APIRouter, HTTPException, Response, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.event_parser import EventParser
from app.utils.csv_generator import generate_csv
import tempfile
import os

router = APIRouter()

@router.post("/extract-event/")
async def extract_event(url: str):
    """
    Extract event details from the given URL and return them as a dictionary.
    """
    try:
        parser = EventParser(url)
        event_details = parser.fetch_event_details()
        return event_details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/download-csv/")
async def download_csv(event_details: dict, background_tasks: BackgroundTasks):
    """
    Accepts an event_details dictionary, generates a CSV, and returns it as a downloadable attachment.
    """
    try:
        csv_file_path = generate_csv(event_details)
        filename = os.path.basename(csv_file_path)
        background_tasks.add_task(os.remove, csv_file_path)
        return FileResponse(
            path=csv_file_path,
            filename=filename,
            media_type="text/csv"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))