import injector

from helper import get_soups_with_gmail_label, get_worksheet_in_recipe_support, get_recipe_support_spreadsheet

from write_product_summary_interactor import ProductSummaryInputData
from write_mixture_with_amount_interactor import MixtureWithAmountInputData
from calc_and_write_mixture_similarity_interactor import SimilarityInputData
from i_parameter import IParameterController
from i_interactor import IWriteProductSummaryInteractor
from i_interactor import IWriteMixtureWithAmountInteractor
from i_interactor import ICalcAndWriteMixtureSimilarityInteractor


class Controller:
    @injector.inject
    def __init__(
        self,
        parameter: IParameterController,
        write_product_summary_interactor: IWriteProductSummaryInteractor,
        write_mixture_with_amount_interactor: IWriteMixtureWithAmountInteractor,
        calc_and_write_mixture_similarity_interactor: ICalcAndWriteMixtureSimilarityInteractor,
    ):
        print("Controller start")
        self.parameter = parameter
        self.write_product_summary_interactor = write_product_summary_interactor
        self.write_mixture_with_amount_interactor = write_mixture_with_amount_interactor
        self.calc_and_write_mixture_similarity_interactor = calc_and_write_mixture_similarity_interactor
        print("Controller end")

    def write_product_if_necessary(self):
        print("Controller.write_product_if_necessary start")
        label = self.parameter.get_label()

        mails = get_soups_with_gmail_label(label)

        input_data = ProductSummaryInputData(mails, label)
        self.write_product_summary_interactor.handle(input_data)

    def write_mixture_with_amount(self):
        label = self.parameter.get_label()

        mails = get_soups_with_gmail_label(label)

        input_data = MixtureWithAmountInputData(mails)

        self.write_mixture_with_amount_interactor.handle(input_data)

    def calc_and_write_mixture_similarity(self):
        # 類似度を求める
        ss = get_recipe_support_spreadsheet()

        similar_worksheet = get_worksheet_in_recipe_support(ss, "領域展開")
        product_worksheet = get_worksheet_in_recipe_support(ss, "製品")
        article_worksheet = get_worksheet_in_recipe_support(ss, "材料")
        package_worksheet = get_worksheet_in_recipe_support(ss, "包材")

        similar_names = similar_worksheet.col_values(6)[1:] # 1始まり(A列はcol_values(1)
        product_names = product_worksheet.col_values(2)[1:]
        article_names = article_worksheet.col_values(2)[1:]
        package_names = package_worksheet.col_values(2)[1:]

        input_data = SimilarityInputData(similar_names, product_names, article_names, package_names)

        self.calc_and_write_mixture_similarity_interactor.handle(input_data)
