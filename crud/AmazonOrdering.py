from selenium import webdriver
import time
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

    def __init__(self):
        self.is_otp_required = False
        self.web = None
        self.captcha = None
        self.login = None
        self.email = None
        self.password = None
        self.buy_btn = None
        self.product_link = None
        self.ordering_process_thread_object = None


    def start_ordering_process_thread(self,email:str,password:str,product_link:str):
        try:
            self.email = email
            self.password = password
            self.product_link = product_link
            self.ordering_process_thread_object = threading.Thread(target=self.ordering_process)
        except Exception as e:
            return e

    def ordering_process(self):
        self.web = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.web.get(self.product_link)
        self.checking_for_any_captcha()
        pass

    def captcha_or_not(self):
        try:
            self.captcha = self.web.find_element(By.XPATH, "/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[2]/input")
            return self.captcha
        except:
            try:
                self.buy_btn = self.web.find_element(By.XPATH,
                                       "/html/body/div[2]/div/div[6]/div[3]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[39]/div/div/span/span/input")
                return self.buy_btn
            except Exception as e:
                return e

    def checking_for_any_captcha(self):
        try:
            element = self.captcha_or_not()
            if element == self.captcha:
                self.if_captcha()
            elif element == self.buy_btn:
                self.placing_order()
            else:
                print(element)

        except Exception as e:
            print("in exception")
            print(e)

    def if_captcha(self):
        try:
            captcha_success = WebDriverWait(self.web, 120).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[2]/div/div[6]/div[3]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[39]/div/div/span/span/input"))
            )
            if captcha_success:
                self.placing_order()
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
            time.sleep(1)

            password = self.web.find_element(By.XPATH,
                                        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/form/div/div[1]/input")
            password.send_keys(self.password)

            login = self.web.find_element(By.XPATH,
                                     "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/form/div/div[2]/span/span/input")
            login.click()
            self.check_for_otp()
        except Exception as e:
            return e

    def check_for_otp(self):
        try:
            otp_input_field = WebDriverWait(self.web, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[3]/form/div[1]/div/div/span[1]/div/input"))
            )

            if otp_input_field:
                otp_success_field = WebDriverWait(self.web, 25).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input"))
                )
                self.cash_payment()
        except Exception as e:
            self.cash_payment()

    def search_element(self):
        try:
            search = self.web.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")
            search.send_keys("a4 size paper")

            time.sleep(2)

            search_btn = self.web.find_element(By.XPATH,
                                          "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input")
            search_btn.click()

            self.placing_order()
        except Exception as e:
            return e

    def placing_order(self):
        try:
            time.sleep(2)
            buy_btn = self.web.find_element(By.XPATH,
                                       "/html/body/div[2]/div/div[6]/div[3]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[39]/div/div/span/span/input")
            buy_btn.click()

            time.sleep(2)
            self.login_user()
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
                    (By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]/div/div/div[2]/div/div[2]/div/div/form/div/div[2]/div/span/span/input"))
            )

            payment_selection = self.web.find_element(By.XPATH,
                                                      "/html/body/div[5]/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]/div/div/div[2]/div/div[2]/div/div/form/div/div[2]/div/span/span/input")
            payment_selection.click()

            time.sleep(10)

            # order_now = self.web.find_element(By.XPATH,
            #                                   "/html/body/div[5]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div/span")
            # order_now.click()
            time.sleep(5)

        except Exception as e:
            return e