"""
100問版シードデータ - 無料プラン対応（バッチ処理）
推しの子クイズ（100問）を段階的に投入
"""
import os
import sys
import json
import time

# Flaskアプリのコンテキストをインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.user import db, User
from src.models.quiz import Quiz, Question, Choice, OshiTag

def seed_data_batch(batch_size=5):
    """
    バッチ処理でシードデータを投入（無料プラン対応）

    Args:
        batch_size: 一度に処理する問題数（デフォルト5問）
    """

    # ユーザーを作成
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        db.session.add(admin)
        db.session.commit()
        print('✅ 管理者ユーザーを作成しました')

    # 推しの子タグを作成
    oshinoko_tag = OshiTag.query.filter_by(name='推しの子').first()
    if not oshinoko_tag:
        oshinoko_tag = OshiTag(
            name='推しの子',
            category='anime',
            description='アニメ・漫画『【推しの子】』'
        )
        db.session.add(oshinoko_tag)
        db.session.commit()
        print('✅ 推しの子タグを作成しました')

    # JSONファイルから問題データを読み込み
    json_path = os.path.join(os.path.dirname(__file__), 'oshinoko_quiz_data.json')

    if not os.path.exists(json_path):
        print(f'❌ エラー: {json_path} が見つかりません')
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)

    print('📚 【推しの子】クイズデータを投入中...')
    print(f'   バッチサイズ: {batch_size}問ずつ処理')

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
                creator_id=admin.id,
                title=quiz_title,
                description=quiz_description,
                oshi_tag_id=oshinoko_tag.id,
                difficulty=difficulty,
                is_public=True
            )
            db.session.add(quiz)
            db.session.flush()
            quiz_count += 1

            print(f'   📝 クイズ作成: {quiz_title} ({len(questions)}問)')

            # 問題をバッチ処理で作成
            total_questions = len(questions)
            for batch_start in range(0, total_questions, batch_size):
                batch_end = min(batch_start + batch_size, total_questions)
                batch_questions = questions[batch_start:batch_end]

                # バッチ内の各問題を処理
                for q_index, q_data in enumerate(batch_questions, batch_start + 1):
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
                            order_index=c_index
                        )
                        db.session.add(choice)

                # バッチごとにコミット（メモリ解放）
                db.session.commit()
                print(f'      ✓ 問題 {batch_start + 1}~{batch_end} を投入完了')

                # メモリ解放のため少し待機（無料プラン対策）
                if batch_end < total_questions:
                    time.sleep(0.1)

    print('\n✅ 【推しの子】クイズデータの投入が完了しました！')
    print(f'   - クイズ数: {quiz_count}個')
    print(f'   - 総問題数: {question_count}問')

def seed_data():
    """
    メイン関数：バッチサイズ5で実行
    """
    seed_data_batch(batch_size=5)

if __name__ == '__main__':
    from src.main import app
    with app.app_context():
        seed_data()
