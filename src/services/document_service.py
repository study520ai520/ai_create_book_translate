import os
from werkzeug.utils import secure_filename
from config.config import Config

class DocumentService:
    def allowed_file(self, filename):
        """检查文件类型是否允许"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    def save_file(self, file):
        """保存上传的文件"""
        filename = secure_filename(file.filename)
        
        # 确保上传目录存在
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    
    def extract_text(self, filepath):
        """从文件中提取文本"""
        # 目前仅支持txt文件，后续可以添加其他格式的支持
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def split_text(self, text, max_length=500):
        """将文本分割成碎片"""
        # 简单按段落分割
        paragraphs = text.split('\n\n')
        fragments = []
        current_fragment = ''
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            if len(current_fragment) + len(paragraph) <= max_length:
                current_fragment += paragraph + '\n\n'
            else:
                if current_fragment:
                    fragments.append(current_fragment.strip())
                current_fragment = paragraph + '\n\n'
        
        if current_fragment:
            fragments.append(current_fragment.strip())
        
        return fragments 