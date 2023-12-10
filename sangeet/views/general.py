# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db
from flask_login import (
    login_user,
    logout_user,
    login_required,
)
from sangeet.models import *

bp = Blueprint('general', __name__)


def content_overview(categories):   # function for showing any content overview and redirecting to a page with all entries by just taking a categories dictionary
    content = {}
    for item in categories:
        table = item['table']
        filter_by = item.get('filter_by', None)
        value = item.get('value', None)
        cat_link = item['cat_link']
        content[cat_link] = {}
        content[cat_link]['title'] = item['title']
        content[cat_link]['cat_link'] = item['cat_link']
        if (filter_by is None):                 # If its the case of returning all items from a table
            query_result = db.session.execute(db.select(table).limit(5)).scalars()
            if (content[cat_link].get('order_by')):
                order_by = content[cat_link].get('order_by')
                query_result = db.session.execute(db.select(table).order_by(getattr(table, order_by)).desc()).limit(5).scalars()
        elif item.get('table_2'):                # if condition will evaluate to true if table_2 attribute exists
            table_2 = item['table_2']
            query_result = db.session.execute(db.select(table).where(getattr(table_2, filter_by).ilike(f"{value}")).limit(5).join_from(table, table_2)).scalars()
        else:   # both of the above and below queries are achiveing case insensitive matching, but in a different way
            query_result = db.session.execute(db.select(Track).where(db.func.lower(getattr(table, filter_by)).ilike(f"{value.lower()}")).limit(5)).scalars()
        query_result = [result for result in query_result]
        content[cat_link]['items'] = query_result
    return content


@bp.route('/home')
@login_required
def home():
    categories = [
        {'title': 'All songs', 'cat_link':'all', 'table': Track},
        {'title': 'Recently on Sangeet', 'cat_link':'recents', 'table': Track, 'order_by':'release_date'},
        ]
    content = content_overview(categories)
    # Return the result
    return render_template('general/home.html', content=content)

@bp.route('/explore')
def explore():
    categories = [
        {'title': 'All songs', 'cat_link':'all', 'table': Track, 'order_by': 'release_date'},
        {'title': 'Top Pop', 'cat_link':'pop', 'table': Track, 'filter_by': 'genre', 'value': 'pop'},
        {'title': 'Romantic Tunes', 'cat_link':'romantic', 'table': Track, 'filter_by': 'genre', 'value': 'Romantic'},
        {'title': 'English', 'cat_link':'english', 'table': Track, 'filter_by': 'name', 'value': 'English', 'table_2':Language},
        {'title': 'Devotional', 'cat_link':'devotional', 'table': Track, 'filter_by': 'genre', 'value': 'devotional'},
        {'title': 'From the Nightingale of India', 'cat_link':'lata', 'table': Track, 'filter_by': 'artist_name', 'value': 'Lata Mangeshkar'}
        ]
    content = content_overview(categories)
    # Return the result
    return render_template('general/explore.html', content=content)

@bp.route('/library')
def library():
    return render_template('general/library.html')

@bp.route('/profile')
def profile():
    return render_template('general/profile.html')

@bp.route('/preferences')
def preferences():
    return render_template('general/preferences.html')

