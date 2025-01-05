import os
import docx
import PyPDF2
import pdfplumber
import magic

class DocumentProcessor:
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

    def split_text(self, text, max_length=1000):
        """将文本分割成较小的片段"""
        # 首先按段落分割
        paragraphs = text.split('\n')
        fragments = []
        current_fragment = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # 如果当前段落加上现有片段仍然在限制之内
            if len(current_fragment) + len(para) <= max_length:
                current_fragment += (para + "\n")
            else:
                # 如果当前片段不为空，添加到结果中
                if current_fragment:
                    fragments.append(current_fragment.strip())
                current_fragment = para + "\n"
        
        # 添加最后一个片段
        if current_fragment:
            fragments.append(current_fragment.strip())
            
        return fragments 