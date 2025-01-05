import os
from flask import Flask
from config.config import config
from src.database import init_db
from src.api import main_api, book_api, translation_api

def create_app(config_name='default'):
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化数据库
    init_db(app)
    
    # 注册蓝图
    app.register_blueprint(main_api)
    app.register_blueprint(book_api)
    app.register_blueprint(translation_api)
    
    return app 