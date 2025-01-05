import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基础配置
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MB

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'translate_book.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文本处理配置
    DEFAULT_MAX_TOKENS = 500  # 默认每个碎片的最大token数
    MIN_TOKENS = 100  # 最小token数
    MAX_TOKENS = 2000  # 最大token数
    MUST_END_WITH_PERIOD = True  # 是否必须以句号结尾
    SPLIT_BY_SENTENCE = True  # 是否按句子分割

    # 支持的文件类型
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 