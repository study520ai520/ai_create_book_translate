from src.database import db

class TranslationLanguage(db.Model):
    """翻译语言模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    is_enabled = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_enabled': self.is_enabled
        }

class TranslationStyle(db.Model):
    """翻译风格模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    is_enabled = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_enabled': self.is_enabled
        }

class PromptTemplate(db.Model):
    """提示词模板模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    template = db.Column(db.Text, nullable=False)
    is_system = db.Column(db.Boolean, default=False)  # 是否为系统预设模板
    is_enabled = db.Column(db.Boolean, default=True)  # 是否启用
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template': self.template,
            'is_enabled': self.is_enabled,
            'is_system': self.is_system
        } 

class OpenAISettings(db.Model):
    """OpenAI设置模型"""
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(200))
    api_base = db.Column(db.String(200))
    model_name = db.Column(db.String(50))
    organization = db.Column(db.String(200))
    api_type = db.Column(db.String(50))
    api_version = db.Column(db.String(50))
    proxy = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'api_key': self.api_key,
            'api_base': self.api_base,
            'model_name': self.model_name,
            'organization': self.organization,
            'api_type': self.api_type,
            'api_version': self.api_version,
            'proxy': self.proxy
        } 