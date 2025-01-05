from flask import Blueprint, request, jsonify
from src.services import DocumentService, TranslationService
from src.models import Book, Fragment
from src.database import db
import os

book_api = Blueprint('book_api', __name__)
document_service = DocumentService()
translation_service = TranslationService()

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

@book_api.route('/translate_remaining/<int:book_id>', methods=['POST'])
def translate_remaining(book_id):
    """翻译书籍中所有未翻译的碎片"""
    try:
        fragments = Fragment.query.filter_by(book_id=book_id, translated_text=None).all()
        for fragment in fragments:
            fragment.translated_text = translation_service.translate(fragment.original_text)
            db.session.add(fragment)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_api.route('/retranslate/<int:book_id>', methods=['POST'])
def retranslate_book(book_id):
    """重新翻译整本书"""
    try:
        book = Book.query.get_or_404(book_id)
        
        # 删除所有现有碎片
        Fragment.query.filter_by(book_id=book_id).delete()
        
        # 重新处理文档
        filepath = os.path.join(Config.UPLOAD_FOLDER, book.name)
        if not os.path.exists(filepath):
            return jsonify({'error': '原文件不存在'}), 404
            
        text = document_service.extract_text(filepath)
        fragments = document_service.split_text(text)
        
        # 更新总碎片数
        book.total_fragments = len(fragments)
        
        # 创建新碎片并翻译
        for idx, content in enumerate(fragments):
            fragment = Fragment(
                book_id=book.id,
                fragment_number=idx + 1,
                original_text=content,
                translated_text=translation_service.translate(content)
            )
            db.session.add(fragment)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 