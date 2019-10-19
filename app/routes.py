from flask import render_template
from flask import jsonify
from app import app
from .bookmark_store import BookmarkStore

store = BookmarkStore()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'boonspoj'}
    store.add_bookmark(url="http://google.com", title="An evil search engine", description="Just stuff")
    return render_template('index.html', title='August', user=user)

@app.route('/bookmarks')
def get_bookmarks():
    bookmarks = store.get_bookmarks()
    return jsonify(bookmarks)


