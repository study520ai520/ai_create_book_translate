import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基础配置
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # 基础路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', '')
    OPENAI_API_TYPE = os.getenv('OPENAI_API_TYPE', 'open_ai')
    OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION', '')
    OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION', '')
    OPENAI_PROXY = os.getenv('OPENAI_PROXY', '')
    
    # 翻译配置
    TIMEOUT = 60  # API调用超时时间（秒）
    TEMPERATURE = 0.7  # 生成文本的随机性
    MAX_TOKENS_PER_REQUEST = 1500  # 每次请求的最大token数

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 