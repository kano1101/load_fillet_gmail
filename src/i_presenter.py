from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IViewer(ABC, Generic[T]):
    @abstractmethod
    def view(self, view_model: T):
        raise NotImplementedError()


