# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sangeet.extensions import db
from sangeet.models import *

bp = Blueprint('admin', __name__)

@bp.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@bp.route('/remove/track', methods=['GET', 'POST'])
def delete_track():
    if request.method == 'POST':
        track_id = request.form.get('track_id')
        if not track_id:
            flash("Invalid Request", 'error')
            return redirect(request.base_url)
        track_to_delete = db.session.get(Track, track_id)
        if track_to_delete:
            try:
                track_name = track_to_delete.name
                db.session.delete(track_to_delete)
                db.session.commit()
                flash(f"Track Deleted : {track_name}", 'success')
                return redirect(request.base_url)
            except Exception as e:
                db.session.rollback()
                flash(f"Error deleting track: {str(e)}", 'error')
                return redirect(request.base_url)
        else:
            flash("Not authenticated")
            return redirect(request.base_url)
    return redirect(request.referrer)
