import os

class Config:
    # 基础配置
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MB

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'translate_book.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文本处理配置
    MAX_FRAGMENT_LENGTH = 1000  # 每个文本碎片的最大长度

    # 支持的文件类型
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

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