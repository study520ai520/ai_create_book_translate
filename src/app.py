from flask import Flask, render_template
from src.database import db
from src.api.book_api import book_api
from src.api.settings_api import settings_api
from config.config import config
import os

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src/templates'),
                static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src/static'))
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(book_api, url_prefix='/api')
    app.register_blueprint(settings_api, url_prefix='/api')
    
    # 添加主页路由
    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context():
        db.create_all()
        
        # 导入模型
        from src.models.settings import TranslationLanguage, TranslationStyle, PromptTemplate
        
        # 初始化默认语言
        if not TranslationLanguage.query.first():
            languages = [
                {
                    'name': '中文',
                    'description': '简体中文',
                    'is_enabled': True
                },
                {
                    'name': '英文',
                    'description': '英语',
                    'is_enabled': True
                },
                {
                    'name': '日文',
                    'description': '日语',
                    'is_enabled': True
                },
                {
                    'name': '韩文',
                    'description': '韩语',
                    'is_enabled': True
                },
                {
                    'name': '法文',
                    'description': '法语',
                    'is_enabled': True
                },
                {
                    'name': '德文',
                    'description': '德语',
                    'is_enabled': True
                },
                {
                    'name': '俄文',
                    'description': '俄语',
                    'is_enabled': True
                },
                {
                    'name': '西班牙文',
                    'description': '西班牙语',
                    'is_enabled': True
                },
                {
                    'name': '意大利文',
                    'description': '意大利语',
                    'is_enabled': True
                },
                {
                    'name': '葡萄牙文',
                    'description': '葡萄牙语',
                    'is_enabled': True
                }
            ]
            
            for lang_data in languages:
                language = TranslationLanguage(**lang_data)
                db.session.add(language)
            
            db.session.commit()
        
        # 初始化默认翻译风格
        if not TranslationStyle.query.first():
            styles = [
                {
                    'name': '准确翻译',
                    'description': '直译为主，追求准确性和忠实原文',
                    'is_enabled': True
                },
                {
                    'name': '意译优化',
                    'description': '在保持原意的基础上优化表达，使译文更加流畅自然',
                    'is_enabled': True
                },
                {
                    'name': '文学风格',
                    'description': '注重文学性和优美度，适合文学作品翻译',
                    'is_enabled': True
                },
                {
                    'name': '口语化',
                    'description': '采用日常口语表达，让译文更接地气',
                    'is_enabled': True
                },
                {
                    'name': '专业术语',
                    'description': '保持专业术语的准确性，适合技术文档翻译',
                    'is_enabled': True
                },
                {
                    'name': '简明扼要',
                    'description': '精简译文，突出重点，适合摘要和总结',
                    'is_enabled': True
                },
                {
                    'name': '学术风格',
                    'description': '严谨的学术风格，适合学术论文翻译',
                    'is_enabled': True
                }
            ]
            
            for style_data in styles:
                style = TranslationStyle(**style_data)
                db.session.add(style)
            
            db.session.commit()
        
        # 初始化系统预设模板
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
                },
                {
                    'name': '口语对话模板',
                    'description': '适合日常对话的翻译',
                    'template': '请将以下文本翻译成{target_language}的日常口语表达，保持{translation_style}的风格，使译文自然流畅：\n\n{text}',
                    'is_system': True
                },
                {
                    'name': '学术论文模板',
                    'description': '适合学术论文的翻译',
                    'template': '请将以下学术文本翻译成{target_language}，使用学术规范的表达方式，保持{translation_style}的风格，确保专业术语的准确性：\n\n{text}',
                    'is_system': True
                },
                {
                    'name': '新闻报道模板',
                    'description': '适合新闻文章的翻译',
                    'template': '请将以下新闻文本翻译成{target_language}，采用新闻报道的语气，保持{translation_style}的风格，确保信息准确客观：\n\n{text}',
                    'is_system': True
                },
                {
                    'name': '简明总结模板',
                    'description': '适合需要简明扼要翻译的场景',
                    'template': '请将以下文本翻译成{target_language}，采用简明扼要的方式，保持{translation_style}的风格，突出重点信息：\n\n{text}',
                    'is_system': True
                }
            ]
            
            for template_data in templates:
                template = PromptTemplate(**template_data)
                db.session.add(template)
            
            db.session.commit()
    
    return app 