from src.database.db import db

class Book(db.Model):
    """书籍模型"""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    total_fragments = db.Column(db.Integer, nullable=False)
    fragments = db.relationship('Fragment', backref='book', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())

    def get_progress(self):
        """计算翻译进度"""
        translated_count = sum(1 for f in self.fragments if f.translated_text)
        return round(translated_count / self.total_fragments * 100, 2) if self.total_fragments > 0 else 0

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'total_fragments': self.total_fragments,
            'progress': self.get_progress(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 