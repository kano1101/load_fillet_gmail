import injector
from typing import Type, TypeVar
from collections.abc import Callable
from dotenv import load_dotenv

from i_parameter import IParameter, IParameterController, IParameterInteractor, IParameterRepository
from parameter import Parameter, ParameterController, ParameterInteractor, ParameterRepository
from controller import Controller
from interactor import IInteractor, IRepository, IPresenter
from interactor import Interactor
from repository import Repository
from presenter import Presenter
from presenter import IViewer
from helper import get_recipe_support_spreadsheet, get_worksheet_in_recipe_support
from viewer import ConsoleViewer

from diff import assign_most_similar_mixture, assign_most_similarity_as_manual
from replace_names import replace_product_names, replace_article_names


def scrape_gmail_to_spreadsheet(dst_worksheet, labels):
    product_names, mixture_names, amounts, units = copy_to_sheet_from_gmail(labels)

    dst_worksheet.update(range_name="B2", values=product_names)
    dst_worksheet.update(range_name="C2", values=mixture_names)
    dst_worksheet.update(range_name="F2", values=amounts)
    dst_worksheet.update(range_name="G2", values=units)


def scrape():
    ss = get_recipe_support_spreadsheet()

    tmp_worksheet = get_worksheet_in_recipe_support(ss, "製品完成量")

    amounts_labels = ['POPUP4', 'POPUP3', 'POPUP2', 'POPUP']
    labels = ['POPUP4']

    # 製品ごとの完成分量を一時シートに更新
    list_product_and_amount_unit = get_product_amount_to_sheet_from_gmail(amounts_labels)
    tmp_worksheet.update(range_name="A2", values=list_product_and_amount_unit)

    dst_worksheet = get_worksheet_in_recipe_support(ss, 'Gmail4')
    articles_worksheet = get_worksheet_in_recipe_support(ss, "材料")
    products_worksheet = get_worksheet_in_recipe_support(ss, "製品")

    # Gmailのメールをスクレイピングし、シートを更新 ラベル指定は関数内でしている
    # scrape_gmail_to_spreadsheet(dst_worksheet, labels)

    # 類似度を計算し、シートを更新
    # 類似度最高値の要素をベースに
    # assign_most_similar_mixture(dst_worksheet, articles_worksheet, products_worksheet)
    # 手作業検索をベースに
    # assign_most_similarity_as_manual(dst_worksheet)

    # 100%一致にするため材料と製品の名称を更新
    # replace_article_names(sh)
    # replace_product_names(sh)


T = TypeVar("T")


class DependencyBuilder:
    def __init__(self):
        # 依存性注入の初期化はconfigureに移譲
        self._injector = injector.Injector(self.__class__.configure)

    @classmethod
    def configure(cls, binder: injector.Binder) -> None:
        binder.bind(IInteractor, to=Interactor)
        binder.bind(IRepository, to=Repository)
        binder.bind(IPresenter, to=Presenter)
        binder.bind(IViewer, to=ConsoleViewer)
        binder.bind(IParameter, to=Parameter)
        binder.bind(IParameterController, to=ParameterController)
        binder.bind(IParameterInteractor, to=ParameterInteractor)
        binder.bind(IParameterRepository, to=ParameterRepository)
        # binder.bind(IParameter, to=Gallery2024Parameter)
        # binder.bind(IParameterController, to=ParameterController)
        # binder.bind(IParameterInteractor, to=Gallery2024ParameterInteractor)
        # binder.bind(IParameterRepository, to=Gallery2024ParameterRepository)

    def __getitem__(self, klass: Type[T]) -> Callable:
        # 与えられたインタフェースに応じて実体クラスを返す
        return lambda: self._injector.get(klass)

    def build(self) -> Controller:
        parameter_controller = self[IParameterController]()
        interactor = self[IInteractor]()
        return Controller(parameter_controller, interactor)


if __name__ == '__main__':
    load_dotenv()

    # scrape()
    # ()
    dependency = DependencyBuilder()
    controller = dependency.build()

    controller.write_mixture_with_similarity()
