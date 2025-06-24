from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from app.services.event_parser import EventParser
from app.utils.csv_generator import generate_csv
import json

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_link(request: Request, event_url: str = Form(...)):
    parser = EventParser(event_url)
    event_details = parser.fetch_event_details()
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "event": event_details}
    )

@app.post("/download-csv", response_class=StreamingResponse)
async def download_csv(event_json: str = Form(...)):
    """
    Accepts event_details as a JSON string, generates a CSV, and returns it as a downloadable file.
    """
    event_details = json.loads(event_json)
    csv_path = generate_csv(event_details)
    file_like = open(csv_path, "rb")
    return StreamingResponse(
        file_like,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=event.csv"}
    )