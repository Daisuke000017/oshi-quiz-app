from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class OshiTag(db.Model):
    __tablename__ = 'oshi_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # anime/manga/idol/vtuber/other
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    quizzes = db.relationship('Quiz', backref='oshi_tag', lazy=True)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    oshi_tag_id = db.Column(db.Integer, db.ForeignKey('oshi_tags.id'), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # beginner/intermediate/advanced/mania
    play_count = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True)
    
    def to_dict(self, include_questions=False):
        data = {
            'id': self.id,
            'creator_id': self.creator_id,
            'title': self.title,
            'description': self.description,
            'oshi_tag': {
                'id': self.oshi_tag.id,
                'name': self.oshi_tag.name,
                'category': self.oshi_tag.category
            } if self.oshi_tag else None,
            'difficulty': self.difficulty,
            'play_count': self.play_count,
            'average_score': self.average_score,
            'rating': self.rating,
            'rating_count': self.rating_count,
            'created_at': self.created_at.isoformat(),
            'question_count': len(self.questions)
        }
        if include_questions:
            data['questions'] = [q.to_dict() for q in self.questions]
        return data

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # multiple_choice/true_false
    order_index = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    choices = db.relationship('Choice', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_answer=False):
        data = {
            'id': self.id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'order_index': self.order_index,
            'choices': [c.to_dict(include_answer) for c in sorted(self.choices, key=lambda x: x.order_index)]
        }
        if include_answer:
            data['explanation'] = self.explanation
        return data

class Choice(db.Model):
    __tablename__ = 'choices'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    choice_text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, nullable=False)
    
    def to_dict(self, include_answer=False):
        data = {
            'id': self.id,
            'choice_text': self.choice_text,
            'order_index': self.order_index
        }
        if include_answer:
            data['is_correct'] = self.is_correct
        return data

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)  # seconds
    rank = db.Column(db.String(1))  # S/A/B/C/D
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    answers = db.relationship('UserAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': round((self.score / self.total_questions * 100), 1) if self.total_questions > 0 else 0,
            'time_taken': self.time_taken,
            'rank': self.rank,
            'completed_at': self.completed_at.isoformat()
        }

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'))
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'selected_choice_id': self.selected_choice_id,
            'is_correct': self.is_correct
        }

