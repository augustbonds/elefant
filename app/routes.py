from flask import render_template, jsonify, request, redirect
from app import app
from app.bookmark_store import BookmarkStore
from app.forms import NewBookmarkForm

store = BookmarkStore()
user = {'username': 'boonspoj'}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=user, bookmarks=store.get_bookmarks())

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

@app.route('/bookmarks/new', methods=['GET', 'POST'])
def create_new_bookmark():
    if request.method == 'POST':
        url = request.form['url']
        title = request.form['title']
        description = request.form['description']
        store.add_bookmark(url=url, title=title, description=description) 
        return redirect('/')
    else:
        form = NewBookmarkForm()
        return render_template('createnew.html', form=form, user=user)

    
        




