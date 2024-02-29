from fastapi import APIRouter

import constants
from crud.AmazonOrdering import AmazonOrdering
import logging
from core.logging_utils import setup_logger

log_name = "amazon"
endpoint_device_logger_setup = setup_logger(log_name, level='INFO')
logger = logging.getLogger(log_name)

router = APIRouter()
ordering_object_id = 0
ordering_object_id_wise_dict = {}

@router.post("/", summary="Initiate Amazon Automation")
def main(email:str, password:str, product_link:str):
    try:
        ordering_object_id = constants.ordering_object_id
        ordering_object_id_wise_dict = constants.ordering_object_id_wise_dict
        ordering_object_id_wise_dict[ordering_object_id] = AmazonOrdering(ordering_object_id=ordering_object_id)
        response = ordering_object_id_wise_dict[ordering_object_id].ordering_process_block_wise(email=email,password=password, product_link=product_link)
        ordering_object_id += 1
        logger.info("success")
        return response
    except Exception as e:
        logger.exception("error")
        return e

@router.get(f"/get_ordering_status/{ordering_object_id}", summary="Initiate Amazon Automation")
def main(email:str, password:str, product_link:str):
    try:
        status = ordering_object_id_wise_dict[ordering_object_id].get_ordering_process_status()
        return {"status": status}
    except Exception as e:
        logger.exception("error")
        return e


@router.post(f"/pass_otp_string/{ordering_object_id}", summary="Initiate Amazon Automation")
def pass_otp_string( otp_string:str):
    try:
        status = ordering_object_id_wise_dict[ordering_object_id].pass_otp_string(otp_string=otp_string)
        return {"status": status}
    except Exception as e:
        logger.exception("error")
        return e
