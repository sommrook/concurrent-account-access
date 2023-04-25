from app.core.settings import API_HOST, API_PORT, API_WORKERS

bind = f'{API_HOST}:{API_PORT}'
workers = f'{API_WORKERS}'
wsgi_app = 'annotator_api.app:annotator_app'
worker_class = 'uvicorn.workers.UvicornWorker'
accesslog = '-'