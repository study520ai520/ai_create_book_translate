from src.database import db

class Fragment(db.Model):
    """文本碎片模型"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    fragment_number = db.Column(db.Integer, nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'number': self.fragment_number,
            'original_text': self.original_text,
            'translated_text': self.translated_text
        } 