import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.quiz import Quiz, Category
from models.question import Question
from models.result import Result
from models.user import User
from utils.helpers import login_required

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/')
def index():
    if session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))

    categories = Category.query.all()
    featured_quizzes = Quiz.query.limit(6).all()
    total_quizzes = Quiz.query.count()
    total_users = User.query.count()
    total_attempts = Result.query.count()
    return render_template('index.html',
                           categories=categories,
                           featured_quizzes=featured_quizzes,
                           total_quizzes=total_quizzes,
                           total_users=total_users,
                           total_attempts=total_attempts)



@quiz_bp.route('/quizzes')
def quiz_list():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str).strip()
    category_id = request.args.get('category', type=int)

    query = Quiz.query

    if search_query:
        query = query.filter(Quiz.quiz_title.ilike(f'%{search_query}%') | Quiz.description.ilike(f'%{search_query}%'))

    if category_id:
        query = query.filter(Quiz.category_id == category_id)

    pagination = query.paginate(page=page, per_page=6, error_out=False)
    categories = Category.query.all()

    return render_template('quiz_list.html',
                           pagination=pagination,
                           categories=categories,
                           search_query=search_query,
                           selected_category=category_id)


@quiz_bp.route('/quiz/<int:quiz_id>')
@login_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    if not questions:
        flash('This quiz has no questions available yet.', 'warning')
        return redirect(url_for('quiz.quiz_list'))

    # Shuffle questions for randomness
    shuffled_questions = list(questions)
    random.shuffle(shuffled_questions)

    # Store active quiz state in session to protect timer / duration
    session[f'quiz_{quiz_id}_questions'] = [q.question_id for q in shuffled_questions]

    return render_template('quiz.html', quiz=quiz, questions=shuffled_questions)


@quiz_bp.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    user_id = session.get('user_id')

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if not questions:
        flash('Error submitting quiz: No questions found.', 'danger')
        return redirect(url_for('quiz.quiz_list'))

    score = 0
    total_marks = len(questions)
    detailed_results = []

    for question in questions:
        user_answer = request.form.get(f'question_{question.question_id}', '').strip().upper()
        is_correct = (user_answer == question.correct_answer)
        if is_correct:
            score += 1

        detailed_results.append({
            'question': question.question,
            'option_a': question.option_a,
            'option_b': question.option_b,
            'option_c': question.option_c,
            'option_d': question.option_d,
            'correct_answer': question.correct_answer,
            'user_answer': user_answer,
            'is_correct': is_correct
        })

    percentage = round((score / total_marks) * 100, 2) if total_marks > 0 else 0.0

    new_result = Result(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        total_marks=total_marks,
        percentage=percentage
    )

    try:
        db.session.add(new_result)
        db.session.commit()
        
        # Save submission details in session temporarily for immediate result display
        session[f'last_result_{new_result.result_id}'] = detailed_results
        
        flash('Quiz submitted successfully!', 'success')
        return redirect(url_for('quiz.view_result', result_id=new_result.result_id))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while saving your quiz result.', 'danger')
        return redirect(url_for('quiz.quiz_list'))


@quiz_bp.route('/result/<int:result_id>')
@login_required
def view_result(result_id):
    result = Result.query.get_or_404(result_id)
    user_id = session.get('user_id')

    # Security check: ensure user owns this result or is admin
    if result.user_id != user_id and session.get('role') != 'admin':
        flash('Unauthorized access to result.', 'danger')
        return redirect(url_for('user.dashboard'))

    quiz = Quiz.query.get(result.quiz_id)
    detailed_results = session.get(f'last_result_{result_id}', None)

    # Reconstruct questions details if not in session
    if not detailed_results:
        questions = Question.query.filter_by(quiz_id=result.quiz_id).all()
        detailed_results = []
        for q in questions:
            detailed_results.append({
                'question': q.question,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_answer': q.correct_answer,
                'user_answer': None,
                'is_correct': None
            })

    return render_template('result.html', result=result, quiz=quiz, detailed_results=detailed_results)


@quiz_bp.route('/leaderboard')
def leaderboard():
    # Leaderboard query: top results ordered by score & percentage
    top_results = db.session.query(Result, User, Quiz)\
        .join(User, Result.user_id == User.user_id)\
        .join(Quiz, Result.quiz_id == Quiz.quiz_id)\
        .order_by(Result.percentage.desc(), Result.completed_at.asc())\
        .limit(20).all()

    return render_template('leaderboard.html', top_results=top_results)
