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

    # 本番環境で初回起動時、古いテーブル構造をリセット
    # RESET_DB環境変数がtrueの場合のみ実行
    if os.environ.get('RESET_DB') == 'true':
        print('⚠️  RESET_DB=trueが設定されています。推しの子クイズアプリのテーブルをリセットします...')

        # 推しの子クイズアプリのテーブルだけを削除（他のアプリのテーブルは保持）
        try:
            # 依存関係のある順番で削除
            from src.models.user import User

            # テーブルが存在する場合のみ削除
            tables_to_drop = [
                UserAnswer.__table__,
                QuizAttempt.__table__,
                Choice.__table__,
                Question.__table__,
                Quiz.__table__,
                OshiTag.__table__,
                User.__table__
            ]

            for table in tables_to_drop:
                try:
                    table.drop(db.engine, checkfirst=True)
                    print(f'  ✓ テーブル {table.name} を削除しました')
                except Exception as e:
                    print(f'  ⚠ テーブル {table.name} の削除をスキップ: {e}')

            # 新しいスキーマでテーブルを再作成
            db.create_all()
            print('✅ テーブルの再作成が完了しました')

            # シードデータを投入
            print('シードデータを投入します...')
            try:
                import seed_data
                seed_data.seed_data()
                print('✅ シードデータの投入が完了しました')
            except Exception as e:
                print(f'❌ シードデータの投入中にエラーが発生しました: {e}')

        except Exception as e:
            print(f'❌ テーブルのリセット中にエラーが発生しました: {e}')
            # エラーが発生してもアプリは起動を続ける
            db.create_all()
    else:
        # 通常起動時はテーブルを作成するのみ
        db.create_all()

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
        except Exception as e:
            print(f'データベースの確認中にエラーが発生しました: {e}')

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

