import uvicorn
from conf.app import app
import routes


app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)