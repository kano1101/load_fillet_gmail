import injector

from i_interactor import IRepository
from i_parameter import IParameterRepository
from write_mixture_with_amount_interactor import SaveMixtureWithAmountData
from calc_and_write_mixture_similarity_interactor import SaveSimilarityData
from utils import index_to_col_name, to_column_values


class Repository(IRepository[SaveMixtureWithAmountData]):
    @injector.inject
    def __init__(self, parameter: IParameterRepository):
        self.parameter = parameter
        self.output_worksheet = self.parameter.get_output_worksheet()

    def save_mixture_and_amount_columns(self, save_data: SaveMixtureWithAmountData):
        self.output_worksheet.batch_clear(["B2:B", "G2:I"])
        self.update_mixture_and_amount_columns(save_data)

    def save_similarity_and_adapter_columns(self, save_data: SaveSimilarityData):
        self.output_worksheet.batch_clear(["J2:K"])
        self.update_similarity_and_adapter_columns(save_data)

    def update_mixture_and_amount_columns(self, save_data: SaveMixtureWithAmountData):
        column_numbers = [1, 6, 7, 8]  # 0を含める
        column_length = 11

        data = save_data.get_rows()
        for i in range(0, column_length):
            if i in column_numbers:
                tup_index = column_numbers.index(i)
                values = [[tup[tup_index]] for tup in data]
                self.update_column(values, i)

    def update_similarity_and_adapter_columns(self, save_data: SaveSimilarityData):
        similarities = save_data.get_similarities()
        adapters = save_data.get_adapters()

        similarity_column_values = to_column_values(similarities)
        adapter_column_values = to_column_values(adapters)

        self.update_column(similarity_column_values, 9)
        self.update_column(adapter_column_values, 10)

    def update_column(self, values, index):
        for row_value in values:
            if len(row_value) != 1:
                raise ValueError("update_columnでは複数列同時更新できません。1列のみの更新に限定してください")
        column_char = index_to_col_name(index)
        self.output_worksheet.update(range_name=f"{column_char}2", values=values)
