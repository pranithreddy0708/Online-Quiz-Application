from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.result import Result
from models.quiz import Quiz
from utils.helpers import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    # Fetch user stats
    user_results = Result.query.filter_by(user_id=user_id).order_by(Result.completed_at.desc()).all()
    total_attempts = len(user_results)
    
    if total_attempts > 0:
        avg_percentage = round(sum(r.percentage for r in user_results) / total_attempts, 1)
        highest_score = max(r.percentage for r in user_results)
    else:
        avg_percentage = 0
        highest_score = 0

    recent_attempts = user_results[:5]
    available_quizzes = Quiz.query.limit(4).all()

    return render_template(
        'dashboard.html',
        user=user,
        total_attempts=total_attempts,
        avg_percentage=avg_percentage,
        highest_score=highest_score,
        recent_attempts=recent_attempts,
        available_quizzes=available_quizzes
    )


@user_bp.route('/history')
@login_required
def history():
    user_id = session.get('user_id')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    pagination = Result.query.filter_by(user_id=user_id)\
        .order_by(Result.completed_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('history.html', pagination=pagination)


@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()

        if not full_name or not email:
            flash('All fields are required.', 'danger')
            return render_template('edit_profile.html', user=user)

        existing_user = User.query.filter(User.email == email, User.user_id != user_id).first()
        if existing_user:
            flash('That email address is already in use by another account.', 'danger')
            return render_template('edit_profile.html', user=user)

        user.full_name = full_name
        user.email = email
        
        try:
            db.session.commit()
            session['user_name'] = user.full_name
            session['user_email'] = user.email
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.dashboard'))
        except Exception:
            db.session.rollback()
            flash('An error occurred while updating profile.', 'danger')

    return render_template('edit_profile.html', user=user)


@user_bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('change_password.html')

        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'danger')
            return render_template('change_password.html')

        user.set_password(new_password)
        try:
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('user.dashboard'))
        except Exception:
            db.session.rollback()
            flash('An error occurred while changing password.', 'danger')

    return render_template('change_password.html')
