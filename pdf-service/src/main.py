import uvicorn
from fastapi import FastAPI, Header, HTTPException

import os
import uuid


app = FastAPI(
    title="Service for PDF",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

@app.get("/")
def hello():
    return "Hello world!"

API_TOKEN = "bla bla"

current_dir = os.getcwd()
pdf_dir = os.path.join(current_dir, "..", "pdfs")
os.makedirs(pdf_dir, exist_ok=True)


@app.post("/generate_pdf")
def generate_pdf(film: str,
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












if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)