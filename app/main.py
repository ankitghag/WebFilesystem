from fastapi import FastAPI, Request
from  app.api.v1.api import api_router
from app.core.config import setting
from fastapi.responses import JSONResponse
from app.exceptions.http_exceptions import BaseCustomError


app= FastAPI()
@app.exception_handler(BaseCustomError)
async def custom_error_handler(request: Request, exc: BaseCustomError):
    # This logic is universal for ALL your custom errors
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "error_code": exc.error_code
        }
    )
app.include_router(api_router, prefix=setting.API_V1_STR)

@app.get("/test")
def testing():
    print("GET REQUIEST")
    return "HELLO WORLD"
print("RUNNING HOST : http://127.0.0.1:8000")