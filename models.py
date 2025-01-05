from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    total_fragments = db.Column(db.Integer, nullable=False)
    fragments = db.relationship('Fragment', backref='book', lazy=True)

    def get_progress(self):
        translated_count = sum(1 for f in self.fragments if f.translated_text)
        return round(translated_count / self.total_fragments * 100, 2) if self.total_fragments > 0 else 0

class Fragment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    fragment_number = db.Column(db.Integer, nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text) 