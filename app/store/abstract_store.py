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

    @abstractmethod
    def search_posts(self, query, offset, limit):
        pass

    @abstractmethod
    def get_post_by_id(self, post_id):
        pass

    @abstractmethod
    def update_post(self, post_id, updated_post):
        pass

    @abstractmethod
    def archive_post(self, post_id):
        pass

    @abstractmethod
    def unified_search(self, tags, text_query, offset, limit):
        pass
