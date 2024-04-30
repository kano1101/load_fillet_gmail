import injector

from helper import get_credentials_cover, get_soups_with_gmail_labels

from calc_and_write_mixture_similarity_interactor import InputData
from i_parameter import IParameterController
from i_interactor import IWriteMixtureWithAmountInteractor
from i_interactor import ICalcAndWriteMixtureSimilarityInteractor


class Controller:
    @injector.inject
    def __init__(
        self,
        parameter: IParameterController,
        write_mixture_with_amount_interactor: IWriteMixtureWithAmountInteractor,
        calc_and_write_mixture_similarity_interactor: ICalcAndWriteMixtureSimilarityInteractor,
    ):
        self.parameter = parameter
        self.write_mixture_with_amount_interactor = write_mixture_with_amount_interactor
        self.calc_and_write_mixture_similarity_interactor = calc_and_write_mixture_similarity_interactor

    # def write_product_with_amount(self, labels):
    #     labels = self.parameter.get_labels()
    #     mails = get_soups_with_gmail_labels(labels)
    #
    #     input_data = InputData(mails)
    #
    #     self.interactor.handle(input_data)

    def write_mixture_with_amount(self):
        labels = self.parameter.get_labels()
        mails = get_soups_with_gmail_labels(labels)

        input_data = InputData(mails)

        self.write_mixture_with_amount_interactor.handle(input_data)

    def calc_and_write_mixture_similarity(self):
        self.calc_and_write_mixture_similarity_interactor.handle()
