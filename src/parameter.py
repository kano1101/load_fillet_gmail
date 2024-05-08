import os

from i_parameter import IParameter, IControllerParameter, IRepositoryParameter, IInteractorParameter
import injector

from helper import open_spreadsheet_on_default_account, get_credentials_cover, get_scopes


class Parameter(IParameter):
    @injector.inject
    def __init__(self):
        pass


class ControllerParameter(IControllerParameter):
    @injector.inject
    def __init__(self, parameter: IParameter):
        self.parameter = parameter
        # self.label = "2024焼菓子ギャラリー"
        self.label = os.environ.get('LABEL_NAME')

    def get_label(self):
        return self.label


class InteractorParameter(IInteractorParameter):
    @injector.inject
    def __init__(self, parameter: IParameter):
        self.parameter = parameter


class RepositoryParameter(IRepositoryParameter):
    @injector.inject
    def __init__(self, parameter: IParameter):
        self.parameter = parameter
        scopes = get_scopes()
        self.creds = get_credentials_cover(scopes)
        spreadsheet_id = os.environ.get('SPREADSHEET_ID')
        ss = open_spreadsheet_on_default_account(spreadsheet_id)
        self.output_product_worksheet = ss.worksheet("製品")
        self.output_expand_worksheet = ss.worksheet("領域展開")

    def get_output_product_worksheet(self):
        return self.output_product_worksheet

    def get_output_expand_worksheet(self):
        return self.output_expand_worksheet
