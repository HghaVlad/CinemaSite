import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os
import uuid


app = FastAPI(
    title="Service for PDF",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

API_TOKEN = "bla bla"

current_dir = os.getcwd()
pdf_dir = "pdfs"
os.makedirs(pdf_dir, exist_ok=True)

try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
except:
    pass


@app.get("/")
def hello():
    return "Hello world!"

@app.post("/generate_pdf")
async def generate_pdf(film: str,
        session: str,
        seat: str,
        row: str,
        time: str,
        user_name: str,
        user_surname: str,
        user_email,
        token: str = Header):

    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")

    file_id = uuid.uuid4()
    file_path = os.path.join(pdf_dir, f"{file_id}.pdf")

    canv = canvas.Canvas(file_path, pagesize=letter)
    canv.drawString(100, 750, f"Film: {film}")
    canv.drawString(100, 730, f"Session: {session}")
    canv.drawString(100, 710, f"Seat: {seat}")
    canv.drawString(100, 690, f"Row: {row}")
    canv.drawString(100, 670, f"Time: {time}")
    canv.drawString(100, 650, f"Name: {user_name}")
    canv.drawString(100, 630, f"Surname: {user_surname}")
    canv.drawString(100, 610, f"Email: {user_email}")
    canv.save()

    return {"file_url": f"/order/{file_id}"}


@app.get("/order/{file_id}")
async def get_pdf(file_id: str):
    file_path = os.path.join(pdf_dir, f"{file_id}.pdf")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf")
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)