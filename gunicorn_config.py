"""
Gunicorn configuration file for Tawi Meridian production deployment.
"""

import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/tawimeridian/access.log"
errorlog = "/var/log/tawimeridian/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "tawimeridian"

# Server mechanics
daemon = False
pidfile = "/var/run/tawimeridian/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if using SSL termination at Gunicorn level)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Server Hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    pass

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    pass

def worker_int(worker):
    """Called when a worker receives the INT or QUIT signal."""
    pass

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    pass

def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    pass

def worker_abort(worker):
    """Called when a worker receives the ABRT signal."""
    pass

def pre_exec(server):
    """Called just before a new master process is forked."""
    pass

def when_ready(server):
    """Called just after the server is started."""
    pass

def on_exit(server):
    """Called just before exiting Gunicorn."""
    pass
