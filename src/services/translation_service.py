from openai import OpenAI
from config.config import Config
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class TranslationService:
    """翻译服务"""
    
    # 默认翻译配置
    DEFAULT_TARGET_LANG = '中文'
    DEFAULT_TRANSLATION_STYLE = '准确、流畅'
    
    # 翻译模板
    TEMPLATES = {
        'standard': '''
你是一个专业的翻译专家。请将以下文本翻译成{target_lang}。

翻译要求：
1. 保持原文的语气和风格
2. 确保翻译准确、自然、流畅
3. 保留原文的专业术语和特定表述
4. 适应目标语言的表达习惯
5. 注意上下文的连贯性

原文内容：
{text}

翻译风格：{style}

请直接输出译文，不要包含任何解释或说明。
''',
        'literary': '''
你是一位资深的文学翻译家。请将以下文本翻译成{target_lang}。

翻译要求：
1. 注重文学性和艺术性表达
2. 保持原文的意境和情感
3. 使用优美、富有诗意的语言
4. 适当运用修辞手法
5. 确保译文优雅流畅

原文内容：
{text}

翻译风格：{style}

请直接输出译文，不要包含任何解释或说明。
''',
        'technical': '''
你是一位专业的技术文档翻译专家。请将以下文本翻译成{target_lang}。

翻译要求：
1. 严格准确的术语翻译
2. 保持专业性和严谨性
3. 使用规范的技术文档语言
4. 确保逻辑清晰
5. 保持格式统一

原文内容：
{text}

翻译风格：{style}

请直接输出译文，不要包含任何解释或说明。
''',
        'casual': '''
你是一位口语翻译专家。请将以下文本翻译成{target_lang}。

翻译要求：
1. 使用自然的口语表达
2. 保持对话的轻松感
3. 适当使用俚语和习语
4. 注重表达的生动性
5. 符合日常交际习惯

原文内容：
{text}

翻译风格：{style}

请直接输出译文，不要包含任何解释或说明。
''',
        'academic': '''
你是一位学术论文翻译专家。请将以下文本翻译成{target_lang}。

翻译要求：
1. 严格遵守学术写作规范
2. 准确传达学术概念
3. 使用规范的学术用语
4. 保持客观严谨的语气
5. 注重专业术语的统一性

原文内容：
{text}

翻译风格：{style}

请直接输出译文，不要包含任何解释或说明。
'''
    }
    
    def __init__(self):
        """初始化OpenAI客户端"""
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_API_BASE or None,
            organization=Config.OPENAI_ORGANIZATION or None,
            timeout=Config.TIMEOUT
        )
        self.model = Config.OPENAI_MODEL
        logging.info(f"翻译服务初始化完成，使用模型：{self.model}")

    def translate(self, text, target_lang='中文', style='准确、流畅', custom_prompt=None):
        """翻译文本
        这里是一个模拟的翻译服务，实际应用中需要替换为真实的翻译API调用
        """
        # 模拟翻译结果
        if target_lang == '中文':
            return f"这是一段模拟的{style}翻译：\n{text}"
        else:
            return f"This is a simulated {style} translation:\n{text}"

    def translate_batch(self, texts, target_lang=None, style=None, custom_prompt=None):
        """
        批量翻译文本
        :param texts: 要翻译的文本列表
        :param target_lang: 目标语言
        :param style: 翻译风格
        :param custom_prompt: 自定义提示词
        :return: 翻译后的文本列表
        """
        total_texts = len(texts)
        logging.info(f"开始批量翻译，共 {total_texts} 个文本")
        start_time = time.time()
        
        translated_texts = []
        success_count = 0
        error_count = 0
        
        for i, text in enumerate(texts, 1):
            try:
                logging.info(f"翻译进度: {i}/{total_texts} ({round(i/total_texts*100, 1)}%)")
                translated_text = self.translate(text, target_lang, style, custom_prompt)
                translated_texts.append(translated_text)
                success_count += 1
                
            except Exception as e:
                logging.error(f"第 {i} 个文本翻译失败: {str(e)}")
                translated_texts.append(text)  # 出错时保留原文
                error_count += 1
        
        # 计算总耗时和统计信息
        end_time = time.time()
        total_duration = round(end_time - start_time, 2)
        avg_duration = round(total_duration / total_texts, 2)
        
        logging.info(f"批量翻译完成:")
        logging.info(f"- 总耗时: {total_duration}秒")
        logging.info(f"- 平均每个文本耗时: {avg_duration}秒")
        logging.info(f"- 成功: {success_count}")
        logging.info(f"- 失败: {error_count}")
        
        return translated_texts 