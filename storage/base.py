from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def add_user(self, user: 'User'):
        pass

    @abstractmethod
    def get_user(self, user_id) -> 'User':
        pass

    @abstractmethod
    def add_check_in(self, check_in: 'CheckIn'):
        pass