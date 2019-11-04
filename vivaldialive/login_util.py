import random
import os
import signal
import logging
import pickle
import re
import pprint as pp
import sqlite3
import math
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Remote
from .time_util import sleep
from socialcommons.file_manager import get_logfolder
from socialcommons.file_manager import get_workspace
from socialcommons.browser import set_selenium_local_session
from socialcommons.exceptions import SocialPyError
from .settings import Settings
import traceback
from .database_engine import get_database
import configparser
from .time_util import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import MoveTargetOutOfBoundsException


def login_browser(vivaldi, vivaldi_password, logfolder, browser, logger):
    try:
        browser.get("https://imap.vivaldi.net/webmail/")
        sleep(2)

        input_vivaldi = browser.find_element_by_xpath("//input[@id='rcmloginuser']")
        (
            ActionChains(browser)
            .move_to_element(input_vivaldi)
            .click()
            .send_keys(vivaldi)
            .perform()
        )
        logger.info("Entered Email: {}".format(vivaldi))
        sleep(1)

        input_pass = browser.find_element_by_xpath("//input[@id='rcmloginpwd']")
        (
            ActionChains(browser)
            .move_to_element(input_pass)
            .click()
            .send_keys(vivaldi_password)
            .perform()
        )
        logger.info("Entered Pass: {}".format(vivaldi_password))
        sleep(1)

        submit_pass = browser.find_element_by_xpath("//input[@id='rcmloginsubmit']")
        (ActionChains(browser).move_to_element(submit_pass).click().perform())
        logger.info("Submitted")

        sleep(3)

    except Exception as e:
        logger.error(e)
        if browser:
            browser.quit()
        return False

    return True
