from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import logging
from src.models.book import Book, Fragment
from src.models.settings import OpenAISettings
from src.services.document_service import DocumentService
from src.services.translation_service import TranslationService
from src.database import db

book_api = Blueprint('book_api', __name__)
document_service = DocumentService()

def get_translation_service():
    """获取翻译服务实例"""
    if not hasattr(current_app, 'translation_service'):
        current_app.translation_service = TranslationService()
    return current_app.translation_service

@book_api.route('/books', methods=['GET'])
def get_books():
    """获取所有书籍"""
    try:
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books])
    except Exception as e:
        logging.error(f"获取书籍列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@book_api.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """获取单本书籍"""
    try:
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict())
    except Exception as e:
        logging.error(f"获取书籍失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@book_api.route('/books', methods=['POST'])
def upload_book():
    """上传新书籍"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件被上传'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
            
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 创建书籍记录
            book = Book(
                title=os.path.splitext(filename)[0],
                file_path=file_path,
                original_filename=filename
            )
            db.session.add(book)
            db.session.commit()
            
            # 处理文档
            fragments = document_service.process_document(file_path)
            
            # 保存文本片段
            for text in fragments:
                fragment = Fragment(
                    book_id=book.id,
                    original_text=text
                )
                db.session.add(fragment)
            
            db.session.commit()
            
            return jsonify(book.to_dict()), 201
            
    except Exception as e:
        logging.error(f"上传书籍失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@book_api.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """删除书籍"""
    try:
        book = Book.query.get_or_404(book_id)
        
        # 删除关联的文件
        if book.file_path and os.path.exists(book.file_path):
            os.remove(book.file_path)
            
        # 删除数据库记录
        db.session.delete(book)
        db.session.commit()
        
        return '', 204
    except Exception as e:
        logging.error(f"删除书籍失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@book_api.route('/books/<int:book_id>/translate', methods=['POST'])
def translate_book(book_id):
    """翻译书籍"""
    try:
        book = Book.query.get_or_404(book_id)
        
        # 检查是否已配置OpenAI设置
        settings = OpenAISettings.query.first()
        if not settings or not settings.api_key:
            return jsonify({'error': '请先在设置中配置OpenAI API密钥'}), 400
        
        # 获取翻译服务实例
        translation_service = get_translation_service()
        
        # 获取未翻译的片段
        fragments = Fragment.query.filter_by(book_id=book_id, translated_text=None).all()
        
        # 更新书籍状态
        book.status = 'translating'
        db.session.commit()
        
        # 翻译每个片段
        total_fragments = len(fragments)
        translated_count = 0
        
        for fragment in fragments:
            try:
                fragment.translated_text = translation_service.translate(
                    fragment.original_text,
                    target_lang=book.target_language,
                    style=book.translation_style,
                    custom_prompt=book.prompt_template
                )
                translated_count += 1
                # 更新进度
                book.progress = (translated_count / total_fragments) * 100
                db.session.commit()
                
            except Exception as e:
                logging.error(f"翻译片段失败: {str(e)}")
                book.status = 'error'
                book.error_message = str(e)
                db.session.commit()
                return jsonify({'error': str(e)}), 500
        
        # 更新书籍状态
        book.status = 'completed'
        book.progress = 100
        db.session.commit()
        
        return jsonify(book.to_dict())
        
    except Exception as e:
        logging.error(f"翻译书籍失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@book_api.route('/books/<int:book_id>/settings', methods=['POST'])
def save_book_settings(book_id):
    """保存书籍翻译设置"""
    try:
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        
        # 更新设置
        book.target_language = data.get('target_language', book.target_language)
        book.translation_style = data.get('translation_style', book.translation_style)
        book.prompt_template = data.get('prompt_template', book.prompt_template)
        
        db.session.commit()
        return jsonify(book.to_dict())
        
    except Exception as e:
        logging.error(f"保存书籍设置失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@book_api.route('/books/<int:book_id>/export', methods=['GET'])
def export_book(book_id):
    """导出书籍"""
    try:
        book = Book.query.get_or_404(book_id)
        fragments = Fragment.query.filter_by(book_id=book_id).order_by(Fragment.id).all()
        
        # 生成导出内容
        content = []
        for fragment in fragments:
            content.append("原文：")
            content.append(fragment.original_text)
            content.append("\n译文：")
            content.append(fragment.translated_text or "（未翻译）")
            content.append("\n" + "="*50 + "\n")
        
        # 创建导出文件
        export_filename = f"{book.title}_translated.txt"
        export_path = os.path.join(current_app.config['UPLOAD_FOLDER'], export_filename)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return jsonify({
            'success': True,
            'file_path': export_path,
            'filename': export_filename
        })
        
    except Exception as e:
        logging.error(f"导出书籍失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 