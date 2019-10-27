from abc import ABC, abstractmethod

class AbstractStore(ABC):

    @abstractmethod
    def get_posts(self, offset, limit):
        pass

    @abstractmethod
    def get_posts_by_tags(self, tags, offset, limit):
        pass

    @abstractmethod
    def add_post(self, post):
        pass

