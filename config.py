"""
Configuration settings for the AI Health Monitoring System
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    # Secret key for session management (change in production)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///health_monitoring.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # ML Model paths
    MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    HOST = '127.0.0.1'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # In production, bind to specific host, not 0.0.0.0
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
