from src.database import db

class Book(db.Model):
    """书籍模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    total_fragments = db.Column(db.Integer, default=0)
    progress = db.Column(db.Integer, default=0)
    
    # 添加翻译设置字段
    target_language = db.Column(db.String(50), default='中文')
    translation_style = db.Column(db.String(50), default='准确、流畅')
    prompt_template = db.Column(db.String(50), default='standard')
    custom_prompt = db.Column(db.Text)
    
    fragments = db.relationship('Fragment', backref='book', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'total_fragments': self.total_fragments,
            'progress': self.progress,
            'target_language': self.target_language,
            'translation_style': self.translation_style,
            'prompt_template': self.prompt_template,
            'custom_prompt': self.custom_prompt,
            'has_translation_settings': bool(self.target_language and self.translation_style and self.prompt_template)
        } 