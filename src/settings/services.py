from abc import ABC, abstractmethod
from typing import Type

from settings.repositories import AbstractRepository


class AbstractService(ABC):
    @abstractmethod
    def __init__(self, repo: Type[AbstractRepository]) -> None: ...


class BaseService(AbstractService):
    def __init__(self, repo: Type[AbstractRepository]) -> None:
        self.repository: AbstractRepository = repo()
