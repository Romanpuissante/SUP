import uvicorn
from conf.app import app
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import routes

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.include_router(routes.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)