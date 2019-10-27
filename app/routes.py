from flask import render_template, jsonify, request, redirect
from app import app
from app.store.file_store import FileStore
from app.forms import NewBookmarkForm
import logging

store = FileStore()
user = {'username': 'boonspoj'}
logger = logging.getLogger(__name__)

@app.route('/')
@app.route('/index')
def index():
    tags = request.args.get('tags', default='', type = str)
    tags = [] if tags == '' else [tag.strip() for tag in tags.split(',')]
    offset = request.args.get('offset', default = 0, type = int)
    limit = request.args.get('limit', default = 10, type = int)
    prev_offset = offset if offset == 0 else offset - 1
    next_offset = offset + 1
    logger.info(f"index(): tags = {tags} offset = {offset} limit = {limit} prev_offset = {prev_offset} next_offset={next_offset}")
    if tags:
        logger.info(f"tags specified: {tags}") 
        return render_template('index.html', user=user, bookmarks=store.get_posts_by_tags(tags, offset, limit))
    else:
        logger.info(f"no tags specified")
        return render_template('index.html', user=user, bookmarks=store.get_posts(offset,limit), page_num=offset+1, prev_offset=prev_offset, next_offset=next_offset)

@app.route('/bookmarks/new', methods=['GET', 'POST'])
def create_new_bookmark():
    if request.method == 'POST':
        post = {}
        post["url"] = request.form['url']
        post["title"] = request.form['title']
        post["description"] = request.form['description']
        tags = request.form.get('tags', default='')
        tags = [tag.strip() for tag in tags.split(',')]
        post["tags"] = tags
        store.add_post(post)
        return redirect('/')
    else:
        form = NewBookmarkForm()
        return render_template('createnew.html', form=form, user=user)


@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    bookmarks = store.get_bookmarks()
    return jsonify(bookmarks)

@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    url = request.form['url']
    title = request.form['title']
    description = request.form['description']
    tags = request.form.get('tags', default='')
    tags = [tag.strip() for tag in tags.split(',')]
    store.add_bookmark(url=url, title=title, description=description, tags=tags)
    return redirect('/')
