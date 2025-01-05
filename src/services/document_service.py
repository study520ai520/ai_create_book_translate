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
    
    def split_text(self, text):
        """
        将文本分割成碎片
        使用配置的碎片大小、最小大小和重叠大小进行智能分割
        """
        # 获取配置值
        max_length = Config.FRAGMENT_SIZE
        min_length = Config.FRAGMENT_MIN_SIZE
        overlap = Config.FRAGMENT_OVERLAP
        
        # 按段落分割
        paragraphs = text.split('\n\n')
        fragments = []
        current_fragment = ''
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # 如果段落本身超过最大长度，需要进行分割
            if len(paragraph) > max_length:
                words = paragraph.split()
                current_part = ''
                
                for word in words:
                    if len(current_part) + len(word) + 1 <= max_length:
                        current_part += (word + ' ')
                    else:
                        # 确保当前部分达到最小长度
                        if len(current_part) >= min_length:
                            fragments.append(current_part.strip())
                            # 保留一部分内容作为重叠
                            current_part = current_part[-overlap:] if overlap > 0 else ''
                        current_part += (word + ' ')
                
                if current_part and len(current_part) >= min_length:
                    fragments.append(current_part.strip())
                continue
            
            # 处理正常大小的段落
            if len(current_fragment) + len(paragraph) + 2 <= max_length:
                current_fragment += paragraph + '\n\n'
            else:
                # 确保当前碎片达到最小长度
                if current_fragment and len(current_fragment) >= min_length:
                    fragments.append(current_fragment.strip())
                current_fragment = paragraph + '\n\n'
        
        # 添加最后一个碎片
        if current_fragment and len(current_fragment) >= min_length:
            fragments.append(current_fragment.strip())
        
        return fragments 