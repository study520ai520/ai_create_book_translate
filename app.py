from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from models import db, Book, Fragment
from document_processor import DocumentProcessor
from translator import Translator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translate_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化数据库
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # 处理文档
    processor = DocumentProcessor()
    text = processor.extract_text(filepath)
    fragments = processor.split_text(text)
    
    # 保存到数据库
    book = Book(name=filename, total_fragments=len(fragments))
    db.session.add(book)
    db.session.commit()
    
    for idx, content in enumerate(fragments):
        fragment = Fragment(
            book_id=book.id,
            fragment_number=idx + 1,
            original_text=content,
            translated_text=""
        )
        db.session.add(fragment)
    
    db.session.commit()
    return jsonify({'success': True, 'book_id': book.id})

@app.route('/books')
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'name': book.name,
        'progress': book.get_progress()
    } for book in books])

@app.route('/book/<int:book_id>/fragments')
def get_fragments(book_id):
    fragments = Fragment.query.filter_by(book_id=book_id).all()
    return jsonify([{
        'id': f.id,
        'number': f.fragment_number,
        'original_text': f.original_text,
        'translated_text': f.translated_text
    } for f in fragments])

@app.route('/translate/<int:fragment_id>', methods=['POST'])
def translate_fragment(fragment_id):
    fragment = Fragment.query.get_or_404(fragment_id)
    translator = Translator()
    fragment.translated_text = translator.translate(fragment.original_text)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 