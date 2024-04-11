import math
from sangeet.extensions import db
from sangeet.models import *
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

# Get the level of access we have to give each user for each track so determing the track listing level or type
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

def extract_track_data(track):
    single_track_data = {}
    single_track_data['track_id'] = track.id
    single_track_data['track'] = track
    try:
        single_track_data['english_lyrics'] = track.lyrics[0].lyrics
    except:
        single_track_data['english_lyrics'] = ''
    return single_track_data


# for storing data of any spcific collection mixed with the current user logged in
# to give the authorized person the ability to modify it
def extract_music_collection_data(music_collection):
    if not music_collection:
        return None
    music_collection_data = dict(
        content = music_collection,
        type = music_collection.__tablename__,
        name = music_collection.name,
        is_user_owner = False
    )
    if (music_collection.__tablename__ == 'playlist') and (music_collection.curator_id == current_user.id):
        music_collection_data['is_user_owner'] = True
    elif (music_collection.__tablename__ == 'album'):
        if music_collection.creator_id == current_user.id:
            music_collection_data['is_user_owner'] = True
    elif (music_collection.__tablename__ == 'creator'):
            music_collection_data['is_user_owner'] = True
    return music_collection_data
    
# make the tracks list suitable for sending it to the template for getting it rendered
# a dictionary of two dictionary providing data about tracks listing and the collection itself, about the permissions of the user etc    
# hide the track if the current user is just a simple user and the track is flagged
# ------------- depends on the function extract_music_collection_data -------------------
def refine_music_data(**kwargs):
    music_page_data = {}
    # getting track data in list of dictionaries if the variable tracks exists in kwargs
    tracks = kwargs.get('tracks', None)
    if tracks:
        track_data = []
        for track in tracks:
            if (track.is_flagged == True): # don't show the user any flagged song, but the original creator and admins can see it   
                if (current_user.role == 'user') or (current_user.role == 'creator' and track.creator_id != current_user.id):
                    continue    # don't include the current track if the above if condition evaluates to true
            single_track_data = extract_track_data(track)
            single_track_data['track_listing_type'] = get_track_listing_type(track, **kwargs)
            track_data.append(single_track_data)
            print(single_track_data.get('track').name)
        music_page_data['tracks'] = track_data

    # if music collection variable exists then provide help to the template in providing options based on that
    music_collection =  kwargs.get('music_collection', None)
    music_page_data['music_collection'] = extract_music_collection_data(music_collection)
    return music_page_data

# grouping any large list into smaller lists of n size
def group_by_n(content, n=6):
    num_iter = math.ceil(len(content)/5)
    new_content = []
    i = 0
    for index in range(num_iter):
        tmp = content[i:i+n]
        new_content.append(tmp)
        i += n
    return new_content

#make content ready for displaying in a card format
def refine_music_data_cards(**kwargs):
    content = kwargs.get('content')
    content = group_by_n(content)
    title_to_display = kwargs.get('title')
    content_type = kwargs.get('content_type')
    music_data = {}
    content_types = {
            'playlist':{'create_link':'/playlist/create'},
            'album':{'create_link':'/album/create'},
            'track':{'create_link':'/track/upload'}
    }
    music_data['content'] = content
    music_data['content_card_path'] = f'music/music_item_cards/{content_type}.html'
    music_data['content_type'] = content_type
    if content_type == 'playlist':
        music_data['links'] = {'Create a new playlist':'/playlist/create'}
    elif content_type == 'album' and current_user.role == 'creator':
        music_data['links'] = {'Create a new album':'/album/create'}
    elif content_type == 'track':
        music_data['links'] = {'Create a new track':'/track/create'}

    return music_data
    
