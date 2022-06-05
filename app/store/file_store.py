from app.store.abstract_store import AbstractStore
import configparser
import json
import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


def posts_sorted_by_time(posts):
    return sorted(posts, key=lambda post: defaultdict(lambda: '', post)["date_added"], reverse=True)


def next_id(store):
    next = store["next_id"]
    store["next_id"] += 1
    return next


def read_db_path_from_conf():
    config = configparser.ConfigParser()
    config.read('conf/app.conf')
    try:
        return config['store']['DbPath']
    except KeyError:
        raise SystemExit("Couldn't find DbPath in app.conf, exiting")


def read_store_from_file(db_path):
    try:
        with open(db_path) as db:
            store = json.load(db)
            return store
    except IOError:
        logger.info("Db file: " + db_path + " didn't exist. Will be created by next add operation.")
        return {"next_id": 1, "bookmarks": []}


class FileStore(AbstractStore):

    def __init__(self):
        self.db_path = read_db_path_from_conf()
        logger.info(f"Loaded bookmark store with path {self.db_path}")

    def get_posts(self, offset=0, limit=10):
        logger.debug(f"get_posts: o={offset} l={limit} ")
        db = read_store_from_file(self.db_path)
        posts = db["bookmarks"]
        sorted_by_time = posts_sorted_by_time(posts)
        return sorted_by_time[offset * limit:offset * limit + limit]

    def get_posts_by_tags(self, tags=[], offset=0, limit=10):
        logger.debug(f"get_posts_by_tags: tags={tags} o={offset} l={limit} ")
        db = read_store_from_file(self.db_path)
        posts = db["bookmarks"]
        by_tags = [post for post in posts if set(post.get("tags", [])).intersection(set(tags))]
        sorted_by_time = posts_sorted_by_time(by_tags)
        return sorted_by_time[offset * limit:offset * limit + limit]

    def add_post(self, post):
        store = read_store_from_file(self.db_path)
        post["id"] = next_id(store)
        post["date_added"] = str(datetime.datetime.utcnow().isoformat())
        store["bookmarks"].append(post)
        self.write_db_file(store)
        logger.debug(f"add_post: {post}")

    def search_posts(self, query, offset, limit):
        query = query.lower()
        posts = self.get_all_posts()
        last_index = offset * limit + limit
        result = []
        for post in posts:
            if len(result) == last_index - 1:
                break
            if query in post["title"].lower():
                result.append(post)
            elif query in post["url"].lower():
                result.append(post)
            elif query in ''.join(post.get("tags", [])).lower():
                result.append(post)
            elif query in post.get("description", "").lower():
                result.append(post)
        return posts_sorted_by_time(result)[offset * limit:]

    def get_all_posts(self):
        return read_store_from_file(self.db_path)["bookmarks"]

    def write_db_file(self, store):
        with open(self.db_path, 'w') as db:
            json.dump(store, db, indent=4)
