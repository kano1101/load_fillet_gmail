from difflib import SequenceMatcher
from utils import replace_whitespace

import injector
from i_interactor import ICalcAndWriteMixtureSimilarityInteractor, IRepository, IPresenter
from i_parameter import IParameterInteractor


class SimilarityInputData:
    def __init__(self, adapter_names, product_names, article_names, package_names) -> None:
        self.adapter_names = adapter_names
        self.product_names = product_names
        self.article_names = article_names
        self.package_names = package_names

    def get_adapter_names(self):
        return self.adapter_names

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
    def __init__(self, similarities, adapters) -> None:
        self.similarities = similarities
        self.adapters = adapters

    def get_similarities(self):
        return self.similarities

    def get_adapters(self):
        return self.adapters


class CalcAndWriteMixtureSimilarityInteractor(ICalcAndWriteMixtureSimilarityInteractor[SimilarityInputData]):
    @injector.inject
    def __init__(self, parameter: IParameterInteractor, repository: IRepository, presenter: IPresenter) -> None:
        self.parameter = parameter
        self.repository = repository
        self.presenter = presenter

    def handle(self, input_data: SimilarityInputData):
        adapter_names = input_data.get_adapter_names()

        product_names = input_data.get_product_names()
        article_names = input_data.get_article_names()
        package_names = input_data.get_package_names()

        buttocks_names = product_names + article_names + package_names

        similarities = []
        adapters = []

        for adapter_name in adapter_names:
            adapter_name_with_whitespace = replace_whitespace(adapter_name)

            highest_similarity = 0
            most_similar_mixture = ""

            for buttocks_name in buttocks_names:

                # ここにのちにアダプタ検索も追加
                buttocks_with_whitespace = replace_whitespace(buttocks_name)

                similarity = SequenceMatcher(None, adapter_name_with_whitespace, buttocks_with_whitespace).ratio()
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    most_similar_mixture = buttocks_with_whitespace

            similarities.append(highest_similarity)
            adapters.append(most_similar_mixture)

        save_data = SaveSimilarityData(similarities, adapters)
        self.repository.save_similarity_and_adapter_columns(save_data)

        # output_result = result
        #
        # output_data = OutputData(output_result)
        # self.presenter.output(output_data)
