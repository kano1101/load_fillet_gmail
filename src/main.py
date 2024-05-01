import injector
from typing import Type, TypeVar
from collections.abc import Callable
from dotenv import load_dotenv

from i_parameter import IParameter, IParameterController, IParameterInteractor, IParameterRepository
from parameter import Parameter, ParameterController, ParameterInteractor, ParameterRepository
from controller import Controller
from i_interactor import IRepository, IPresenter, IWriteProductSummaryInteractor
from i_interactor import IWriteMixtureWithAmountInteractor
from i_interactor import ICalcAndWriteMixtureSimilarityInteractor
from write_product_summary_interactor import WriteProductSummaryInteractor
from write_mixture_with_amount_interactor import WriteMixtureWithAmountInteractor
from calc_and_write_mixture_similarity_interactor import CalcAndWriteMixtureSimilarityInteractor
from repository import Repository
from presenter import Presenter
from presenter import IViewer
from viewer import ConsoleViewer


T = TypeVar("T")


class DependencyBuilder:
    def __init__(self):
        # 依存性注入の初期化はconfigureに移譲
        self._injector = injector.Injector(self.__class__.configure)

    @classmethod
    def configure(cls, binder: injector.Binder) -> None:
        binder.bind(Controller, to=Controller)
        binder.bind(IWriteProductSummaryInteractor, to=WriteProductSummaryInteractor)
        binder.bind(IWriteMixtureWithAmountInteractor, to=WriteMixtureWithAmountInteractor)
        binder.bind(ICalcAndWriteMixtureSimilarityInteractor, to=CalcAndWriteMixtureSimilarityInteractor)
        binder.bind(IRepository, to=Repository)
        binder.bind(IPresenter, to=Presenter)
        binder.bind(IViewer, to=ConsoleViewer)
        binder.bind(IParameter, to=Parameter)
        binder.bind(IParameterController, to=ParameterController)
        binder.bind(IParameterInteractor, to=ParameterInteractor)
        binder.bind(IParameterRepository, to=ParameterRepository)

    def __getitem__(self, klass: Type[T]) -> Callable:
        # 与えられたインタフェースに応じて実体クラスを返す
        return lambda: self._injector.get(klass)

    def build(self) -> Controller:
        return self[Controller]()


if __name__ == '__main__':
    load_dotenv()
    dependency = DependencyBuilder()
    controller = dependency.build()

    controller.write_product_if_necessary()
    # controller.write_mixture_with_amount()
    # controller.calc_and_write_mixture_similarity()
