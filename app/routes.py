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
    search_query = request.args.get("q", default='', type = str)
    if (search_query):
        logger.info(f"search query specififed: {search_query}")
        return render_template('index.html', search_query=search_query, user=user, bookmarks=store.search_posts(search_query, offset, limit), page_num=offset+1, prev_offset=prev_offset, next_offset=next_offset,limit=limit)
    elif tags:
        logger.info(f"tags specified: {tags}") 
        return render_template('index.html', tags=",".join(tags), user=user, bookmarks=store.get_posts_by_tags(tags, offset, limit), page_num=offset+1, prev_offset=prev_offset, next_offset=next_offset,limit=limit)
    else:
        logger.info(f"no tags specified")
        return render_template('index.html', user=user, bookmarks=store.get_posts(offset,limit), page_num=offset+1, prev_offset=prev_offset, next_offset=next_offset,limit=limit)

@app.route('/bookmarks/new', methods=['GET', 'POST'])
def create_new_bookmark():
    if request.method == 'POST':
        post = post_from_form(request.form)
        store.add_post(post)
        return redirect('/')
    else:
        form = NewBookmarkForm()
        return render_template('createnew.html', form=form, user=user)


@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    search_query = request.args["q"]
    if (search_query):
        return jsonify(store.search_posts(query=search_query, offset=request.args["offset"], limit=request.args["limit"]))
    else:
        return jsonify(store.get_all_posts())

@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    post = post_from_form(request.form)
    store.add_post(post)
    return redirect('/')

def post_from_form(form):
    post = {}
    post["url"] = request.form['url']
    post["title"] = request.form['title']
    post["description"] = request.form['description']
    tags = request.form.get('tags', default='')
    tags = [tag.strip() for tag in tags.split(',')]
    post["tags"] = tags
    return post