from fastapi import APIRouter
from crud.AmazonOrdering import AmazonOrdering
import logging
from core.logging_utils import setup_logger

log_name = "amazon"
endpoint_device_logger_setup = setup_logger(log_name, level='INFO')
logger = logging.getLogger(log_name)

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
