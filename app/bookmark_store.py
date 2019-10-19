import configparser
import json

class BookmarkStore:
   
    def __init__(self):
        self.read_conf()
        print(f"[BookmarkStore] Loaded bookmark store with path {self.db_path}")

    def read_conf(self):
        config = configparser.ConfigParser()
        config.read('conf/app.conf')
        try:
            self.db_path = config['store']['DbPath']
        except KeyError:
           raise SystemExit(f"[BookmarkStore] Couldn't find DbPath in app.conf, exiting") 
    
    def add_bookmark(self, url, title, description):
        store = self.read_db_file()
        bookmark = {"id": store['next_id'], "url": url, "title": title, "description": description}
        store["bookmarks"].append(bookmark)
        store["next_id"] += 1
        self.write_db_file(store)
        print(f"[BookmarkStore] Added entry: id={bookmark['id']} url={url} title={title} description={description}")

    def get_bookmarks(self):
        store = self.read_db_file()
        bookmarks = store["bookmarks"]
        print(f"[BookmarkStore] Returning all {len(bookmarks)} bookmarks")
        return bookmarks
    
    def write_db_file(self,store):
        with open(self.db_path, 'w') as db:
            json.dump(store, db)
    
    def read_db_file(self):
        try:
            with open(self.db_path) as db:
                store = json.load(db)
                return store
        except IOError:
            print(f"[BookmarkStore] Db file didn't exist. Will be created by next add operation.")
            return {"next_id": 1, "bookmarks": []}

