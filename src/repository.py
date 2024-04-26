import os

import injector
from xlwingsform import Workbook

from i_interactor import IRepository
from i_parameter import IParameterRepository
from interactor import SaveData


class Repository(IRepository[SaveData]):
    @injector.inject
    def __init__(self, parameter: IParameterRepository):
        self.parameter = parameter
        self.output_worksheet = self.parameter.get_output_worksheet()

    def save(self, save_data: SaveData):
        data = save_data.data

        blank_column_numbers = [0, 2, 3, 4, 5, 9, 10]  # 0を含める
        blanks = [""] * len(blank_column_numbers)

        save_values = [blanks[:1] + list(row) + blanks[1:] for row in data]

        for i, save_value in enumerate(save_values):
            self.add(save_value)

    def add(self, row_value, index=0):
        # self.output_worksheet.update(range_name=f"A{index + 2}", values=[[row_value]])
        print(row_value)
