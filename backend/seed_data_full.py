import os
import sys
import json
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.user import db, User
from src.models.quiz import OshiTag, Quiz, Question, Choice

def seed_data():
    with app.app_context():
        # データベースをリセット
        db.drop_all()
        db.create_all()

        # サンプルユーザー作成
        user = User(username='oshinoko_fan', name='【推しの子】ファン', email='fan@oshinoko.com')
        db.session.add(user)
        db.session.flush()

        # 【推しの子】タグ作成
        tag = OshiTag(
            name='【推しの子】',
            category='anime',
            description='アニメ・漫画【推しの子】の究極クイズ'
        )
        db.session.add(tag)
        db.session.flush()

        # JSONファイルから問題データを読み込み
        json_path = os.path.join(os.path.dirname(__file__), 'oshinoko_quiz_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)

        print('【推しの子】クイズデータを投入中...')

        quiz_count = 0
        question_count = 0

        # 各難易度のクイズを作成
        for part in quiz_data:
            difficulty = part['difficulty']
            part_name = part['name']

            # 各セットをクイズとして作成
            for set_data in part['sets']:
                set_title = set_data['title']
                questions = set_data['questions']

                # クイズタイトルを生成
                quiz_title = f'【推しの子】{part_name} - {set_title}'

                # クイズの説明を生成
                quiz_description = f'{part_name}の{set_title}に関する問題です。全{len(questions)}問。'

                # クイズを作成
                quiz = Quiz(
                    creator_id=user.id,
                    title=quiz_title,
                    description=quiz_description,
                    oshi_tag_id=tag.id,
                    difficulty=difficulty
                )
                db.session.add(quiz)
                db.session.flush()
                quiz_count += 1

                # 問題を作成
                for q_index, q_data in enumerate(questions, 1):
                    question_text = q_data['question_text']
                    choices_list = q_data['choices']
                    correct_answer = q_data['correct_answer']  # A, B, C, D
                    explanation = q_data.get('explanation', '')

                    # 問題タイプを判定（選択肢が2つなら○×、4つなら4択）
                    question_type = 'true_false' if len(choices_list) == 2 else 'multiple_choice'

                    question = Question(
                        quiz_id=quiz.id,
                        question_text=question_text,
                        question_type=question_type,
                        order_index=q_index,
                        explanation=explanation
                    )
                    db.session.add(question)
                    db.session.flush()
                    question_count += 1

                    # 選択肢を作成
                    correct_index = ord(correct_answer) - ord('A')  # A=0, B=1, C=2, D=3

                    for c_index, choice_text in enumerate(choices_list):
                        is_correct = (c_index == correct_index)

                        choice = Choice(
                            question_id=question.id,
                            choice_text=choice_text,
                            is_correct=is_correct,
                            order_index=c_index + 1
                        )
                        db.session.add(choice)

        db.session.commit()

        print('✅ 【推しの子】クイズデータの投入が完了しました！')
        print(f'- ユーザー: {user.name}')
        print(f'- タグ: {tag.name} ({tag.category})')
        print(f'- クイズ数: {quiz_count}個')
        print(f'- 総問題数: {question_count}問')
        print('\n作成されたクイズ一覧:')

        quizzes = Quiz.query.all()
        for i, q in enumerate(quizzes, 1):
            print(f'{i}. {q.title} ({q.difficulty}, {len(q.questions)}問)')

if __name__ == '__main__':
    seed_data()
