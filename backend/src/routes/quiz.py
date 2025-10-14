from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.quiz import Quiz, Question, Choice, QuizAttempt, UserAnswer, OshiTag
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

# タグ一覧取得
@quiz_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = OshiTag.query.all()
    return jsonify([{
        'id': tag.id,
        'name': tag.name,
        'category': tag.category,
        'description': tag.description
    } for tag in tags])

# タグ作成
@quiz_bp.route('/tags', methods=['POST'])
def create_tag():
    data = request.json
    tag = OshiTag(
        name=data['name'],
        category=data['category'],
        description=data.get('description', '')
    )
    db.session.add(tag)
    db.session.commit()
    return jsonify({'id': tag.id, 'name': tag.name}), 201

# クイズ一覧取得
@quiz_bp.route('/quizzes', methods=['GET'])
def get_quizzes():
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    tag_id = request.args.get('tag_id')
    
    query = Quiz.query.filter_by(is_public=True)
    
    if category:
        query = query.join(OshiTag).filter(OshiTag.category == category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if tag_id:
        query = query.filter_by(oshi_tag_id=tag_id)
    
    quizzes = query.order_by(Quiz.created_at.desc()).all()
    return jsonify([quiz.to_dict() for quiz in quizzes])

# クイズ詳細取得
@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return jsonify(quiz.to_dict(include_questions=True))

# クイズ作成
@quiz_bp.route('/quizzes', methods=['POST'])
def create_quiz():
    data = request.json
    
    # クイズ作成
    quiz = Quiz(
        creator_id=data.get('creator_id', 1),  # デモ用
        title=data['title'],
        description=data.get('description', ''),
        oshi_tag_id=data['oshi_tag_id'],
        difficulty=data['difficulty']
    )
    db.session.add(quiz)
    db.session.flush()
    
    # 問題作成
    for q_data in data['questions']:
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data['question_text'],
            question_type=q_data['question_type'],
            order_index=q_data['order_index'],
            explanation=q_data.get('explanation', '')
        )
        db.session.add(question)
        db.session.flush()
        
        # 選択肢作成
        for c_data in q_data['choices']:
            choice = Choice(
                question_id=question.id,
                choice_text=c_data['choice_text'],
                is_correct=c_data['is_correct'],
                order_index=c_data['order_index']
            )
            db.session.add(choice)
    
    db.session.commit()
    return jsonify(quiz.to_dict(include_questions=True)), 201

# クイズ回答送信
@quiz_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    data = request.json
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # 正解数カウント
    score = 0
    total = len(data['answers'])
    
    # 挑戦記録作成
    attempt = QuizAttempt(
        user_id=data.get('user_id', 1),  # デモ用
        quiz_id=quiz_id,
        score=0,  # 後で更新
        total_questions=total,
        time_taken=data.get('time_taken', 0)
    )
    db.session.add(attempt)
    db.session.flush()
    
    # 各回答を処理
    for answer_data in data['answers']:
        question = Question.query.get(answer_data['question_id'])
        selected_choice = Choice.query.get(answer_data['selected_choice_id'])
        
        is_correct = selected_choice.is_correct if selected_choice else False
        if is_correct:
            score += 1
        
        user_answer = UserAnswer(
            attempt_id=attempt.id,
            question_id=answer_data['question_id'],
            selected_choice_id=answer_data['selected_choice_id'],
            is_correct=is_correct
        )
        db.session.add(user_answer)
    
    # スコアとランク計算
    attempt.score = score
    percentage = (score / total * 100) if total > 0 else 0
    
    if percentage >= 90:
        rank = 'S'
    elif percentage >= 75:
        rank = 'A'
    elif percentage >= 60:
        rank = 'B'
    elif percentage >= 40:
        rank = 'C'
    else:
        rank = 'D'
    
    attempt.rank = rank
    
    # クイズ統計更新
    quiz.play_count += 1
    if quiz.play_count > 0:
        # 平均スコア再計算
        all_attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id).all()
        total_score = sum(a.score for a in all_attempts)
        total_questions_sum = sum(a.total_questions for a in all_attempts)
        quiz.average_score = (total_score / total_questions_sum * 100) if total_questions_sum > 0 else 0
    
    db.session.commit()
    
    # 結果を返す
    result = attempt.to_dict()
    result['answers'] = []
    
    for user_answer in attempt.answers:
        question = Question.query.get(user_answer.question_id)
        selected_choice = Choice.query.get(user_answer.selected_choice_id) if user_answer.selected_choice_id else None
        correct_choice = next((c for c in question.choices if c.is_correct), None)
        
        result['answers'].append({
            'question_id': question.id,
            'question_text': question.question_text,
            'selected_choice_id': user_answer.selected_choice_id,
            'selected_choice_text': selected_choice.choice_text if selected_choice else None,
            'correct_choice_id': correct_choice.id if correct_choice else None,
            'correct_choice_text': correct_choice.choice_text if correct_choice else None,
            'is_correct': user_answer.is_correct,
            'explanation': question.explanation
        })
    
    return jsonify(result), 201

# ランキング取得
@quiz_bp.route('/rankings/quizzes', methods=['GET'])
def get_quiz_rankings():
    quizzes = Quiz.query.filter_by(is_public=True).order_by(Quiz.play_count.desc()).limit(10).all()
    return jsonify([quiz.to_dict() for quiz in quizzes])

# クイズ別ランキング取得
@quiz_bp.route('/quizzes/<int:quiz_id>/rankings', methods=['GET'])
def get_quiz_specific_rankings(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # スコアが高い順、同点の場合は時間が短い順でソート
    attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id)\
        .order_by(QuizAttempt.score.desc(), QuizAttempt.time_taken.asc())\
        .limit(100)\
        .all()

    rankings = []
    for idx, attempt in enumerate(attempts, 1):
        user = User.query.get(attempt.user_id)
        percentage = (attempt.score / attempt.total_questions * 100) if attempt.total_questions > 0 else 0

        rankings.append({
            'rank': idx,
            'attempt_id': attempt.id,
            'player_name': user.username if user else 'Unknown',
            'score': attempt.score,
            'total_questions': attempt.total_questions,
            'percentage': round(percentage, 1),
            'time_taken': attempt.time_taken,
            'rank_grade': attempt.rank
        })

    return jsonify({
        'quiz_id': quiz_id,
        'quiz_title': quiz.title,
        'rankings': rankings
    })

