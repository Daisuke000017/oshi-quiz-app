# クイックスタートガイド

このガイドでは、推し活クイズアプリを最速でデプロイする手順を説明します。

## 📦 ダウンロードしたファイル

`oshi-quiz-deploy.zip` を解凍すると、以下の構成になっています。

```
oshi-quiz-deploy/
├── backend/          # バックエンド（Flask API）
├── frontend/         # フロントエンド（React）
├── README.md         # 詳細なドキュメント
├── DEPLOY.md         # デプロイ手順の詳細
├── QUICKSTART.md     # このファイル
└── .gitignore        # Git除外設定
```

## 🚀 最速デプロイ（5ステップ）

### ステップ1: GitHubにアップロード

```bash
# 解凍したフォルダに移動
cd oshi-quiz-deploy

# Gitリポジトリを初期化
git init
git add .
git commit -m "Initial commit"

# GitHubリポジトリを作成して接続（URLは自分のものに変更）
git remote add origin https://github.com/yourusername/oshi-quiz.git
git branch -M main
git push -u origin main
```

### ステップ2: Render.comにログイン

https://render.com にアクセスし、GitHubアカウントでログインします。

### ステップ3: バックエンドをデプロイ

1. 「New +」→「Web Service」をクリック
2. GitHubリポジトリを選択
3. 以下を入力：
   - **Name**: `oshi-quiz-api`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app`
4. 環境変数を追加：
   - `FLASK_ENV` = `production`
5. 「Create Web Service」をクリック
6. デプロイ完了後、URLをコピー（例: `https://oshi-quiz-api.onrender.com`）

### ステップ4: フロントエンドをデプロイ

1. 「New +」→「Static Site」をクリック
2. 同じGitHubリポジトリを選択
3. 以下を入力：
   - **Name**: `oshi-quiz-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `pnpm install && pnpm run build`
   - **Publish Directory**: `dist`
4. 環境変数を追加：
   - `VITE_API_URL` = バックエンドのURL（ステップ3でコピーしたもの）
5. 「Create Static Site」をクリック

### ステップ5: アクセス

デプロイ完了後、フロントエンドのURLにアクセスすれば完了です！🎉

## 🔧 ローカルで動作確認

デプロイ前にローカルで動作確認したい場合：

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py
python src/main.py
```

→ http://localhost:5000 で起動

### フロントエンド

```bash
cd frontend
pnpm install
pnpm run dev
```

→ http://localhost:5173 で起動

## 📚 詳細情報

- **README.md**: プロジェクトの詳細な説明
- **DEPLOY.md**: デプロイ手順の詳細（PostgreSQL設定など）

## ❓ よくある質問

**Q: 無料で使えますか？**
A: はい、Render.comの無料プランで動作します。ただし、15分間アクセスがないとスリープします。

**Q: データベースはどうなっていますか？**
A: デフォルトではSQLiteを使用します。本番環境ではPostgreSQLへの移行を推奨します（DEPLOY.mdを参照）。

**Q: コードを変更したらどうすればいいですか？**
A: GitHubにプッシュすれば自動的に再デプロイされます。

```bash
git add .
git commit -m "Update"
git push
```

**Q: エラーが出ました**
A: Render.comのダッシュボードで「Logs」タブを開き、エラーメッセージを確認してください。

## 🎉 完了！

これで推し活クイズアプリがインターネット上で公開されました！

URLを友達に共有して、一緒に推し愛を試しましょう！

