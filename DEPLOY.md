# デプロイガイド - Render.com

このガイドでは、推し活クイズアプリをRender.comにデプロイする手順を説明します。

## 前提条件

以下のアカウントが必要です。

- **GitHubアカウント**: コードをホスティングするため
- **Render.comアカウント**: アプリをデプロイするため（無料プランで可）

## ステップ1: GitHubリポジトリの作成

### 1.1 GitHubで新しいリポジトリを作成

1. GitHubにログインし、右上の「+」→「New repository」をクリックします。
2. リポジトリ名を入力します（例: `oshi-quiz`）。
3. 「Public」または「Private」を選択します。
4. 「Create repository」をクリックします。

### 1.2 ローカルでGitリポジトリを初期化

ダウンロードしたプロジェクトフォルダで以下のコマンドを実行します。

```bash
cd oshi-quiz-deploy

# Gitリポジトリを初期化
git init

# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: Oshi-Katsu Quiz app"

# GitHubリポジトリをリモートとして追加（URLは自分のリポジトリに変更）
git remote add origin https://github.com/yourusername/oshi-quiz.git

# メインブランチにプッシュ
git branch -M main
git push -u origin main
```

## ステップ2: Render.comでバックエンドをデプロイ

### 2.1 Render.comにログイン

1. https://render.com にアクセスします。
2. 「Get Started for Free」をクリックし、GitHubアカウントで登録/ログインします。

### 2.2 Web Serviceを作成

1. ダッシュボードで「New +」→「Web Service」をクリックします。
2. 「Connect a repository」で、先ほど作成したGitHubリポジトリを選択します。
3. 以下の設定を入力します。

**基本設定**
- **Name**: `oshi-quiz-api`（任意の名前）
- **Region**: `Oregon (US West)` または最寄りのリージョン
- **Branch**: `main`
- **Root Directory**: `backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app`

**プラン**
- **Instance Type**: `Free`（無料プラン）

### 2.3 環境変数を設定

「Environment」セクションで以下の環境変数を追加します。

- **FLASK_ENV**: `production`
- **PYTHON_VERSION**: `3.11.0`

### 2.4 デプロイを開始

「Create Web Service」をクリックします。デプロイが開始され、数分で完了します。

### 2.5 バックエンドURLを確認

デプロイが完了したら、画面上部に表示されるURLをコピーします（例: `https://oshi-quiz-api.onrender.com`）。このURLは後で使用します。

## ステップ3: Render.comでフロントエンドをデプロイ

### 3.1 Static Siteを作成

1. ダッシュボードで「New +」→「Static Site」をクリックします。
2. 同じGitHubリポジトリを選択します。
3. 以下の設定を入力します。

**基本設定**
- **Name**: `oshi-quiz-frontend`（任意の名前）
- **Region**: `Oregon (US West)` または最寄りのリージョン
- **Branch**: `main`
- **Root Directory**: `frontend`
- **Build Command**: `pnpm install && pnpm run build`
- **Publish Directory**: `dist`

### 3.2 環境変数を設定

「Environment」セクションで以下の環境変数を追加します。

- **VITE_API_URL**: バックエンドのURL（ステップ2.5でコピーしたURL）

例: `https://oshi-quiz-api.onrender.com`

### 3.3 デプロイを開始

「Create Static Site」をクリックします。デプロイが開始され、数分で完了します。

### 3.4 フロントエンドURLを確認

デプロイが完了したら、画面上部に表示されるURLにアクセスして、アプリが正常に動作することを確認します。

## ステップ4: データベースのセットアップ（オプション）

無料プランではSQLiteが使用されますが、本番環境ではPostgreSQLの使用を推奨します。

### 4.1 PostgreSQLデータベースを作成

1. ダッシュボードで「New +」→「PostgreSQL」をクリックします。
2. 以下の設定を入力します。
   - **Name**: `oshi-quiz-db`
   - **Region**: バックエンドと同じリージョン
   - **Plan**: `Free`

3. 「Create Database」をクリックします。

### 4.2 データベースURLを取得

作成されたデータベースの詳細ページで「Internal Database URL」をコピーします。

### 4.3 バックエンドに環境変数を追加

バックエンドのWeb Serviceの「Environment」セクションで以下の環境変数を追加します。

- **DATABASE_URL**: コピーしたInternal Database URL

### 4.4 バックエンドコードを修正

`backend/src/main.py` を以下のように修正します。

```python
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# データベース設定
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Render.comのPostgreSQL URLを修正
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ... 残りのコード
```

### 4.5 データベースを初期化

バックエンドのデプロイが完了したら、以下のコマンドでデータベースを初期化します。

```bash
# Render.comのシェルにアクセス
# ダッシュボードでバックエンドサービスを開き、「Shell」タブをクリック

# データベースを初期化
python seed_data.py
```

## ステップ5: 自動デプロイの設定

GitHubにプッシュすると自動的にデプロイされるように設定されています。コードを変更した場合は、以下のコマンドでデプロイできます。

```bash
git add .
git commit -m "Update: 変更内容の説明"
git push origin main
```

Render.comが自動的に変更を検知し、再デプロイを開始します。

## トラブルシューティング

### デプロイが失敗する場合

1. **ビルドログを確認**: Render.comのダッシュボードで「Logs」タブを開き、エラーメッセージを確認します。
2. **環境変数を確認**: すべての必要な環境変数が正しく設定されているか確認します。
3. **依存パッケージを確認**: `requirements.txt` と `package.json` に必要なパッケージがすべて含まれているか確認します。

### CORSエラーが発生する場合

バックエンドの `main.py` で CORS 設定を確認します。

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### データベース接続エラーが発生する場合

1. `DATABASE_URL` 環境変数が正しく設定されているか確認します。
2. PostgreSQLのURLが `postgresql://` で始まっているか確認します（`postgres://` ではない）。

### フロントエンドからAPIにアクセスできない場合

1. `VITE_API_URL` 環境変数が正しく設定されているか確認します。
2. バックエンドのURLが正しいか確認します（末尾にスラッシュが不要）。
3. ブラウザの開発者ツールでネットワークタブを開き、APIリクエストのURLを確認します。

## 無料プランの制限

Render.comの無料プランには以下の制限があります。

- **スリープ**: 15分間アクセスがないとサービスがスリープします。次回アクセス時に起動するまで数秒かかります。
- **実行時間**: 月間750時間まで無料です。
- **帯域幅**: 月間100GBまで無料です。
- **ビルド時間**: 月間500分まで無料です。

本格的な運用には有料プランへのアップグレードを検討してください。

## まとめ

これで推し活クイズアプリがRender.comにデプロイされました！🎉

- **フロントエンドURL**: `https://oshi-quiz-frontend.onrender.com`
- **バックエンドURL**: `https://oshi-quiz-api.onrender.com`

アプリを共有して、友達と一緒に推し愛を試しましょう！

