from app.store.abstract_store import AbstractStore
import configparser
import json
import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class FileStore(AbstractStore):

    def __init__(self):
        self.read_conf()
        logger.info(f"Loaded bookmark store with path {self.db_path}")

    def get_posts(self, offset=0, limit=10):
        logger.debug(f"get_posts: o={offset} l={limit} ")
        db = self.read_db_file()
        posts = db["bookmarks"]
        sorted_by_time = self.posts_sorted_by_time(posts)
        return sorted_by_time[offset*limit:offset*limit+limit]

    def get_posts_by_tags(self, tags=[], offset=0, limit=10):
        logger.debug(f"get_posts_by_tags: tags={tags} o={offset} l={limit} ")
        db = self.read_db_file()
        posts = db["bookmarks"]
        by_tags = [post for post in posts if set(post.get("tags",[])).intersection(set(tags))]
        sorted_by_time = self.posts_sorted_by_time(by_tags)
        return sorted_by_time[offset*limit:offset*limit+limit]

    def add_post(self, post):
        store = self.read_db_file()
        post["id"] = self.next_id(store)
        post["date_added"] = str(datetime.datetime.utcnow().isoformat())
        store["bookmarks"].append(post)
        self.write_db_file(store)
        logger.debug(f"add_post: {post}")

    def posts_sorted_by_time(self, posts):
        return sorted(posts, key=lambda post: defaultdict(lambda: '', post)["date_added"], reverse=True)
    
    def search_posts(self, query, offset, limit):
        query = query.lower()
        posts = self.get_all_posts()
        last_index = offset*limit + limit
        result = []
        for post in posts:
            if (len(result) == last_index - 1):
                break
            if (query in post["title"].lower()):
                result.append(post)
            elif (query in post["url"].lower()):
                result.append(post)
            elif (query in ''.join(post.get("tags", [])).lower()):
                result.append(post)
            elif (query in post.get("description", "").lower()):
                result.append(post)
        return self.posts_sorted_by_time(result)[offset*limit:]
    
    def get_all_posts(self):
        return self.read_db_file()["bookmarks"]

    def next_id(self, store):
        next = store["next_id"]
        store["next_id"] += 1
        return next

    def read_conf(self):
        config = configparser.ConfigParser()
        config.read('conf/app.conf')
        try:
            self.db_path = config['store']['DbPath']
        except KeyError:
           raise SystemExit("Couldn't find DbPath in app.conf, exiting")

    def write_db_file(self,store):
        with open(self.db_path, 'w') as db:
            json.dump(store, db)

    def read_db_file(self):
        try:
            with open(self.db_path) as db:
                store = json.load(db)
                return store
        except IOError:
            logger.info("Db file didn't exist. Will be created by next add operation.")
            return {"next_id": 1, "bookmarks": []}

