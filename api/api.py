from fastapi import APIRouter

from endpoints import amazon_automation

api_router = APIRouter()
api_router.include_router(amazon_automation.router, prefix="/amazon")