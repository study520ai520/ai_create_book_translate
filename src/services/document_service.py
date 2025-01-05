import os
import re
import docx
import PyPDF2
import pdfplumber
from magic import Magic
from werkzeug.utils import secure_filename
from config.config import Config

class DocumentService:
    """文档处理服务"""
    
    def __init__(self):
        """初始化Magic实例"""
        self.magic = Magic(mime=True)
    
    @staticmethod
    def allowed_file(filename):
        """检查文件类型是否允许"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    def save_file(self, file):
        """保存上传的文件"""
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath

    def extract_text(self, filepath):
        """从不同格式的文档中提取文本"""
        file_type = self.magic.from_file(filepath)
        
        if 'pdf' in file_type.lower():
            return self._extract_from_pdf(filepath)
        elif 'microsoft word' in file_type.lower() or 'openxmlformats-officedocument' in file_type.lower():
            return self._extract_from_docx(filepath)
        elif 'text' in file_type.lower():
            return self._extract_from_txt(filepath)
        else:
            raise ValueError(f'不支持的文件类型: {file_type}')

    def _extract_from_pdf(self, filepath):
        """从PDF文件中提取文本"""
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self, filepath):
        """从DOCX文件中提取文本"""
        doc = docx.Document(filepath)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def _extract_from_txt(self, filepath):
        """从TXT文件中提取文本"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def split_text(self, text, max_tokens=None, must_end_with_period=None, split_by_sentence=None):
        """
        将文本分割成较小的片段
        :param text: 要分割的文本
        :param max_tokens: 每个片段的最大token数
        :param must_end_with_period: 是否必须以句号结尾
        :param split_by_sentence: 是否按句子分割
        """
        # 使用默认配置
        max_tokens = max_tokens or Config.DEFAULT_MAX_TOKENS
        must_end_with_period = must_end_with_period if must_end_with_period is not None else Config.MUST_END_WITH_PERIOD
        split_by_sentence = split_by_sentence if split_by_sentence is not None else Config.SPLIT_BY_SENTENCE

        # 首先按段落分割
        paragraphs = text.split('\n')
        fragments = []
        current_fragment = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 如果按句子分割
            if split_by_sentence:
                sentences = re.split(r'([。！？])', para)
                i = 0
                while i < len(sentences):
                    sentence = sentences[i]
                    # 如果有标点符号，将其加到句子后面
                    if i + 1 < len(sentences) and sentences[i + 1] in '。！？':
                        sentence += sentences[i + 1]
                        i += 2
                    else:
                        i += 1

                    if not sentence.strip():
                        continue

                    # 检查是否需要开始新的片段
                    if len(current_fragment) + len(sentence) > max_tokens:
                        if current_fragment:
                            # 如果当前片段不为空且需要以句号结尾
                            if must_end_with_period and not current_fragment.strip().endswith(('。', '！', '？')):
                                current_fragment += '。'
                            fragments.append(current_fragment.strip())
                        current_fragment = sentence
                    else:
                        current_fragment += sentence
            else:
                # 如果当前段落加上现有片段超过限制
                if len(current_fragment) + len(para) > max_tokens:
                    if current_fragment:
                        # 如果当前片段不为空且需要以句号结尾
                        if must_end_with_period and not current_fragment.strip().endswith(('。', '！', '？')):
                            current_fragment += '。'
                        fragments.append(current_fragment.strip())
                    current_fragment = para
                else:
                    current_fragment += (para + "\n")

        # 添加最后一个片段
        if current_fragment:
            # 对于最后一个片段，我们不强制要求以句号结尾
            fragments.append(current_fragment.strip())

        return fragments 