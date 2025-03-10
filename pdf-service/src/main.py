import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Service for PDF",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

@app.get("/")
def hello():
    return "Hello world!"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)