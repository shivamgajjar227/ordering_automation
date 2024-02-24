
from fastapi import APIRouter
from crud.AmazonOrdering import AmazonOrdering
import logging

logging.basicConfig(level=logging.INFO, filename="./logs/amazon.log",filemode="w")
logger = logging.getLogger("amazon")
router = APIRouter()

@router.post("/", summary="Initiate Amazon Automation")
def main(email:str, password:str, product_link:str):
    try:
        amazon_ordering = AmazonOrdering()
        response = amazon_ordering.start_ordering_process_thread(email=email,password=password, product_link=product_link)
        logger.info("success")
        return response
    except Exception as e:
        logger.exception("error")
        return e
