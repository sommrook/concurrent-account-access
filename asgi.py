import os
from app.core.settings import API_HOST, API_PORT, API_WORKERS

os.system(f"gunicorn --bind {API_HOST}:{API_PORT} "
          f"--workers {API_WORKERS} "
          f"app.app:app "
          f"--worker-class uvicorn.workers.UvicornWorker "
          f"--access-logfile -")
