# nfatools form3 job controller

from .eforms import EForms
from time import Sleep


class Job():

    def __init__(self, db, job_id):
        self.db = db
        self.job_id = job_id

    def read_form_data(self):
        self.data = dict(username='foo', password='moo')

    def run(self, out):
        try:
            with EForms(self.data) as eforms:
                Sleep(5)
                ret = 200
        except NFAToolsException as ex:
            logger.error(ex)
            ret = 500
        return ret
