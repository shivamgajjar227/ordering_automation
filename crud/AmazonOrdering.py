import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi import APIRouter
import threading
import time

router = APIRouter()

class AmazonOrdering:
    STATUS_PROCESS_STARTED = 1
    STATUS_PRODUCT_FOUND = 2
    STATUS_CHECKING_FOR_CAPTCHA = 3
    STATUS_CAPTCHA_FOUND = 4
    STATUS_CAPTCHA_SUCCESSFUL = 5
    STATUS_CAPTCHA_FAILED = 6
    STATUS_PROCESS_LOGIN_USER = 7
    STATUS_LOGIN_DONE = 8
    STATUS_CHECKING_FOR_OTP = 9
    STATUS_ENTER_OTP = 10
    STATUS_OTP_SUCCESSFUL = 11
    STATUS_OTP_FAILED = 12
    STATUS_PLACING_ORDER = 13
    STATUS_ORDER_PLACED = 14

    def __init__(self, ordering_object_id):
        self.is_otp_required = False
        self.web = None
        self.captcha = None
        self.login = None
        self.email = None
        self.password = None
        self.buy_btn = None
        self.product_link = None
        self.ordering_process_thread_object = None
        self.ordering_process_status = 0
        self.ordering_object_id = None
        self.element = None
        self.success_captcha = 0
        self.otp_string = None

    def ordering_process_block_wise(self, email: str, password: str, product_link: str):
        self.email = email
        self.password = password
        self.product_link = product_link


        """Process started"""
        self.ordering_process_status = self.STATUS_PROCESS_STARTED


        """ Opening product link"""
        self.start_ordering_process_thread()
        self.ordering_process_status = self.STATUS_PRODUCT_FOUND


        """ Checking for captcha"""
        self.ordering_process_status = self.STATUS_CHECKING_FOR_CAPTCHA
        captcha = self.checking_for_any_captcha()
        while self.success_captcha != 1:
            if captcha:
                self.ordering_process_status = self.STATUS_CAPTCHA_FOUND
                self.success_captcha = self.input_captcha()
                if self.success_captcha == 1:
                    self.ordering_process_status = self.STATUS_CAPTCHA_SUCCESSFUL
                else:
                    self.ordering_process_status = self.STATUS_CAPTCHA_FAILED


        """ BUYING THE PRODUCT"""
        self.buying_product()


        """ LOGGING IN"""
        self.ordering_process_status = self.STATUS_PROCESS_LOGIN_USER
        self.login_user()
        self.ordering_process_status = self.STATUS_LOGIN_DONE


        """ CHECKING FOR OTP """
        self.ordering_process_status = self.STATUS_CHECKING_FOR_OTP
        otp = self.check_for_otp()
        while otp != 1:
            self.ordering_process_status = self.STATUS_ENTER_OTP
            while not self.otp_string is None:
                time.sleep(0.3)
            otp_success = self.input_otp(otp=self.otp_string)
            if otp_success:
                self.ordering_process_status = self.STATUS_OTP_SUCCESSFUL
            else:
                self.ordering_process_status = self.STATUS_OTP_FAILED
        # otp_input_field = "/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/form/div[2]/div[2]/div/input"
        #otp_submit = "/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/form/div[4]/span/span/input"


        """ PLACING ORDER """
        self.ordering_process_status = self.STATUS_PLACING_ORDER
        self.cash_payment()
        self.ordering_process_status = self.STATUS_ORDER_PLACED


    def start_ordering_process_thread(self):
        try:
            self.ordering_process_thread_object = threading.Thread(target=self.ordering_process())
        except Exception as e:
            return e

    def pass_otp_string(self, otp_string):
        try:
            self.otp_string = otp_string
        except Exception as e:
            return e

    def ordering_process(self):
        try:
            self.web = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            self.web.get(self.product_link)
        except Exception as e:
            return (f"no product found, error: {e}")

    def checking_for_any_captcha(self):
        try:
            self.element = self.captcha_or_not()
            if self.element == self.captcha:
                return 1
            elif self.element == self.buy_btn:
                return 0
        except Exception as e:
            return e

    def captcha_or_not(self):
        try:
            self.captcha = self.web.find_element(By.XPATH,
                                                 "/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[2]/input")
            return self.captcha
        except:
            try:
                self.buy_btn = self.web.find_element(By.XPATH,
                                                     "/html/body/div[2]/div/div[6]/div[3]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[39]/div/div/span/span/input")
                return self.buy_btn
            except Exception as e:
                return e

    def input_captcha(self):
        try:
            captcha_success = WebDriverWait(self.web, 120).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[2]/div/div[6]/div[3]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[39]/div/div/span/span/input"))
            )
            if captcha_success:
                return 1
        except Exception as e:
            return e

    def buying_product(self):
        try:
            time.sleep(2)
            buy_btn = self.web.find_element(By.XPATH,
                                            "/html/body/div[2]/div/div[6]/div[3]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[39]/div/div/span/span/input")
            buy_btn.click()
            time.sleep(1)
        except Exception as e:
            return e

    def login_user(self):
        try:
            username = self.web.find_element(By.XPATH,
                                             "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div[1]/form/div/div/div/div[1]/input[1]")
            username.send_keys(self.email)

            submit = self.web.find_element(By.XPATH,
                                           "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[2]/div[1]/form/div/div/div/div[2]/span/span/input ")
            submit.click()
            time.sleep(2)

            password = self.web.find_element(By.XPATH,
                                             "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/form/div/div[1]/input")
            password.send_keys(self.password)

            login = self.web.find_element(By.XPATH,
                                          "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/form/div/div[2]/span/span/input")
            login.click()
        except Exception as e:
            return e

    def check_for_otp(self):
        try:
            otp_input_field = WebDriverWait(self.web, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[3]/form/div[1]/div/div/span[1]/div/input"))
            )

            if otp_input_field:
                return 1
            return 0

        except Exception as e:
            return 0

    def input_otp(self,otp:str):
        try:
            otp_input_field = self.web.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/form/div[2]/div[2]/div/input")
            otp_input_field.send_keys(otp)

            submit_otp = self.web.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/form/div[4]/span/span/input")
            submit_otp.click()

            success_otp = WebDriverWait(self.web, 25).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "/html/body/div[5]/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]/div/div/div[2]/div/div[2]/div/div/form/div/div[1]/div/div[2]/div[6]/div/div/div/div/div[1]/div/label/input"))
            )
            if success_otp:
                return 1
            return 0
        except Exception as e:
            return e

    def cash_payment(self):
        try:
            cash_pay = self.web.find_element(By.XPATH,
                                             "/html/body/div[5]/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]/div/div/div[2]/div/div[2]/div/div/form/div/div[1]/div/div[2]/div[6]/div/div/div/div/div[1]/div/label/input")
            cash_pay.click()

            time.sleep(2)

            payment_page = WebDriverWait(self.web, 25).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "/html/body/div[5]/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]/div/div/div[2]/div/div[2]/div/div/form/div/div[2]/div/span/span/input"))
            )

            payment_selection = self.web.find_element(By.XPATH,
                                                      "/html/body/div[5]/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]/div/div/div[2]/div/div[2]/div/div/form/div/div[2]/div/span/span/input")
            payment_selection.click()

            time.sleep(3)

            # order_now = self.web.find_element(By.XPATH,
            #                                   "/html/body/div[5]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div/span")
            # order_now.click()
            time.sleep(2)

        except Exception as e:
            return e

    '''def search_element(self):
            try:
                search = self.web.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")
                search.send_keys("a4 size paper")

                time.sleep(2)

                search_btn = self.web.find_element(By.XPATH,
                                              "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input")
                search_btn.click()

                self.placing_order()
            except Exception as e:
                return e'''

    def get_ordering_process_status(self):
        return self.ordering_process_status
