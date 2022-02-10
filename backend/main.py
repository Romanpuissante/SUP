import uvicorn
from conf.app import app
from fastapi.middleware.cors import CORSMiddleware
import routes
from routes.consumers import router as ws_router

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://172.16.200.22:8080"
]

app.include_router(routes.router, prefix="/api")
app.include_router(ws_router, prefix="")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


