import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.quiz import quiz_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# CORS設定 - フロントエンドからのアクセスを許可
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ブループリントの登録
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(quiz_bp, url_prefix='/api')

# データベース設定
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Render.comのPostgreSQL URLを修正
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # ローカル開発環境ではSQLiteを使用
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database', 'app.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの初期化
db.init_app(app)
with app.app_context():
    from src.models.quiz import Quiz, Question, Choice, QuizAttempt, UserAnswer, OshiTag

    # データベースのマイグレーション処理
    # テーブルを削除せずに、不足しているカラムを追加する
    try:
        from sqlalchemy import inspect, text
        from src.models.user import User

        inspector = inspect(db.engine)

        # 全テーブルのスキーマ定義
        table_schemas = {
            'quizzes': {
                'creator_id': 'INTEGER',
                'oshi_tag_id': 'INTEGER',
                'difficulty': 'VARCHAR(20)',
                'play_count': 'INTEGER DEFAULT 0',
                'average_score': 'FLOAT DEFAULT 0.0',
                'rating': 'FLOAT DEFAULT 0.0',
                'rating_count': 'INTEGER DEFAULT 0',
                'is_public': 'BOOLEAN DEFAULT TRUE',
                'created_at': 'TIMESTAMP',
                'updated_at': 'TIMESTAMP'
            },
            'questions': {
                'order_index': 'INTEGER DEFAULT 0',
                'explanation': 'TEXT',
                'created_at': 'TIMESTAMP'
            },
            'choices': {
                'order_index': 'INTEGER DEFAULT 0',
                'is_correct': 'BOOLEAN DEFAULT FALSE'
            },
            'oshi_tags': {
                'category': 'VARCHAR(50)',
                'description': 'TEXT',
                'created_at': 'TIMESTAMP'
            },
            'users': {
                'created_at': 'TIMESTAMP'
            }
        }

        # 各テーブルのカラムをチェック・追加
        for table_name, required_columns in table_schemas.items():
            if inspector.has_table(table_name):
                print(f'既存の{table_name}テーブルを確認しています...')
                columns = [col['name'] for col in inspector.get_columns(table_name)]

                missing_columns = []
                for col_name, col_type in required_columns.items():
                    if col_name not in columns:
                        missing_columns.append((col_name, col_type))

                if missing_columns:
                    print(f'  不足しているカラムを追加します: {[col[0] for col in missing_columns]}')
                    for col_name, col_type in missing_columns:
                        try:
                            with db.engine.connect() as conn:
                                conn.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}'))

                                # 特定のカラムにデフォルト値を設定
                                if table_name == 'quizzes':
                                    if col_name == 'creator_id':
                                        conn.execute(text('UPDATE quizzes SET creator_id = 1 WHERE creator_id IS NULL'))
                                    elif col_name == 'oshi_tag_id':
                                        conn.execute(text('UPDATE quizzes SET oshi_tag_id = 1 WHERE oshi_tag_id IS NULL'))
                                    elif col_name == 'difficulty':
                                        conn.execute(text("UPDATE quizzes SET difficulty = 'intermediate' WHERE difficulty IS NULL"))

                                conn.commit()
                            print(f'    ✓ カラム {col_name} を追加しました')
                        except Exception as e:
                            print(f'    ⚠ カラム {col_name} の追加をスキップ: {e}')
                else:
                    print(f'  {table_name}テーブルは最新の構造です')

        # テーブルが存在しない場合は作成
        db.create_all()
        print('✅ データベースの初期化が完了しました')

        # テーブルが空の場合のみシードデータを投入
        try:
            count = db.session.execute(db.select(db.func.count()).select_from(Quiz)).scalar()
            if count == 0:
                print('データベースが空です。シードデータを投入します...')
                try:
                    import seed_data
                    seed_data.seed_data()
                    print('✅ シードデータの投入が完了しました')
                except Exception as e:
                    print(f'シードデータの投入中にエラーが発生しました: {e}')
            else:
                print(f'既存のクイズデータが {count} 件見つかりました')
        except Exception as e:
            print(f'データベースの確認中にエラーが発生しました: {e}')

    except Exception as e:
        print(f'データベースのマイグレーション中にエラーが発生しました: {e}')
        # エラーが発生してもテーブルは作成する
        db.create_all()

# ヘルスチェックエンドポイント
@app.route('/')
def health_check():
    return {'status': 'ok', 'message': 'Oshi-Katsu Quiz API is running'}

@app.route('/api')
def api_info():
    return {
        'name': 'Oshi-Katsu Quiz API',
        'version': '1.0.0',
        'endpoints': {
            'quizzes': '/api/quizzes',
            'tags': '/api/tags',
            'users': '/api/users'
        }
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')

