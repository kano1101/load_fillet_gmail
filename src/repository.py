import injector
from xlwingsform import Workbook

from i_interactor import IRepository
from i_parameter import IParameterRepository
from src.i_interactor import T


class SaveData:
    def __init__(self):
        self.workbook = Workbook()


class Repository(IRepository[SaveData]):
    @injector.inject
    def __init__(self, parameter: IParameterRepository):
        self.parameter = parameter

    def save(self, save_data: SaveData):
        value = self.parameter.get_value(save_data)
        self.workbook.set_value(value)
