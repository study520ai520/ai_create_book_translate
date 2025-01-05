from src.database import db

class Book(db.Model):
    """书籍模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    total_fragments = db.Column(db.Integer, default=0)
    progress = db.Column(db.Integer, default=0)  # 翻译进度（百分比）
    
    # 翻译设置
    target_language = db.Column(db.String(50))
    translation_style = db.Column(db.String(50))
    prompt_template = db.Column(db.String(50))
    custom_prompt = db.Column(db.Text)
    
    # 关联的碎片
    fragments = db.relationship('Fragment', backref='book', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'total_fragments': self.total_fragments,
            'progress': self.progress,
            'has_translation_settings': bool(self.target_language and self.translation_style and self.prompt_template),
            'target_language': self.target_language,
            'translation_style': self.translation_style,
            'prompt_template': self.prompt_template,
            'custom_prompt': self.custom_prompt
        }

class Fragment(db.Model):
    """文本碎片模型"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    fragment_number = db.Column(db.Integer, nullable=False)  # 碎片序号
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'number': self.fragment_number,
            'original_text': self.original_text,
            'translated_text': self.translated_text
        } 