from flask import Blueprint, request, jsonify
from src.database import db
from src.models.settings import TranslationLanguage, TranslationStyle, PromptTemplate

settings_api = Blueprint('settings_api', __name__)

# 语言设置API
@settings_api.route('/languages', methods=['GET'])
def get_languages():
    """获取所有翻译语言"""
    languages = TranslationLanguage.query.all()
    return jsonify([lang.to_dict() for lang in languages])

@settings_api.route('/languages', methods=['POST'])
def add_language():
    """添加翻译语言"""
    data = request.json
    try:
        language = TranslationLanguage(
            name=data['name'],
            description=data.get('description', ''),
            is_enabled=data.get('is_enabled', True)
        )
        db.session.add(language)
        db.session.commit()
        return jsonify({'success': True, 'data': language.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@settings_api.route('/languages/<int:id>', methods=['PUT'])
def update_language(id):
    """更新翻译语言"""
    language = TranslationLanguage.query.get_or_404(id)
    data = request.json
    try:
        language.name = data.get('name', language.name)
        language.description = data.get('description', language.description)
        language.is_enabled = data.get('is_enabled', language.is_enabled)
        db.session.commit()
        return jsonify({'success': True, 'data': language.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@settings_api.route('/languages/<int:id>', methods=['DELETE'])
def delete_language(id):
    """删除翻译语言"""
    language = TranslationLanguage.query.get_or_404(id)
    try:
        db.session.delete(language)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# 翻译风格API
@settings_api.route('/styles', methods=['GET'])
def get_styles():
    """获取所有翻译风格"""
    styles = TranslationStyle.query.all()
    return jsonify([style.to_dict() for style in styles])

@settings_api.route('/styles', methods=['POST'])
def add_style():
    """添加翻译风格"""
    data = request.json
    try:
        style = TranslationStyle(
            name=data['name'],
            description=data.get('description', ''),
            is_enabled=data.get('is_enabled', True)
        )
        db.session.add(style)
        db.session.commit()
        return jsonify({'success': True, 'data': style.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@settings_api.route('/styles/<int:id>', methods=['PUT'])
def update_style(id):
    """更新翻译风格"""
    style = TranslationStyle.query.get_or_404(id)
    data = request.json
    try:
        style.name = data.get('name', style.name)
        style.description = data.get('description', style.description)
        style.is_enabled = data.get('is_enabled', style.is_enabled)
        db.session.commit()
        return jsonify({'success': True, 'data': style.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@settings_api.route('/styles/<int:id>', methods=['DELETE'])
def delete_style(id):
    """删除翻译风格"""
    style = TranslationStyle.query.get_or_404(id)
    try:
        db.session.delete(style)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# 提示词模板API
@settings_api.route('/templates', methods=['GET'])
def get_templates():
    """获取所有提示词模板"""
    templates = PromptTemplate.query.all()
    return jsonify([template.to_dict() for template in templates])

@settings_api.route('/templates', methods=['POST'])
def add_template():
    """添加提示词模板"""
    data = request.json
    try:
        template = PromptTemplate(
            name=data['name'],
            description=data.get('description', ''),
            template=data['template'],
            is_enabled=data.get('is_enabled', True),
            is_system=data.get('is_system', False)
        )
        db.session.add(template)
        db.session.commit()
        return jsonify({'success': True, 'data': template.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@settings_api.route('/templates/<int:id>', methods=['PUT'])
def update_template(id):
    """更新提示词模板"""
    template = PromptTemplate.query.get_or_404(id)
    data = request.json
    try:
        if template.is_system and not request.json.get('is_system', True):
            return jsonify({'success': False, 'error': '系统预设模板不能修改为用户模板'}), 400
        
        template.name = data.get('name', template.name)
        template.description = data.get('description', template.description)
        template.template = data.get('template', template.template)
        template.is_enabled = data.get('is_enabled', template.is_enabled)
        db.session.commit()
        return jsonify({'success': True, 'data': template.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@settings_api.route('/templates/<int:id>', methods=['DELETE'])
def delete_template(id):
    """删除提示词模板"""
    template = PromptTemplate.query.get_or_404(id)
    try:
        if template.is_system:
            return jsonify({'success': False, 'error': '系统预设模板不能删除'}), 400
        db.session.delete(template)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400 