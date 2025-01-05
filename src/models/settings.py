from src.database import db

class TranslationLanguage(db.Model):
    """翻译语言设置"""
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
    """翻译风格设置"""
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
    """提示词模板设置"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    template = db.Column(db.Text, nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)
    is_system = db.Column(db.Boolean, default=False)  # 是否是系统预设模板
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template': self.template,
            'is_enabled': self.is_enabled,
            'is_system': self.is_system
        } 