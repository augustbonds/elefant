from flask import render_template, jsonify, request, redirect
from app import app
from app.bookmark_store import BookmarkStore
from app.forms import NewBookmarkForm

store = BookmarkStore()
user = {'username': 'boonspoj'}

@app.route('/')
@app.route('/index')
def index():
    offset = request.args.get('offset', default = 0, type = int)
    limit = request.args.get('limit', default = 10, type = int)
    prev_offset = offset if offset == 0 else offset - 1
    next_offset = offset + 1
    return render_template('index.html', user=user, bookmarks=store.get_bookmarks_sorted_with_limit(offset,limit), page_num=offset+1, prev_offset=prev_offset, next_offset=next_offset)

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

