# eforms website class

import arrow

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import all_of, alert_is_present, invisibility_of_element_located
from selenium.common.exceptions import TimeoutException

from .web import Driver, Element, Page, XPATH, ID, URL
from .exceptions import EformsFailure, LoginTimeout

DEFAULT_LOGIN_TIMEOUT = 60


class EForms(Driver):

    def __init__(self, data, timeout=DEFAULT_LOGIN_TIMEOUT):
        self.login_state = False
        self.data = data
        self.login_timeout = timeout
        super().__init__()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.quit()

    def front_page(self):
        return Page(
            driver=self,
            elements=dict(
                input_username=Element(XPATH, '//*[@id="pt1:it2::content"]', 30),
                input_password=Element(XPATH, '//*[@id="pt1:it1::content"]', 5),
                button_login_ok=Element(XPATH, '//*[@id="pt1:cb1"]', 10),
                div_loading_documents=Element(ID, 'pt1:r1:0:t2::sm', 60),
                div_loading_pages=Element(ID, 'pt1:r1:0:t2::sm', 60),
                div_form_picker=Element(ID, 'pt1:r1:0:c2::sn', 60),
                url_front_page=Element(URL, 'https://eforms.atf.gov/EForms', 60)
            )
        )

    def login(self):
        logger.info('Login...')

        if self.logged_in:
            raise EformsFailure('illegal duplicate login')

        self.login_time = arrow.utcnow()
        self.page = self.front_page()

        # open front page
        self.page.url.get()

        # fill username, password and click submit
        self.page.input_username.fill(self.username)
        self.page.input_password.fill(self.password)
        self.page.button_submit.click()

        # wait for warning popup and click it
        self.page.button_accept.hover()
        self.page.button_accept.click()

        # wait for login complete conditions
        self.wait_front_page_load()

        self.logged_in = True

        logging.info(f"login complete {arrow.utcnow() - self.login_time}")

    def wait_front_page_load(self, timeout=DEFAULT_LOGIN_TIMEOUT):
        """wait for front page load complete, returning list of condition return values or False on timeout"""
        conditions = [
            invisibility_of_element_located(self.page.button_accept.locator),
            invisibility_of_element_located(self.page.div_loading_documents.locator),
            invisibility_of_element_located(self.page.div_loading_pages.locator),
            lambda x: self.selenium_driver.execute_script('return document.readyState') == 'complete'
        ]
        ret = WebDriverWait(self, timeout).until(all_of(conditions), message='login timeout')
