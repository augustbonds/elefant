class BookmarkStore:
    
    def __init__(self):
        self.store = [];
    
    def add_bookmark(self, url, title, description):
        self.store.append({"url": url, "title": title, "description": description})
        print(f"[BookmarkStore] Added entry: url={url} title={title} description={description}")

    def get_bookmarks(self):
        print(f"[BookmarkStore] Returning all {len(self.store)} bookmarks")
        return self.store


