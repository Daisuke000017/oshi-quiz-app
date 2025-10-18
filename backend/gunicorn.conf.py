import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes（Professional Plan最適化: 4GB RAM）
workers = 4  # Professionalプランの潤沢なメモリを活用
worker_class = 'sync'
worker_connections = 1000
timeout = 120  # 通常のタイムアウト設定
keepalive = 5
max_requests = 1000  # メモリリーク対策
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# パフォーマンス最適化
preload_app = True  # アプリを事前読み込みして起動を高速化

