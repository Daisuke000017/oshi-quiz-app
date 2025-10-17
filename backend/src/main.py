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

    # SSL設定を追加（PostgreSQL接続エラー対策）
    if '?' not in database_url:
        database_url += '?sslmode=require'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
else:
    # ローカル開発環境ではSQLiteを使用
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database', 'app.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの初期化
db.init_app(app)

# 起動時の初期化処理（テーブル作成のみ、高速化）
def init_db():
    """データベーステーブルを作成する"""
    try:
        from src.models.quiz import Quiz, Question, Choice, QuizAttempt, UserAnswer, OshiTag
        from src.models.user import User

        print('データベーステーブルを作成中...')
        db.create_all()
        print('✅ データベーステーブルの作成が完了しました')
    except Exception as e:
        print(f'⚠ データベース初期化エラー: {e}')
        import traceback
        traceback.print_exc()

# アプリ起動時にデータベーステーブルを作成のみ（シードデータは手動）
with app.app_context():
    init_db()

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
            'users': '/api/users',
            'seed': '/api/seed (POST)'
        }
    }

# シードデータ投入エンドポイント（デプロイ後に一度だけ実行）
@app.route('/api/seed', methods=['POST'])
def seed_data_endpoint():
    """
    シードデータを投入する（管理者用）

    100問を5問ずつバッチ処理で投入します。
    無料プランのメモリ制約に対応しています。
    """
    try:
        from src.models.quiz import Quiz, Question

        # 既にデータが存在する場合はスキップ
        count = db.session.execute(db.select(db.func.count()).select_from(Quiz)).scalar()
        if count > 0:
            return {
                'status': 'skipped',
                'message': f'既存のクイズデータが {count} 件存在します',
                'count': count
            }, 200

        # シードデータを投入（バッチ処理）
        import sys
        import os
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, backend_dir)

        import seed_data
        print('📚 100問版シードデータの投入を開始します（バッチ処理）')
        seed_data.seed_data()

        # 投入後のカウント
        new_count = db.session.execute(db.select(db.func.count()).select_from(Quiz)).scalar()
        question_count = db.session.execute(db.select(db.func.count()).select_from(Question)).scalar()

        return {
            'status': 'success',
            'message': '100問版シードデータの投入が完了しました',
            'quiz_count': new_count,
            'question_count': question_count
        }, 200
    except Exception as e:
        import traceback
        return {
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')

