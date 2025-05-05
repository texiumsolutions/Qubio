import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    LOG_FOLDER = os.path.join(os.getcwd(), "logs")
    ALLOWED_EXTENSIONS = {"pdb"}

    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


config = Config()
