from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.quiz import Quiz, Category
from models.question import Question
from models.result import Result
from utils.helpers import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    total_users = User.query.count()
    total_quizzes = Quiz.query.count()
    total_questions = Question.query.count()
    total_attempts = Result.query.count()
    categories = Category.query.all()
    recent_results = Result.query.order_by(Result.completed_at.desc()).limit(5).all()

    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_quizzes=total_quizzes,
                           total_questions=total_questions,
                           total_attempts=total_attempts,
                           categories=categories,
                           recent_results=recent_results)


# ---------------------- CATEGORIES ---------------------- #
@admin_bp.route('/admin/category/add', methods=['POST'])
@admin_required
def add_category():
    category_name = request.form.get('category_name', '').strip()
    if not category_name:
        flash('Category name cannot be empty.', 'danger')
        return redirect(url_for('admin.dashboard'))

    existing = Category.query.filter_by(category_name=category_name).first()
    if existing:
        flash('Category already exists.', 'warning')
        return redirect(url_for('admin.dashboard'))

    new_cat = Category(category_name=category_name)
    try:
        db.session.add(new_cat)
        db.session.commit()
        flash(f'Category "{category_name}" created successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('Error creating category.', 'danger')

    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/admin/category/delete/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    cat = Category.query.get_or_404(category_id)
    try:
        db.session.delete(cat)
        db.session.commit()
        flash(f'Category "{cat.category_name}" and related quizzes deleted.', 'success')
    except Exception:
        db.session.rollback()
        flash('Error deleting category.', 'danger')
    return redirect(url_for('admin.dashboard'))


# ---------------------- QUIZZES ---------------------- #
@admin_bp.route('/admin/quizzes')
@admin_required
def manage_quizzes():
    quizzes = Quiz.query.all()
    categories = Category.query.all()
    return render_template('manage_quizzes.html', quizzes=quizzes, categories=categories)


@admin_bp.route('/admin/quiz/add', methods=['POST'])
@admin_required
def add_quiz():
    quiz_title = request.form.get('quiz_title', '').strip()
    category_id = request.form.get('category_id', type=int)
    description = request.form.get('description', '').strip()
    time_limit = request.form.get('time_limit', type=int, default=10)
    total_questions = request.form.get('total_questions', type=int, default=10)

    if not quiz_title or not category_id:
        flash('Quiz title and category are required.', 'danger')
        return redirect(url_for('admin.manage_quizzes'))

    new_quiz = Quiz(
        quiz_title=quiz_title,
        category_id=category_id,
        description=description,
        time_limit=time_limit,
        total_questions=total_questions
    )

    try:
        db.session.add(new_quiz)
        db.session.commit()
        flash(f'Quiz "{quiz_title}" created successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('Error adding new quiz.', 'danger')

    return redirect(url_for('admin.manage_quizzes'))


@admin_bp.route('/admin/quiz/edit/<int:quiz_id>', methods=['POST'])
@admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.quiz_title = request.form.get('quiz_title', quiz.quiz_title).strip()
    quiz.category_id = request.form.get('category_id', type=int, default=quiz.category_id)
    quiz.description = request.form.get('description', quiz.description).strip()
    quiz.time_limit = request.form.get('time_limit', type=int, default=quiz.time_limit)
    quiz.total_questions = request.form.get('total_questions', type=int, default=quiz.total_questions)

    try:
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('Error updating quiz.', 'danger')

    return redirect(url_for('admin.manage_quizzes'))


@admin_bp.route('/admin/quiz/delete/<int:quiz_id>', methods=['POST'])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    try:
        db.session.delete(quiz)
        db.session.commit()
        flash(f'Quiz "{quiz.quiz_title}" deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('Error deleting quiz.', 'danger')
    return redirect(url_for('admin.manage_quizzes'))


# ---------------------- QUESTIONS ---------------------- #
@admin_bp.route('/admin/questions')
@admin_required
def manage_questions():
    quiz_id = request.args.get('quiz_id', type=int)
    quizzes = Quiz.query.all()

    if quiz_id:
        selected_quiz = Quiz.query.get(quiz_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
    else:
        selected_quiz = quizzes[0] if quizzes else None
        questions = Question.query.filter_by(quiz_id=selected_quiz.quiz_id).all() if selected_quiz else []

    return render_template('manage_questions.html',
                           quizzes=quizzes,
                           selected_quiz=selected_quiz,
                           questions=questions)


@admin_bp.route('/admin/question/add', methods=['POST'])
@admin_required
def add_question():
    quiz_id = request.form.get('quiz_id', type=int)
    question_text = request.form.get('question', '').strip()
    option_a = request.form.get('option_a', '').strip()
    option_b = request.form.get('option_b', '').strip()
    option_c = request.form.get('option_c', '').strip()
    option_d = request.form.get('option_d', '').strip()
    correct_answer = request.form.get('correct_answer', '').strip().upper()

    if not all([quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer]):
        flash('All question fields are required.', 'danger')
        return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))

    new_q = Question(
        quiz_id=quiz_id,
        question=question_text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer
    )

    try:
        db.session.add(new_q)
        db.session.commit()
        flash('Question added successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('Error creating question.', 'danger')

    return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))


@admin_bp.route('/admin/question/edit/<int:question_id>', methods=['POST'])
@admin_required
def edit_question(question_id):
    q = Question.query.get_or_404(question_id)
    q.question = request.form.get('question', q.question).strip()
    q.option_a = request.form.get('option_a', q.option_a).strip()
    q.option_b = request.form.get('option_b', q.option_b).strip()
    q.option_c = request.form.get('option_c', q.option_c).strip()
    q.option_d = request.form.get('option_d', q.option_d).strip()
    q.correct_answer = request.form.get('correct_answer', q.correct_answer).strip().upper()

    try:
        db.session.commit()
        flash('Question updated successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('Error updating question.', 'danger')

    return redirect(url_for('admin.manage_questions', quiz_id=q.quiz_id))


@admin_bp.route('/admin/question/delete/<int:question_id>', methods=['POST'])
@admin_required
def delete_question(question_id):
    q = Question.query.get_or_404(question_id)
    quiz_id = q.quiz_id
    try:
        db.session.delete(q)
        db.session.commit()
        flash('Question deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('Error deleting question.', 'danger')

    return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))


# ---------------------- USERS & REPORTS ---------------------- #
@admin_bp.route('/admin/users')
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('manage_users.html', users=users)


@admin_bp.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    try:
        db.session.delete(u)
        db.session.commit()
        flash(f'User "{u.full_name}" deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('Error deleting user.', 'danger')

    return redirect(url_for('admin.manage_users'))
