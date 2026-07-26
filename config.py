import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-quiz-app-2026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # DB environment variables
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'online_quiz_db')

    # Construct MySQL URI if DATABASE_URL is not set
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        # Check if USE_SQLITE flag or fallback is requested
        if os.environ.get('USE_SQLITE', 'false').lower() == 'true':
            DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'online_quiz.db')
        else:
            if DB_PASSWORD:
                DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            else:
                DATABASE_URL = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

