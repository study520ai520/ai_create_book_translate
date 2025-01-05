from flask import Flask
from src.database import db
from src.api.book_api import book_api
from src.api.settings_api import settings_api
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(book_api, url_prefix='/')
    app.register_blueprint(settings_api, url_prefix='/')
    
    with app.app_context():
        db.create_all()
        
        # 初始化系统预设模板
        from src.models.settings import PromptTemplate
        if not PromptTemplate.query.filter_by(is_system=True).first():
            templates = [
                {
                    'name': '标准模板',
                    'description': '通用翻译模板，适合大多数场景',
                    'template': '请将以下文本翻译成{target_language}，保持{translation_style}的风格：\n\n{text}',
                    'is_system': True
                },
                {
                    'name': '文学翻译模板',
                    'description': '适合文学作品的翻译',
                    'template': '请以文学翻译的方式将以下文本翻译成{target_language}，注重文学性和优美度，保持{translation_style}的风格：\n\n{text}',
                    'is_system': True
                },
                {
                    'name': '技术文档模板',
                    'description': '适合技术文档的翻译',
                    'template': '请以技术文档的专业方式将以下文本翻译成{target_language}，保持专业术语的准确性，遵循{translation_style}的风格：\n\n{text}',
                    'is_system': True
                }
            ]
            
            for template_data in templates:
                template = PromptTemplate(**template_data)
                db.session.add(template)
            
            db.session.commit()
    
    return app 