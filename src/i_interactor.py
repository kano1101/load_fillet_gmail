from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IWriteProductSummaryInteractor(ABC, Generic[T]):
    @abstractmethod
    def handle(self, input_data: T):
        raise NotImplementedError()


class IWriteMixtureWithAmountInteractor(ABC, Generic[T]):
    @abstractmethod
    def handle(self, input_data: T):
        raise NotImplementedError()


class ICalcAndWriteMixtureSimilarityInteractor(ABC, Generic[T]):
    @abstractmethod
    def handle(self, input_data: T):
        raise NotImplementedError()


class IRepository(ABC, Generic[T]):
    @abstractmethod
    def save_product_summary_direct_if_necessary(self, save_data: T):
        raise NotImplementedError()

    @abstractmethod
    def save_mixture_and_amount_columns(self, save_data: T):
        raise NotImplementedError()

    @abstractmethod
    def save_similarity_and_adapter_columns(self, save_data: T):
        raise NotImplementedError()


class IPresenter(ABC, Generic[T]):
    @abstractmethod
    def output(self, output_data: T):
        raise NotImplementedError()
