from app.store.abstract_store import AbstractStore
import configparser
import json
import datetime
from collections import defaultdict
import logging
import re

logger = logging.getLogger(__name__)


def parse_search_query(query):
    """Parse unified search query to extract tags and text"""
    if not query:
        return [], ""
    
    # Extract #tags using regex
    tag_matches = re.findall(r'#(\w+)', query)
    tags = [tag.lower() for tag in tag_matches]
    
    # Remove #tags from query to get remaining text
    text_query = re.sub(r'#\w+', '', query).strip()
    # Clean up multiple spaces
    text_query = ' '.join(text_query.split())
    
    return tags, text_query


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

    def get_posts(self, offset=0, limit=20):
        logger.debug(f"get_posts: o={offset} l={limit} ")
        db = read_store_from_file(self.db_path)
        posts = [post for post in db["bookmarks"] if not post.get("archived", False)]
        sorted_by_time = posts_sorted_by_time(posts)
        return sorted_by_time[offset:offset + limit], len(posts)

    def get_posts_by_tags(self, tags=[], offset=0, limit=20):
        logger.debug(f"get_posts_by_tags: tags={tags} o={offset} l={limit} ")
        db = read_store_from_file(self.db_path)
        posts = [post for post in db["bookmarks"] if not post.get("archived", False)]
        by_tags = [post for post in posts if set(post.get("tags", [])).intersection(set(tags))]
        sorted_by_time = posts_sorted_by_time(by_tags)
        return sorted_by_time[offset:offset + limit], len(by_tags)

    def add_post(self, post):
        store = read_store_from_file(self.db_path)
        post["id"] = next_id(store)
        post["date_added"] = str(datetime.datetime.utcnow().isoformat())
        post["archived"] = False
        store["bookmarks"].append(post)
        self.write_db_file(store)
        logger.debug(f"add_post: {post}")

    def search_posts(self, query, offset, limit):
        query = query.lower()
        all_posts = self.get_all_posts()
        posts = [post for post in all_posts if not post.get("archived", False)]
        result = []
        for post in posts:
            if query in post["title"].lower():
                result.append(post)
            elif query in post["url"].lower():
                result.append(post)
            elif query in ''.join(post.get("tags", [])).lower():
                result.append(post)
            elif query in post.get("description", "").lower():
                result.append(post)
        sorted_results = posts_sorted_by_time(result)
        return sorted_results[offset:offset + limit]

    def get_all_posts(self):
        return read_store_from_file(self.db_path)["bookmarks"]

    def get_post_by_id(self, post_id):
        db = read_store_from_file(self.db_path)
        posts = db["bookmarks"]
        for post in posts:
            if post["id"] == post_id:
                return post
        return None

    def update_post(self, post_id, updated_post):
        store = read_store_from_file(self.db_path)
        posts = store["bookmarks"]
        for i, post in enumerate(posts):
            if post["id"] == post_id:
                updated_post["id"] = post_id
                updated_post["date_added"] = post["date_added"]
                updated_post["date_updated"] = str(datetime.datetime.utcnow().isoformat())
                updated_post["archived"] = post.get("archived", False)
                posts[i] = updated_post
                self.write_db_file(store)
                logger.debug(f"update_post: {updated_post}")
                return True
        return False

    def archive_post(self, post_id):
        store = read_store_from_file(self.db_path)
        posts = store["bookmarks"]
        for i, post in enumerate(posts):
            if post["id"] == post_id and not post.get("archived", False):
                post["archived"] = True
                post["date_archived"] = str(datetime.datetime.utcnow().isoformat())
                posts[i] = post
                self.write_db_file(store)
                logger.debug(f"archive_post: {post}")
                return True
        return False

    def unified_search(self, tags, text_query, offset, limit):
        """Unified search that handles both tag filtering and text search"""
        all_posts = self.get_all_posts()
        posts = [post for post in all_posts if not post.get("archived", False)]
        result = []
        
        for post in posts:
            # Check tag matching
            tag_match = True
            if tags:
                post_tags = [tag.lower() for tag in post.get("tags", [])]
                tag_match = all(tag in post_tags for tag in tags)
            
            # Check text matching
            text_match = True
            if text_query:
                text_query_lower = text_query.lower()
                text_match = (
                    text_query_lower in post["title"].lower() or
                    text_query_lower in post["url"].lower() or
                    text_query_lower in post.get("description", "").lower() or
                    text_query_lower in ''.join(post.get("tags", [])).lower()
                )
            
            # Both conditions must match
            if tag_match and text_match:
                result.append(post)
        
        sorted_results = posts_sorted_by_time(result)
        return sorted_results[offset:offset + limit], len(result)

    def write_db_file(self, store):
        with open(self.db_path, 'w') as db:
            json.dump(store, db, indent=4)
