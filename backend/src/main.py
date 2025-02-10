import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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
    default_response_class=JSONResponse,
    swagger_ui_parameters={"oauth2RedirectUrl": "/docs/oauth2-redirect"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping_router)
app.include_router(users_router)
app.include_router(films_router)
app.include_router(showtime_router)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])


openapi_schema = get_openapi(
        title="Your API",
        version="1.0",
        routes=app.routes,
    )

openapi_schema.setdefault("components", {})

openapi_schema["components"]["securitySchemes"] = {
    "Bearer": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
}

for path, methods in openapi_schema["paths"].items():
    for method, details in methods.items():
        if "security" in details:
            details["security"] = [{"Bearer": []}]


app.openapi_schema = openapi_schema

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)