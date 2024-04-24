from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IInteractor(ABC, Generic[T]):
    @abstractmethod
    def handle(self, input_data: T):
        raise NotImplementedError()


class IRepository(ABC, Generic[T]):
    @abstractmethod
    def save(self, save_data: T):
        raise NotImplementedError()


class IPresenter(ABC, Generic[T]):
    @abstractmethod
    def output(self, output_data: T):
        raise NotImplementedError()
