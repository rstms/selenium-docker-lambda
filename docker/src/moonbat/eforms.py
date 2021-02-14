# eforms website class

import arrow

from driver import Driver 
from page import Page
from element import Element

DEFAULT_LOGIN_TIMEOUT=60

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
        return Page(driver=self, elements=dict(
            input_username=Element('//*[@id="pt1:it2::content"]', 30),
            input_password=Element('//*[@id="pt1:it1::content"]', 5),
            button_login_ok=Element('//*[@id="pt1:cb1"]', 10),
            div_loading_documents=Element('pt1:r1:0:t2::sm', 60),
            div_loading_pages=Element('pt1:r1:0:t2::sm', 60),
            div_form_picker=Element('pt1:r1:0:c2::sn', 60),
            url_front_page=Element('https://eforms.atf.gov/EForms', 60)
        ))

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

    def wait_front_page_load(self):
        self.driver

        

        self.get_element('login', 'usrname_txtbox', 20).fill(username)
        self.get_element('login', 'passwd_txtbox', 5).fill(password)
        self.get_element('login', 'submit_btn', 10).click(wait_conditions=[
            ('element_visible', DomData.get_id('login', 'accept_btn')),
        ])
        accept_button = self.get_element('login', 'accept_btn', self.login_wait, True)
        accept_button.hover()
        if wait:
            time.sleep(wait)
        logger.info(f"clicking the accept_button...")

        ret = accept_button.click(
            attempts=1,
            wait_conditions=[
                ('element_invisible', DomData.get_id('login', 'accept_btn')), ('element_invisible', 'pt1:r1:0:t2::sm'),
                ('element_invisible', 'pt1:r1:0:c2::sm'), ('document_ready', True)
            ]
        )


        if ret:
            logger.info(f"{success_strings['login']}")
            logger.debug(f"login success for account '{username}' elapsed={arrow.utcnow() - self.login_time}")
        else:
            logger.info(f"Login failed.")
        self.login_state = ret
        return ret
