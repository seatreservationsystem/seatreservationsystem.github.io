
# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():

    user_type = current_user.user_type
    

    if user_type == True:
        return render_template('instructor_profile.html', name=current_user.name, user_type=current_user.user_type)
    return render_template('student_profile.html', name=current_user.name, user_type=current_user.user_type)


