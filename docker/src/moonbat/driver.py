# browser.py

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.by import By

import logging
logger.logging.getlogger(__name__)

DEFAULT_IMPLICIT_WAIT=30
DEFAULT_FIND_ELEMENT_TIMEOUT=30
DEFAULT_GET_TIMEOUT=60
DEFAULT_CLICK_TIMEOUT=30
DEFAULT_CLOSE_TIMEOUT=30
DEFAULT_QUIT_TIMEOUT=30

SELENIUM_DOWNLOAD_PATH='/var/download'

class Driver(AbstractEventListener):

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option(
            "prefs", {
                "download.default_directory": SELENIUM_DOWNLOAD_PATH,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
        )
        self.driver = EventFiringWebDriver(
            webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                desired_capabilities=self.chrome_options.to_capabilities()
            )
        )
        self.driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
        self.driver.fullscreen_window()

    def after_click(self, element, driver):
        logging.info(f"Element {element} clicked on {driver}")

    def after_find(self, element, driver):
        logging.info(f"Element {element} found on {driver}")

    def after_navigate_to(self, url, driver):
        logging.info(f"Navigated to {url} on {driver}")

    def on_exception(self, exception, driver):
        logging.info(f"Exception {url} raised by {driver}")

    def find_element(self, value, timeout=DEFAULT_FIND_ELEMENT_TIMEOUT):
        if value.startswith('/'):
            by = By.XPATH
        else:
            by = By.tag_name
        element = self.driver.find_element(by, value)
        return element

    def get(self, url, timeout=DEFAULT_GET_TIMEOUT):
        self.driver.get(url)

    def close(self, timeout=DEFAULT_CLOSE_TIMEOUT):
        self.driver.close()

    def quit(self, timeout=DEFAULT_QUIT_TIMEOUT):
        self.driver.quit()
