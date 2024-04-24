import injector
from dotenv import load_dotenv
from typing import Type, TypeVar
from collections.abc import Callable
from i_parameter import IParameter, IParameterController, IParameterInteractor, IParameterRepository
from controller import Controller
from interactor import IInteractor, IRepository, IPresenter
from interactor import Interactor
from repository import Repository
from presenter import Presenter
from presenter import IViewer
from viewer import ConsoleViewer

from i_parameter import ParameterController
from parameter_2024popup import Popup2024ParameterInteractor, Popup2024ParameterRepository, Popup2024Parameter

from diff import assign_most_similar_mixture, assign_most_similarity_as_manual
from copy_to_sheet_from_gmail import get_product_amount_to_sheet_from_gmail, copy_to_sheet_from_gmail
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


if __name__ == '__main__':
    load_dotenv()

    # scrape()
    # ()
    dependency = DependencyBuilder()
    controller = dependency.build()

    controller.copy_to_sheet()
