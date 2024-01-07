from flask_login import current_user

def get_user_layout():
    user_role = current_user.role
    layout_paths = {
        'user' : 'layouts/user_layout.html',
        'creator' : 'layouts/creator_layout.html',
        'admin' : 'layouts/admin_layout.html',
    }
    return layout_paths.get(user_role)

# passing common variables, related to a user through context processor
def inject_user_data():
    return dict(
        t_var = f"this is a test variable mr. {current_user.first_name}",
        appropriate_layout = get_user_layout()
    )