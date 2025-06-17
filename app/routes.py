from flask import render_template, jsonify, request, redirect
from flask_basicauth import BasicAuth

from app import app
from app.store.file_store import FileStore
from app.forms import NewBookmarkForm, EditBookmarkForm
from app.config import config
import logging

store = FileStore()
user = config.DEFAULT_USER
logger = logging.getLogger(__name__)

basic_auth = BasicAuth(app)


def handle_bookmark_form(form, post_id=None):
    """
    Common handler for bookmark form processing (create/edit)
    
    Args:
        form: The validated form instance
        post_id: Optional post ID for editing (None for creating)
        
    Returns:
        redirect response if successful, None if form should be re-rendered
    """
    if form.validate_on_submit():
        post = post_from_form(request.form)
        
        if post_id:
            # Edit existing bookmark
            if store.update_post(post_id, post):
                return redirect('/')
            else:
                logger.error(f"Failed to update bookmark {post_id}")
                return "Error updating bookmark", 500
        else:
            # Create new bookmark
            store.add_post(post)
            return redirect('/')
    
    # Form validation failed, return None to re-render
    return None


def populate_edit_form(form, bookmark):
    """Populate edit form with existing bookmark data"""
    form.url.data = bookmark['url']
    form.title.data = bookmark['title']
    form.description.data = bookmark.get('description', '')
    form.tags.data = ','.join(bookmark.get('tags', []))


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
    limit = request.args.get('limit', default=config.DEFAULT_PAGE_SIZE, type=int)
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
    form = NewBookmarkForm()
    
    # Try to handle form submission
    result = handle_bookmark_form(form)
    if result:
        return result
    
    # Form not submitted or validation failed, render template
    return render_template('createnew.html', form=form, user=user, config=config)


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
    bookmark = store.get_post_by_id(post_id)
    if not bookmark:
        return "Bookmark not found", 404
    
    form = EditBookmarkForm()
    
    # Try to handle form submission
    result = handle_bookmark_form(form, post_id)
    if result:
        return result
    
    # Pre-populate form with existing data on GET request
    if request.method == 'GET':
        populate_edit_form(form, bookmark)
    
    return render_template('edit.html', form=form, user=user, bookmark=bookmark, config=config)


@app.route('/bookmarks/<int:post_id>/archive', methods=['POST'])
@basic_auth.required
def archive_bookmark(post_id):
    if store.archive_post(post_id):
        return redirect('/')
    else:
        return "Bookmark not found", 404


@app.route('/api/tags')
def get_tags():
    """Return all unique tags as JSON for autocomplete"""
    all_posts = store.get_all_posts()
    active_posts = [post for post in all_posts if not post.get("archived", False)]
    
    # Collect all tags from all posts
    all_tags = set()
    for post in active_posts:
        for tag in post.get("tags", []):
            if tag.strip():
                all_tags.add(tag.strip())
    
    # Return sorted list of tags
    return jsonify(sorted(list(all_tags)))


def post_from_form(form):
    post = {"url": request.form['url'],
            "title": request.form['title'],
            "description": request.form['description']}
    tags = request.form.get('tags', default='')
    tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
    post["tags"] = tags
    return post
