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

