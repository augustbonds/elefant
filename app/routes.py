from flask import render_template, jsonify, request, redirect
from flask_basicauth import BasicAuth

from app import app
from app.store.file_store import FileStore
from app.forms import NewBookmarkForm, EditBookmarkForm
import logging

store = FileStore()
user = {'username': 'boonspoj'}
logger = logging.getLogger(__name__)

basic_auth = BasicAuth(app)


def parse_search_query(query):
    """Parse unified search query to extract tags and text"""
    if not query:
        return [], ""
    
    import re
    
    # Extract #tags using regex
    tag_matches = re.findall(r'#(\w+)', query)
    tags = [tag.lower() for tag in tag_matches]
    
    # Remove #tags from query to get remaining text
    text_query = re.sub(r'#\w+', '', query).strip()
    # Clean up multiple spaces
    text_query = ' '.join(text_query.split())
    
    return tags, text_query


@app.route('/')
@app.route('/index')
def index():
    # Support legacy ?tags= parameter by converting to unified search
    legacy_tags = request.args.get('tags', default='', type=str)
    search_query = request.args.get("q", default='', type=str)
    
    # Convert legacy tag filtering to unified search
    if legacy_tags and not search_query:
        tag_list = [tag.strip() for tag in legacy_tags.split(',') if tag.strip()]
        search_query = ' '.join(f'#{tag}' for tag in tag_list)
    
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=20, type=int)
    prev_offset = max(0, offset - limit)
    next_offset = offset + limit
    
    # Parse unified search query
    tags, text_query = parse_search_query(search_query)
    
    logger.info(f"index(): search_query='{search_query}' tags={tags} text='{text_query}' offset={offset}")
    
    if search_query:
        # Use unified search that handles both tags and text
        bookmarks, total = store.unified_search(tags, text_query, offset, limit)
    else:
        # No search query - show all posts
        bookmarks, total = store.get_posts(offset, limit)
    
    # Calculate pagination state
    current_page = (offset // limit) + 1
    total_pages = (total + limit - 1) // limit  # Ceiling division
    has_prev = offset > 0
    has_next = offset + limit < total
    
    return render_template('index.html', search_query=search_query, user=user,
                           bookmarks=bookmarks, page_num=current_page, total_pages=total_pages,
                           prev_offset=prev_offset, next_offset=next_offset, limit=limit,
                           has_prev=has_prev, has_next=has_next, total=total)


@app.route('/bookmarks/new', methods=['GET', 'POST'])
@basic_auth.required
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
    if search_query:
        return jsonify(
            store.search_posts(query=search_query, offset=request.args["offset"], limit=request.args["limit"]))
    else:
        return jsonify(store.get_all_posts())


@app.route('/bookmarks', methods=['POST'])
@basic_auth.required
def add_bookmark():
    post = post_from_form(request.form)
    store.add_post(post)
    return redirect('/')


@app.route('/bookmarks/<int:post_id>/edit', methods=['GET', 'POST'])
@basic_auth.required
def edit_bookmark(post_id):
    if request.method == 'POST':
        updated_post = post_from_form(request.form)
        if store.update_post(post_id, updated_post):
            return redirect('/')
        else:
            return "Bookmark not found", 404
    else:
        bookmark = store.get_post_by_id(post_id)
        if bookmark:
            form = EditBookmarkForm()
            form.url.data = bookmark['url']
            form.title.data = bookmark['title']
            form.description.data = bookmark.get('description', '')
            form.tags.data = ','.join(bookmark.get('tags', []))
            return render_template('edit.html', form=form, user=user, bookmark=bookmark)
        else:
            return "Bookmark not found", 404


@app.route('/bookmarks/<int:post_id>/archive', methods=['POST'])
@basic_auth.required
def archive_bookmark(post_id):
    if store.archive_post(post_id):
        return redirect('/')
    else:
        return "Bookmark not found", 404


def post_from_form(form):
    post = {"url": request.form['url'],
            "title": request.form['title'],
            "description": request.form['description']}
    tags = request.form.get('tags', default='')
    tags = [tag.strip() for tag in tags.split(',')]
    post["tags"] = tags
    return post
