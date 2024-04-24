import os
import injector

from access import get_credentials_cover, run_gas_function

from interactor import IInteractor
from interactor import InputData
from i_parameter import IParameterController


class Controller:
    @injector.inject
    def __init__(self, parameter: IParameterController, interactor: IInteractor):
        self.parameter = parameter
        self.interactor = interactor
        scopes = [
            'https://www.googleapis.com/auth/script.projects',
            'https://www.googleapis.com/auth/spreadsheets',
        ]
        self.creds = get_credentials_cover(scopes)
        self.deploy_id = os.environ.get("DEPLOY_ID")

    def copy_to_form(self):
        for item_num in list(map(lambda v: int(v), self.parameter.get_target_indices())):
            product_name = self.parameter.get_product_name(item_num)
            self.parameter.update_product_name(product_name)

            # GAS実行
            run_gas_function(self.creds, self.deploy_id, 'runCreative')

            # 読み込み直してみる
            list_material_and_allergen = self.parameter.get_list_zipped_materials_and_allergens()

            # 変換
            input_data = InputData(item_num, product_name, list_material_and_allergen)

            # Interactorハンドル
            self.interactor.handle(input_data)

        # ファイルに変更を保存
        # self.workbook.save(self.path)
