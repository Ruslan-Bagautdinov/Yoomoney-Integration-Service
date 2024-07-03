from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    async def get_session(self):
        pass

    @abstractmethod
    async def init_db(self):
        pass