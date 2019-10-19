from flask import render_template
from flask import jsonify
from app import app
from .bookmark_store import BookmarkStore

store = BookmarkStore()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'boonspoj'}
    return render_template('index.html', title='August', user=user, bookmarks=store.get_bookmarks())

@app.route('/bookmarks')
def get_bookmarks():
    bookmarks = store.get_bookmarks()
    return jsonify(bookmarks)


