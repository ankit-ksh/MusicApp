from sangeet.extensions import db
from sangeet.models import Track
from pydub.utils import mediainfo
from flask_login import current_user

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

def get_file_duration(file):
    file_info = mediainfo(file)
    total_seconds = float(file_info.get('duration'))
    minutes = int(total_seconds//60)
    seconds = int(total_seconds%60)
    answer = f"{minutes}min {seconds}s"
    print(answer)
    
def get_top_n(table, n):
    query_result = db.session.execute(db.select(table).limit(n)).scalars()
    list = [entry for entry in query_result]
    return list


def refine_track_data(tracks, **kwargs):    # make the tracks list suitable for sending it to the template for getting it rendered
    # # if the page is requesting some type of page context, then do the checking based on that
    # page_type = kwargs.get('page_type')

    def get_track_listing_type(track, **kwargs):
        track_listing_type = {}
        # checking the role, and instructing to show options based on those
        if current_user.role == 'user':
            track_listing_type['role'] = 'user'
        elif (current_user.role == 'creator') and (track.creator_id == current_user.id):
            track_listing_type['role'] = 'creator'
        elif (current_user.role == 'admin'):
            track_listing_type['role'] = 'admin'
        # checking based on the context, like playlist or music
        if kwargs.get('page_type'):
            if (kwargs.get('page_type') == 'playlist') and (kwargs.get('playlist').curator_id == current_user.id):
                track_listing_type['page_type'] = 'playlist'
            elif (kwargs.get('page_type') == 'album') and (kwargs.get('album').creator_id == current_user.id):
                track_listing_type['page_type'] = 'album'
        return track_listing_type
    track_data = {}
    for track in tracks:
        data = {}
        data['track'] = track
        data['track_listing_type'] = get_track_listing_type(track, **kwargs)
        data['is_flagged'] = track.is_flagged
        track_data[track.id] = data
    return track_data