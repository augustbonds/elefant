from flask import render_template, jsonify, request, redirect
from app import app
from .bookmark_store import BookmarkStore

store = BookmarkStore()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'boonspoj'}
    return render_template('index.html', title='August', user=user, bookmarks=store.get_bookmarks())

@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    bookmarks = store.get_bookmarks()
    return jsonify(bookmarks)

@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    url = request.form['url']
    title = request.form['title']
    description = request.form['description']
    store.add_bookmark(url=url, title=title, description=description) 
    return redirect('/')


    
        




