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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Async SUP",
        version="alfa 1.0.0",
        description="Схема",
        routes=app.routes,
    )
    headers = {
        "name": "Authorization",
        "in": "header",
        "required": True,
        "schema": {
            "title": "Authorization",
            "type": "string"
        },
    }

    router_authorize = [route for route in app.routes[4:] if route.operation_id == "authorize"]
    for route in router_authorize:
        method = list(route.methods)[0].lower()
        try:
            # If the router has another parameter
            openapi_schema["paths"][route.path][method]['parameters'].append(headers)
        except Exception:
            # If the router doesn't have a parameter
            openapi_schema["paths"][route.path][method].update({"parameters":[headers]})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)