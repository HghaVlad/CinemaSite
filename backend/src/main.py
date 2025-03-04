import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.ping import router as ping_router
from api.users import router as users_router
from api.auth import router as auth_router
from api.films import router as films_router
from api.showtime import router as showtime_router
from api.payments import router as payments_router

app = FastAPI(
    title="Сайт для Кинотеатра",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=JSONResponse
)

app.include_router(ping_router)
app.include_router(users_router)
app.include_router(films_router)
app.include_router(showtime_router)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)