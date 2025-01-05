from flask import Flask
from src.database import db
from src.models import Book, Fragment
from config.config import config

def init_database():
    """初始化数据库"""
    app = Flask(__name__)
    app.config.from_object(config['default'])
    
    db.init_app(app)
    
    with app.app_context():
        # 删除所有表
        db.drop_all()
        # 创建所有表
        db.create_all()
        
        print("数据库初始化完成！")

if __name__ == '__main__':
    init_database() 