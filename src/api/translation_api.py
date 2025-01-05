from flask import Blueprint, jsonify, current_app
from src.services.translation_service import TranslationService
from src.models.fragment import Fragment
from src.models.settings import OpenAISettings
from src.database import db

translation_api = Blueprint('translation_api', __name__)

def get_translation_service():
    """获取翻译服务实例"""
    if not hasattr(current_app, 'translation_service'):
        current_app.translation_service = TranslationService()
    return current_app.translation_service

@translation_api.route('/translate/<int:fragment_id>', methods=['POST'])
def translate_fragment(fragment_id):
    """翻译文本碎片"""
    try:
        # 检查是否已配置OpenAI设置
        settings = OpenAISettings.query.first()
        if not settings or not settings.api_key:
            return jsonify({'error': '请先在设置中配置OpenAI API密钥'}), 400
            
        fragment = Fragment.query.get_or_404(fragment_id)
        translation_service = get_translation_service()
        fragment.translated_text = translation_service.translate(fragment.original_text)
        db.session.commit()
        return jsonify({'success': True, 'fragment': fragment.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 