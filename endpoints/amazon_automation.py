from fastapi import APIRouter, HTTPException

import constants
from crud.AmazonOrdering import AmazonOrdering
import logging
from core.logging_utils import setup_logger

log_name = "amazon"
endpoint_device_logger_setup = setup_logger(log_name, level='INFO')
logger = logging.getLogger(log_name)

router = APIRouter()

ordering_object_id_wise_dict={}
ordering_object_id = 0

@router.post("/", summary="Initiate Amazon Automation")
def main(email:str, password:str, product_link:str, quantity:int):
    try:
        global ordering_object_id
        global ordering_object_id_wise_dict
        ordering_object_id = constants.ordering_object_id
        ordering_object_id_wise_dict = constants.ordering_object_id_wise_dict
        ordering_object_id_wise_dict[ordering_object_id] = AmazonOrdering(ordering_object_id=ordering_object_id)
        response = ordering_object_id_wise_dict[ordering_object_id].ordering_process_block_wise(email=email,password=password, product_link=product_link,quantity=quantity)
        constants.ordering_object_id += 1
        logger.info("success")
        return response
    except Exception as e:
        logger.exception(f'Exception in Amazon Ordering: {e}')
        raise HTTPException(status_code=401, detail=f'Exception in Amazon Ordering: {e}')


@router.get(f"/get_ordering_status", summary="Get Order Status")
def get_order_status(ordering_object_id:int):
    try:
        status = constants.ordering_object_id_wise_dict[ordering_object_id].get_ordering_process_status()
        return {"status": status}
    except Exception as e:
        logger.exception(f'Exception in Get Order Status: {e}')
        raise HTTPException(status_code=401, detail=f'Exception in Get Order Status: {e}')


@router.post(f"/pass_otp_string", summary="Get OTP")
def pass_otp_string(otp_string:str):
    try:
        status = ordering_object_id_wise_dict[ordering_object_id].pass_otp_string(otp_string=otp_string)
        return {"status": status}
    except Exception as e:
        logger.exception(f'Exception in Get OTP: {e}')
        raise HTTPException(status_code=401, detail=f'Exception in Get OTP: {e}')
