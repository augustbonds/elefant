import configparser
import json

class BookmarkStore:
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/app.conf')
        try:
            self.db_path = config['store']['DbPath']
        except KeyError:
            raise SystemExit(f"[BookmarkStore] Couldn't find DbPath in app.conf, exiting")
        print(f"[BookmarkStore] Loaded bookmark store with path {self.db_path}")
    
    def add_bookmark(self, url, title, description):
        store = self.read_db_file()
        store.append({"url": url, "title": title, "description": description})
        self.write_db_file(store)
        print(f"[BookmarkStore] Added entry: url={url} title={title} description={description}")

    def get_bookmarks(self):
        store = self.read_db_file()
        print(f"[BookmarkStore] Returning all {len(store)} bookmarks")
        return store
    
    def write_db_file(self,bookmarks):
        with open(self.db_path, 'w') as db:
            json.dump(bookmarks, db)
    
    def read_db_file(self):
        try:
            with open(self.db_path) as db:
                bookmarks = json.load(db)
                return bookmarks
        except IOError:
            print(f"[BookmarkStore] Db file didn't exist. Will be created by next add operation.")
            return []

