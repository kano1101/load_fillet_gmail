import os

from i_parameter import IParameter, IParameterController, IParameterRepository
import injector

from src.helper import open_spreadsheet_on_default_account, get_credentials_cover


class ParameterController(IParameterController):
    @injector.inject
    def __init__(self, parameter: IParameter):
        self.parameter = parameter
        self.labels = ["焼菓子ギャラリー"]

    def get_labels(self):
        return self.labels


class ParameterRepository(IParameterRepository):
    @injector.inject
    def __init__(self, parameter: IParameter):
        self.parameter = parameter
        scopes = [
            'https://www.googleapis.com/auth/script.projects',
            'https://www.googleapis.com/auth/spreadsheets',
        ]
        self.creds = get_credentials_cover(scopes)
        spreadsheet_id = os.environ.get('SPREADSHEET_ID')
        ss = open_spreadsheet_on_default_account(spreadsheet_id)
        self.output_worksheet = ss.worksheet("領域展開")

    def get_output_worksheet(self):
        return self.labels
