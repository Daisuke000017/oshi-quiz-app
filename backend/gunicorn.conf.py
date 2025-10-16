import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 2  # 無料インスタンスのメモリ制約のため減らす
worker_class = 'sync'
worker_connections = 1000
timeout = 120  # シードデータ投入のため120秒に延長
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

