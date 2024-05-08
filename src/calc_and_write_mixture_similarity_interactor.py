from flexa import Flexa
from difflib import SequenceMatcher
from utils import replace_whitespace

import injector
from i_interactor import ICalcAndWriteMixtureSimilarityInteractor, IRepository, IPresenter
from i_parameter import IInteractorParameter


class SimilarityInputData:
    def __init__(self, similar_names, product_names, article_names, package_names) -> None:
        self.similar_names = similar_names
        self.product_names = product_names
        self.article_names = article_names
        self.package_names = package_names

    def get_similar_names(self):
        return self.similar_names

    def get_product_names(self):
        return self.product_names

    def get_article_names(self):
        return self.article_names

    def get_package_names(self):
        return self.package_names


class SimilarityOutputData:
    def __init__(self, data) -> None:
        self.data = data


class SaveSimilarityData:
    def __init__(self, similarities, similar_names) -> None:
        self.similarities = similarities
        self.similar_names = similar_names

    def get_similarities(self):
        return self.similarities

    def get_similar_names(self):
        return self.similar_names


class CalcAndWriteMixtureSimilarityInteractor(ICalcAndWriteMixtureSimilarityInteractor[SimilarityInputData]):
    @injector.inject
    def __init__(self, parameter: IInteractorParameter, repository: IRepository, presenter: IPresenter) -> None:
        self.parameter = parameter
        self.repository = repository
        self.presenter = presenter
        self.flexa = Flexa()

    def add_to_flexa(self, buttocks_names):
        for buttocks_name in buttocks_names:
            self.flexa.set(buttocks_name, buttocks_name)

    def handle(self, input_data: SimilarityInputData):
        similar_names = input_data.get_similar_names()

        product_names = input_data.get_product_names()
        article_names = input_data.get_article_names()
        package_names = input_data.get_package_names()

        buttocks_names = product_names + article_names + package_names

        similarities = []
        adapter_names = []

        for similar_name in similar_names:
            similar_name_with_whitespace = replace_whitespace(similar_name)

            highest_similarity = 0
            most_similar_adapter_name = ""

            for buttocks_name in buttocks_names:

                # ここにのちにアダプタ検索も追加


                buttocks_with_whitespace = replace_whitespace(buttocks_name)

                similarity = SequenceMatcher(None, similar_name_with_whitespace, buttocks_with_whitespace).ratio()
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    most_similar_adapter_name = buttocks_with_whitespace

            similarities.append(highest_similarity)
            adapter_names.append(most_similar_adapter_name)

        save_data = SaveSimilarityData(similarities, adapter_names)
        self.repository.save_similarity_and_adapter_columns(save_data)

        # output_result = result
        #
        # output_data = OutputData(output_result)
        # self.presenter.output(output_data)
