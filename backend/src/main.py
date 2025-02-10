import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.ping import router as ping_router
from api.users import router as users_router


app = FastAPI(
    title="Сайт для Кинотеатра",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=JSONResponse
)

app.include_router(ping_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)