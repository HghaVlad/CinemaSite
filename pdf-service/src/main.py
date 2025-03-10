import os
import uuid

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from ticket_creator_utils import generate_ticket_pdf

load_dotenv()

app = FastAPI(
    title="Service for PDF",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

API_TOKEN = os.getenv("PDF_API_TOKEN")

current_dir = os.getcwd()
pdf_dir = "pdfs"
parent_dir = os.path.join(current_dir, "..", pdf_dir)
os.makedirs(parent_dir, exist_ok=True)


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
    """
    Generates pdf for entered data. Outputs url like /order/<pdf_id>.
    You can access created pdf on <servername>/order/<pdf_id>
    """

    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")

    file_id = uuid.uuid4()
    file_path = os.path.join(parent_dir, f"{file_id}.pdf")

    generate_ticket_pdf(
        filename=file_path,
        film=film,
        session=session,
        seat=seat,
        row=row,
        time=time,
        user_name=user_name,
        user_surname=user_surname,
        user_email=user_email
    )

    return {"file_url": f"/order/{file_id}"}


@app.get("/order/{file_id}")
async def get_pdf(file_id: str):
    file_path = os.path.join(parent_dir, f"{file_id}.pdf")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf")
    else:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)