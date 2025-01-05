from flask import Flask, render_template
from src.api import book_api
from src.database import init_db
from config.config import Config
import os

def create_app():
    """创建Flask应用"""
    app = Flask(__name__, 
                template_folder='src/templates',
                static_folder='src/static')
    
    # 配置应用
    app.config.from_object(Config)
    
    # 确保上传目录存在
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    # 初始化数据库
    init_db(app)
    
    # 注册蓝图
    app.register_blueprint(book_api)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 