import random
import logging
import string
from .time_util import sleep
from .util import check_kill_process, gen_random_string
from .login_util import login_browser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Remote
from socialcommons.file_manager import get_logfolder
from socialcommons.file_manager import get_workspace
from socialcommons.browser import set_selenium_local_session
from socialcommons.exceptions import SocialPyError
from .settings import Settings
import traceback
from .database_engine import get_database
from pathlib import Path


class VivaldiAlive:
    def __init__(
        self,
        vivaldi,
        vivaldi_password,
        headless=False,
        memory_hogging_processes=["Fire", "Chrome", "chromedriver", "DrCleaner"],
    ):
        self.vivaldi = vivaldi
        self.vivaldi_password = vivaldi_password
        self.multi_logs = True
        self.logfolder = get_logfolder(self.vivaldi, self.multi_logs, Settings)
        self.get_vivaldialive_logger()
        for mhp in memory_hogging_processes:
            check_kill_process(mhp, self.logger)
        self.page_delay = 25
        self.use_firefox = headless
        self.headless_browser = headless
        self.disable_image_load = False
        self.browser_profile_path = None
        self.proxy_chrome_extension = None
        self.proxy_address = None
        self.proxy_address = None
        Settings.profile["name"] = self.vivaldi

        if not get_workspace(Settings):
            raise SocialPyError("Oh no! I don't have a workspace to work at :'(")

        get_database(Settings, make=True)
        self.set_selenium_local_session(Settings)

    def get_vivaldialive_logger(self):
        self.logger = logging.getLogger(self.vivaldi)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler("{}general.log".format(self.logfolder))
        file_handler.setLevel(logging.DEBUG)
        extra = {"vivaldi": self.vivaldi}
        logger_formatter = logging.Formatter(
            "%(levelname)s [%(asctime)s] [VivaldiAlive:%(vivaldi)s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(logger_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logger_formatter)
        self.logger.addHandler(console_handler)

        self.logger = logging.LoggerAdapter(self.logger, extra)

    def set_selenium_local_session(self, Settings):
        self.browser, err_msg = set_selenium_local_session(
            self.proxy_address,
            self.proxy_address,
            self.proxy_chrome_extension,
            self.headless_browser,
            self.use_firefox,
            self.browser_profile_path,
            self.disable_image_load,
            self.page_delay,
            self.logger,
            Settings,
        )
        if len(err_msg) > 0:
            raise SocialPyError(err_msg)

    def send_a_mail(self):
        sleep(5)
        try:
            compose_btn = self.browser.find_element_by_xpath(
                "//*[@id='rcmbtn112']"
            )                
            ActionChains(self.browser).move_to_element(
                compose_btn
            ).click().perform()
            self.logger.info("Clicked Compose")
            sleep(5)
            to_ele = self.browser.find_element_by_xpath(
                "//*[@id='_to']"
            )
            ActionChains(self.browser).move_to_element(to_ele).click().perform()
            ActionChains(self.browser).move_to_element(to_ele).click().send_keys(
                "ishandutta2007@gmail.com"
            ).perform()
            self.logger.info("Entered To: ishandutta2007@gmail.com")
            subjectbox_ele = self.browser.find_element_by_xpath(
                "//*[@id='compose-subject']"
            )
            ActionChains(self.browser).move_to_element(
                subjectbox_ele
            ).click().perform()
            ActionChains(self.browser).move_to_element(
                subjectbox_ele
            ).click().send_keys(
                "abhi vivaldiwale zinda hai "
                + gen_random_string(8, string.digits)
                + gen_random_string(15, string.ascii_letters)
            ).perform()

            body_ele = self.browser.find_element_by_xpath(
                "//*[@id='composebody']"
            )
            ActionChains(self.browser).move_to_element(
                body_ele
            ).click().perform()
            ActionChains(self.browser).move_to_element(
                body_ele
            ).click().send_keys(
                "Some blabla body "
                + gen_random_string(8, string.digits)
                + gen_random_string(15, string.ascii_letters)
            ).perform()

            send_btn = self.browser.find_element_by_xpath(
                "//*[@id='rcmbtn112']"
            )
            ActionChains(self.browser).move_to_element(send_btn).click().perform()
            self.logger.info("Clicked Send")
            sleep(5)
        except Exception as e:
            traceback.print_exc()
            raise e
        sleep(5)

    def check_mail(self):
        try:
            if login_browser(
                self.vivaldi,
                self.vivaldi_password,
                self.logfolder,
                self.browser,
                self.logger,
            ):
                print("Login Successful")
                self.send_a_mail()
            else:
                print("Login Failed")
            if self.browser:
                self.browser.quit()
        except Exception as e:
            traceback.print_exc()
            if self.browser:
                self.browser.quit()
            raise e
