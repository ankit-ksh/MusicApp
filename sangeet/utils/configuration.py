from flask_login import current_user, login_required

def logged_in_vars():
    user_role = current_user.role
    layout_paths = {
        'user' : 'layouts/user_layout.html',
        'creator' : 'layouts/creator_layout.html',
        'admin' : 'layouts/admin_layout.html'
    }
    track_listing_paths = {
        'user' : 'music/music_listing_new.html',
        'creator' : 'creator/track_listing.html',
        'admin' : 'admin/track_listing.html'
    }
    return dict(
        track_listing_template = track_listing_paths.get(user_role),
        layout_path = layout_paths.get(user_role),
    )

def logged_out_vars():
    return dict(
        layout  = 'layouts/logged_out_layout.html'
    )



# This function is passed to the context processor which runs this function every time a template is rendered and 
# accordingly passes the values defined here to the template
# Note : If I just use the @login_required decorator, it won't work since in that case no response is returned by the function
# if the user is not authenticated
def inject_user_data():
    if current_user.is_authenticated:
        context_dict =  dict(
            t_var = f"this is a test variable {current_user.first_name}",
            appropriate_layout = logged_in_vars().get('layout_path'),
            track_listing_template = logged_in_vars().get('track_listing_template'),
        )
    else:
        context_dict = dict(
            appropriate_layout = logged_out_vars().get('layout')
        )
    return context_dict


