# 【推しの子】究極クイズ - Oshi no Ko Ultimate Quiz

アニメ・漫画『【推しの子】』のファン向け究極クイズアプリケーションです。

![【推しの子】クイズ](https://via.placeholder.com/800x400/9333EA/FFFFFF?text=Oshi+no+Ko+Ultimate+Quiz)

## 機能

このアプリケーションは、『【推しの子】』の世界を深く理解するためのクイズプラットフォームです。初級から上級まで、全100問の問題に挑戦できます。

### クイズ構成

**初級編（30問）**
- 主要キャラクターと物語の始まり（10問）
- 新生B小町と芸能界への一歩（10問）
- アニメ基本情報（10問）

**中級編（40問）**
- 恋愛リアリティショー『今ガチ』編（10問）
- 2.5次元舞台『東京ブレイド』編（10問）
- 転生と過去の因縁（10問）
- 制作の舞台裏（10問）

**上級編（30問）**
- 伏線と考察（10問）
- 黒幕と復讐の行方（10問）
- 原作・制作トリビア（10問）

### 主要機能

**クイズプレイ機能**では、4択問題に対応しており、リアルタイムで進捗が表示されます。クイズ終了後には、S〜Dのランク評価、スコアと正答率、所要時間、全問題の解答詳細と解説が表示されます。

**難易度フィルター**を使用して、初級・中級・上級のクイズを絞り込むことができます。

**統計情報**として、各クイズの問題数、挑戦回数、平均正答率が表示されます。

## 技術スタック

### フロントエンド

- **React 18**: UIライブラリ
- **Vite**: ビルドツール
- **React Router**: ルーティング
- **Tailwind CSS**: スタイリング
- **Lucide React**: アイコン
- **shadcn/ui**: UIコンポーネント

### バックエンド

- **Flask 3.1.1**: Pythonウェブフレームワーク
- **SQLAlchemy 2.0.41**: ORM（オブジェクト関係マッピング）
- **SQLite**: データベース（開発環境）
- **PostgreSQL**: データベース（本番環境推奨）
- **Flask-CORS**: CORS対応
- **Gunicorn**: 本番用WSGIサーバー

## プロジェクト構成

```
oshi-quiz-deploy/
├── backend/                 # バックエンド（Flask API）
│   ├── src/
│   │   ├── models/         # データベースモデル
│   │   │   ├── user.py
│   │   │   └── quiz.py
│   │   ├── routes/         # APIルート
│   │   │   ├── user.py
│   │   │   └── quiz.py
│   │   └── main.py         # メインアプリケーション
│   ├── parse_quiz.py       # Markdownパーサー
│   ├── seed_data.py        # データ投入スクリプト
│   ├── oshinoko_quiz_data.json  # 問題データJSON
│   ├── requirements.txt    # Python依存パッケージ
│   └── gunicorn.conf.py    # Gunicorn設定
├── frontend/               # フロントエンド（React）
│   ├── src/
│   │   ├── components/ui/  # UIコンポーネント
│   │   ├── App.jsx         # メインアプリケーション
│   │   └── main.jsx        # エントリーポイント
│   ├── public/             # 静的ファイル
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md               # このファイル
```

## ローカル開発環境のセットアップ

### 前提条件

以下のソフトウェアがインストールされている必要があります。

- **Python 3.11以上**
- **Node.js 18以上**
- **pnpm**（または npm/yarn）

### バックエンドのセットアップ

```bash
# バックエンドディレクトリに移動
cd backend

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存パッケージをインストール
pip install -r requirements.txt

# データベースを初期化してサンプルデータを投入
python seed_data.py

# 開発サーバーを起動
python src/main.py
```

バックエンドAPIは `http://localhost:5000` で起動します。

### フロントエンドのセットアップ

```bash
# フロントエンドディレクトリに移動
cd frontend

# 依存パッケージをインストール
pnpm install

# 開発サーバーを起動
pnpm run dev
```

フロントエンドは `http://localhost:5173` で起動します。

## Render.comへのデプロイ

詳細なデプロイ手順は `DEPLOY.md` を参照してください。

### 簡単な手順

1. GitHubリポジトリを作成してコードをプッシュ
2. Render.comでアカウントを作成
3. Web Serviceとしてバックエンドをデプロイ
4. Static Siteとしてフロントエンドをデプロイ
5. （オプション）PostgreSQLデータベースを作成

## 環境変数

### バックエンド

- `FLASK_ENV`: 環境（`development` または `production`）
- `DATABASE_URL`: データベース接続URL（PostgreSQL使用時）
- `SECRET_KEY`: セッション暗号化キー

### フロントエンド

- `VITE_API_URL`: バックエンドAPIのURL

## データベーススキーマ

### 主要テーブル

- **users**: ユーザー情報
- **oshi_tags**: 推しタグ（【推しの子】）
- **quizzes**: クイズ情報
- **questions**: 問題
- **choices**: 選択肢
- **quiz_attempts**: 挑戦履歴
- **user_answers**: 回答記録

## API エンドポイント

### クイズ関連

- `GET /api/quizzes`: クイズ一覧を取得
- `GET /api/quizzes/:id`: クイズ詳細を取得
- `POST /api/quizzes/:id/submit`: クイズの回答を送信

### タグ関連

- `GET /api/tags`: タグ一覧を取得

## デザイン

**テーマ**: 【推しの子】の世界観を表現
**カラースキーム**: パープル・ピンクのグラデーション
**背景**: 深いパープルからピンクへのグラデーション
**カード**: 白い半透明、バックドロップブラー効果
**アニメーション**: ホバー時のスケール効果、スムーズなトランジション

## カスタマイズ

### 新しい問題の追加

`【推しの子】究極クイズ（4択選択式）.md` を編集して、`backend/parse_quiz.py` を実行してJSONを再生成し、`seed_data.py` を実行してデータベースに投入します。

```bash
cd backend
python parse_quiz.py
python seed_data.py
```

### デザインのカスタマイズ

`frontend/src/App.jsx` でTailwind CSSのクラスを編集します。

## トラブルシューティング

### CORS エラー

バックエンドの `main.py` で CORS 設定を確認してください。

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### データベース接続エラー

環境変数 `DATABASE_URL` が正しく設定されているか確認してください。

### ビルドエラー

Node.jsとPythonのバージョンが要件を満たしているか確認してください。

## ライセンス

MIT License

## クレジット

- 原作: 赤坂アカ × 横槍メンゴ『【推しの子】』
- クイズデータ: オリジナル編集

## 注意事項

このアプリケーションは非公式のファンメイドプロジェクトです。『【推しの子】』の著作権は原作者および関係各社に帰属します。
