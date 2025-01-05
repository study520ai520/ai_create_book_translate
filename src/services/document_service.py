import os
from werkzeug.utils import secure_filename
from config.config import Config
import re

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
        将文本按句号分割成碎片
        :param text: 要分割的文本
        :return: 分割后的文本碎片列表
        """
        # 获取配置的最大长度
        max_length = Config.FRAGMENT_SIZE
        
        # 预处理文本：删除多余的空白字符
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 使用正则表达式按句号切分，保留句号
        # 匹配中文句号和英文句号，但不包括小数点
        sentences = re.split(r'([。.](?!\d))', text)
        
        # 合并句子和句号
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        sentences = [s for s in sentences if s.strip()]  # 移除空字符串
        
        fragments = []
        current_fragment = ''
        
        for sentence in sentences:
            # 如果当前句子本身就超过最大长度，直接作为一个片段
            if len(sentence) > max_length:
                if current_fragment:
                    fragments.append(current_fragment.strip())
                fragments.append(sentence.strip())
                current_fragment = ''
                continue
            
            # 如果添加当前句子后会超过最大长度
            if len(current_fragment) + len(sentence) > max_length and current_fragment:
                fragments.append(current_fragment.strip())
                current_fragment = sentence
            else:
                current_fragment += sentence
        
        # 添加最后一个片段（可能不以句号结尾）
        if current_fragment:
            fragments.append(current_fragment.strip())
        
        return fragments 