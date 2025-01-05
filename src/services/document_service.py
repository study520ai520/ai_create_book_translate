import os
import docx
import PyPDF2
import pdfplumber
import magic
from werkzeug.utils import secure_filename
from config.config import Config

class DocumentService:
    """文档处理服务"""
    
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
        file_type = magic.from_file(filepath, mime=True)
        
        if file_type == 'application/pdf':
            return self._extract_from_pdf(filepath)
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return self._extract_from_docx(filepath)
        elif file_type == 'text/plain':
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

    def split_text(self, text):
        """将文本分割成较小的片段"""
        paragraphs = text.split('\n')
        fragments = []
        current_fragment = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            if len(current_fragment) + len(para) <= Config.MAX_FRAGMENT_LENGTH:
                current_fragment += (para + "\n")
            else:
                if current_fragment:
                    fragments.append(current_fragment.strip())
                current_fragment = para + "\n"
        
        if current_fragment:
            fragments.append(current_fragment.strip())
            
        return fragments 