from flask import Blueprint, jsonify
from src.services import TranslationService
from src.models import Fragment
from src.database import db

translation_api = Blueprint('translation_api', __name__)
translation_service = TranslationService()

@translation_api.route('/translate/<int:fragment_id>', methods=['POST'])
def translate_fragment(fragment_id):
    """翻译文本碎片"""
    try:
        fragment = Fragment.query.get_or_404(fragment_id)
        fragment.translated_text = translation_service.translate(fragment.original_text)
        db.session.commit()
        return jsonify({'success': True, 'fragment': fragment.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 