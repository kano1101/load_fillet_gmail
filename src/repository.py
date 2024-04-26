import os

import injector
from xlwingsform import Workbook

from i_interactor import IRepository
from i_parameter import IParameterRepository
from interactor import SaveData
from utils import index_to_col_name


class Repository(IRepository[SaveData]):
    @injector.inject
    def __init__(self, parameter: IParameterRepository):
        self.parameter = parameter
        self.output_worksheet = self.parameter.get_output_worksheet()

    def save(self, save_data: SaveData):
        self.output_worksheet.batch_clear(["B2:B", "G2:K"])
        self.update_columns(save_data)

    def update_columns(self, save_data: SaveData):
        column_numbers = [1, 6, 7, 8]  # 0を含める
        column_length = 11

        data = save_data.data
        save_values = []
        for i in range(0, column_length):
            if i in column_numbers:
                tup_index = column_numbers.index(i)
                values = [[tup[tup_index]] for tup in data]
                self.update_column(values, i)

    def update_row(self, save_data: SaveData):
        blank_column_numbers = [0, 2, 3, 4, 5, 9, 10]  # 0を含める
        column_length = 11

        data = save_data.data
        save_values = []
        for d in data:
            tmp = list(d)
            for blank_column_number in blank_column_numbers:
                tmp.insert(blank_column_number, "")
            save_values.append(tmp)

        for i, save_value in enumerate(save_values):
            self.add_row(save_value, i)

    def add_row(self, row_value, index=0):
        self.output_worksheet.update(range_name=f"A{index + 3}", values=[row_value])

    def update_column(self, values, index=0):
        column_char = index_to_col_name(index)
        self.output_worksheet.update(range_name=f"{column_char}2", values=values)
