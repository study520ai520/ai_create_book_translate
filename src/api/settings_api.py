from flask import Blueprint, jsonify, request
from src.database import db
from src.models.settings import TranslationLanguage, TranslationStyle, PromptTemplate

settings_api = Blueprint('settings_api', __name__)

# 语言管理接口
@settings_api.route('/languages', methods=['GET'])
def get_languages():
    """获取所有翻译语言"""
    languages = TranslationLanguage.query.all()
    return jsonify([lang.to_dict() for lang in languages])

@settings_api.route('/languages/<int:id>', methods=['GET'])
def get_language(id):
    """获取单个翻译语言"""
    language = TranslationLanguage.query.get_or_404(id)
    return jsonify(language.to_dict())

@settings_api.route('/languages', methods=['POST'])
def add_language():
    """添加新的翻译语言"""
    data = request.get_json()
    language = TranslationLanguage(
        name=data['name'],
        description=data.get('description', ''),
        is_enabled=data.get('is_enabled', True)
    )
    db.session.add(language)
    db.session.commit()
    return jsonify(language.to_dict()), 201

@settings_api.route('/languages/<int:id>', methods=['PUT'])
def update_language(id):
    """更新翻译语言"""
    language = TranslationLanguage.query.get_or_404(id)
    data = request.get_json()
    language.name = data.get('name', language.name)
    language.description = data.get('description', language.description)
    language.is_enabled = data.get('is_enabled', language.is_enabled)
    db.session.commit()
    return jsonify(language.to_dict())

@settings_api.route('/languages/<int:id>', methods=['DELETE'])
def delete_language(id):
    """删除翻译语言"""
    language = TranslationLanguage.query.get_or_404(id)
    db.session.delete(language)
    db.session.commit()
    return '', 204

# 翻译风格接口
@settings_api.route('/styles', methods=['GET'])
def get_styles():
    """获取所有翻译风格"""
    styles = TranslationStyle.query.all()
    return jsonify([style.to_dict() for style in styles])

@settings_api.route('/styles/<int:id>', methods=['GET'])
def get_style(id):
    """获取单个翻译风格"""
    style = TranslationStyle.query.get_or_404(id)
    return jsonify(style.to_dict())

@settings_api.route('/styles', methods=['POST'])
def add_style():
    """添加新的翻译风格"""
    data = request.get_json()
    style = TranslationStyle(
        name=data['name'],
        description=data.get('description', ''),
        is_enabled=data.get('is_enabled', True)
    )
    db.session.add(style)
    db.session.commit()
    return jsonify(style.to_dict()), 201

@settings_api.route('/styles/<int:id>', methods=['PUT'])
def update_style(id):
    """更新翻译风格"""
    style = TranslationStyle.query.get_or_404(id)
    data = request.get_json()
    style.name = data.get('name', style.name)
    style.description = data.get('description', style.description)
    style.is_enabled = data.get('is_enabled', style.is_enabled)
    db.session.commit()
    return jsonify(style.to_dict())

@settings_api.route('/styles/<int:id>', methods=['DELETE'])
def delete_style(id):
    """删除翻译风格"""
    style = TranslationStyle.query.get_or_404(id)
    db.session.delete(style)
    db.session.commit()
    return '', 204

# 提示词模板接口
@settings_api.route('/templates', methods=['GET'])
def get_templates():
    """获取所有提示词模板"""
    templates = PromptTemplate.query.all()
    return jsonify([template.to_dict() for template in templates])

@settings_api.route('/templates/<int:id>', methods=['GET'])
def get_template(id):
    """获取单个提示词模板"""
    template = PromptTemplate.query.get_or_404(id)
    return jsonify(template.to_dict())

@settings_api.route('/templates', methods=['POST'])
def add_template():
    """添加新的提示词模板"""
    data = request.get_json()
    template = PromptTemplate(
        name=data['name'],
        description=data.get('description', ''),
        template=data['template'],
        is_system=data.get('is_system', False),
        is_enabled=data.get('is_enabled', True)
    )
    db.session.add(template)
    db.session.commit()
    return jsonify(template.to_dict()), 201

@settings_api.route('/templates/<int:id>', methods=['PUT'])
def update_template(id):
    """更新提示词模板"""
    template = PromptTemplate.query.get_or_404(id)
    data = request.get_json()
    
    # 系统预设模板只允许修改 is_enabled
    if template.is_system:
        template.is_enabled = data.get('is_enabled', template.is_enabled)
    else:
        template.name = data.get('name', template.name)
        template.description = data.get('description', template.description)
        template.template = data.get('template', template.template)
        template.is_enabled = data.get('is_enabled', template.is_enabled)
    
    db.session.commit()
    return jsonify(template.to_dict())

@settings_api.route('/templates/<int:id>', methods=['DELETE'])
def delete_template(id):
    """删除提示词模板"""
    template = PromptTemplate.query.get_or_404(id)
    # 不允许删除系统预设模板
    if template.is_system:
        return jsonify({'error': '系统预设模板不允许删除'}), 403
    db.session.delete(template)
    db.session.commit()
    return '', 204 