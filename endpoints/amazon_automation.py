
from fastapi import APIRouter
from crud.AmazonOrdering import AmazonOrdering

router = APIRouter()

@router.post("/", summary="Initiate Amazon Automation")
def main(email:str, password:str, product_link:str):
    try:
        amazon_ordering = AmazonOrdering()
        response = amazon_ordering.start_ordering_process_thread(email=email,password=password, product_link=product_link)
        return response
    except Exception as e:
        return e
