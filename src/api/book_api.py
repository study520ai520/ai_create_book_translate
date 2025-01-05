from flask import Blueprint, request, jsonify
from src.services import DocumentService
from src.models import Book, Fragment
from src.database import db

book_api = Blueprint('book_api', __name__)
document_service = DocumentService()

@book_api.route('/books', methods=['GET'])
def get_books():
    """获取所有书籍"""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@book_api.route('/upload', methods=['POST'])
def upload_file():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if not document_service.allowed_file(file.filename):
        return jsonify({'error': '不支持的文件类型'}), 400

    try:
        # 保存文件
        filepath = document_service.save_file(file)
        
        # 处理文档
        text = document_service.extract_text(filepath)
        fragments = document_service.split_text(text)
        
        # 保存到数据库
        book = Book(name=file.filename, total_fragments=len(fragments))
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
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_api.route('/book/<int:book_id>/fragments', methods=['GET'])
def get_fragments(book_id):
    """获取书籍的所有文本碎片"""
    fragments = Fragment.query.filter_by(book_id=book_id).all()
    return jsonify([fragment.to_dict() for fragment in fragments]) 