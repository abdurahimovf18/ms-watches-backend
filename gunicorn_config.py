import multiprocessing

# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1  # Typically, 2x CPU cores + 1

# The type of worker to use (Uvicorn worker for FastAPI)
worker_class = "uvicorn.workers.UvicornWorker"

# The bind address for the server
bind = "0.0.0.0:8000"  # You can replace with your server address if needed

# The log level (choices: debug, info, warning, error, critical)
loglevel = "info"

# Access log format (optional, to log incoming requests)
accesslog = "-"  # "-" means output to stdout

# Error log file (optional)
errorlog = "-"  # "-" means output to stderr

# Whether to daemonize the server (run in the background)
daemon = False

# Timeout for workers (in seconds)
timeout = 30  # Adjust as needed

# Reload the server automatically if any code changes (useful in development)
reload = True

# Max number of connections to allow (optional, adjust based on your use case)
max_requests = 20000
max_requests_jitter = 50
