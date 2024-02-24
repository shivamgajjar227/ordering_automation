from fastapi import FastAPI
from api.api import api_router
import uvicorn

app = FastAPI(title='Order Automation', openapi_url="/api/api/openapi.json")

app.include_router(api_router)

uvicorn.run(app, host="localhost", port=8000)