import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes（無料プラン最適化: 512MB RAM対応）
workers = 1  # メモリ制約のため最小限に
worker_class = 'sync'
worker_connections = 500  # 同時接続数を削減
timeout = 180  # 100問バッチ処理のため180秒に延長
keepalive = 2
max_requests = 1000  # メモリリーク対策
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# メモリ最適化
preload_app = False  # メモリ節約のためpreloadしない

