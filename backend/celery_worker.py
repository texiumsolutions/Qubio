# backend/celery_worker.py

from celery import Celery
from backend.config import Config

celery_app = Celery("bio_tasks", broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

# Optional: For Flask context if needed
def make_celery(app):
    celery_app.conf.update(app.config)
    return celery_app
