from src.database.db import db

class Fragment(db.Model):
    """文本碎片模型"""
    __tablename__ = 'fragments'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    fragment_number = db.Column(db.Integer, nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'number': self.fragment_number,
            'original_text': self.original_text,
            'translated_text': self.translated_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 