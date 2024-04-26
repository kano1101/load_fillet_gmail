import injector

from helper import get_credentials_cover, get_soups_with_gmail_labels

from interactor import IInteractor
from interactor import InputData
from i_parameter import IParameterController


class Controller:
    @injector.inject
    def __init__(self, parameter: IParameterController, interactor: IInteractor):
        self.parameter = parameter
        self.interactor = interactor

    def write_mixture_with_similarity(self):
        labels = self.parameter.get_labels()
        mails = get_soups_with_gmail_labels(labels)

        input_data = InputData(mails)

        self.interactor.handle(input_data)

    # def write_product_with_amount(self, labels):
    #     labels = self.parameter.get_labels()
    #     mails = get_soups_with_gmail_labels(labels)
    #
    #     input_data = InputData(mails)
    #
    #     self.interactor.handle(input_data)
