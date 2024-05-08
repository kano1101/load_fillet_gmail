import injector

from i_interactor import IRepository
from i_parameter import IRepositoryParameter
from write_product_summary_interactor import SaveProductSummaryData
from write_mixture_with_amount_interactor import SaveMixtureWithAmountData
from calc_and_write_mixture_similarity_interactor import SaveSimilarityData
from utils import index_to_col_name, to_column_values, max_value_in_column, to_num


def exists_product_and_label(added_product_summary_values, product_name, label):
    for added_product_summary_value in added_product_summary_values:
        added_product_name = added_product_summary_value[1]
        added_label = added_product_summary_value[2]
        if product_name == added_product_name and label == added_label:
            return True
    return False


class Repository(IRepository[SaveMixtureWithAmountData]):
    @injector.inject
    def __init__(self, parameter: IRepositoryParameter):
        self.parameter = parameter
        self.output_product_worksheet = self.parameter.get_output_product_worksheet()
        self.output_expand_worksheet = self.parameter.get_output_expand_worksheet()

    def save_product_summary_direct_if_necessary(self, save_data: SaveProductSummaryData):
        print("Repository.save_product_summary_direct_if_necessary start")
        self.add_product_summary_direct_if_necessary(save_data)

    def save_mixture_and_amount_columns(self, save_data: SaveMixtureWithAmountData):
        self.output_expand_worksheet.batch_clear(["B2:B", "G2:I"])
        self.update_mixture_and_amount_columns(save_data)

    def save_similarity_and_adapter_columns(self, save_data: SaveSimilarityData):
        self.output_expand_worksheet.batch_clear(["K2:L"])
        self.update_similarity_and_adapter_columns(save_data)

    def add_product_summary_direct_if_necessary(self, save_data: SaveProductSummaryData):
        rows = save_data.get_rows()
        output_direct_worksheet = self.output_product_worksheet
        added_product_summary_values = output_direct_worksheet.get_values("A:C")[1:]
        product_code_column_index = 0

        new_code = 1 + max_value_in_column(added_product_summary_values, product_code_column_index)

        not_yet_added_rows: list[[int, str, str, str, float, float | str]] = []

        for i, row_properties in enumerate(rows):
            product_name = row_properties[0]
            label = row_properties[1]
            amount = to_num(row_properties[2])
            unit = row_properties[3]

            not_yet_added_row = []

            if exists_product_and_label(added_product_summary_values, product_name, label):
                continue # 存在するのでスキップ

            # 存在しないので追加リストに保持
            not_yet_added_row.append(new_code + i)
            not_yet_added_row.append(product_name)
            not_yet_added_row.append(label)
            not_yet_added_row.append(None)
            if unit == "g":
                not_yet_added_row.append(1)
                not_yet_added_row.append(amount)
            else:
                not_yet_added_row.append(amount)
                not_yet_added_row.append("")

            # 追加リストを登録
            print(f"Logging in Repository.add_product_summary_direct_if_necessary: {not_yet_added_row}")
            not_yet_added_rows.append(not_yet_added_row)

        output_direct_worksheet.append_rows(not_yet_added_rows)

    def update_mixture_and_amount_columns(self, save_data: SaveMixtureWithAmountData):
        column_numbers = [1, 2, 3, 4]  # 0を含める
        column_length = 11

        data = save_data.get_rows()
        for i in range(0, column_length):
            if i in column_numbers:
                tup_index = column_numbers.index(i)
                values = [[tup[tup_index]] for tup in data]
                self.update_column_on_expand_worksheet(values, i)

    def update_similarity_and_adapter_columns(self, save_data: SaveSimilarityData):
        similarities = save_data.get_similarities()
        adapters = save_data.get_similar_names()

        similarity_column_values = to_column_values(similarities)
        adapter_column_values = to_column_values(adapters)

        self.update_column_on_expand_worksheet(similarity_column_values, 6)
        self.update_column_on_expand_worksheet(adapter_column_values, 7)

    def update_column_on_expand_worksheet(self, values, index):
        for row_value in values:
            if len(row_value) != 1:
                raise ValueError("update_columnでは複数列同時更新できません。1列のみの更新に限定してください")
        column_char = index_to_col_name(index)
        self.output_expand_worksheet.update(range_name=f"{column_char}2", values=values)
