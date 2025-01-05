from openai import OpenAI
from config.config import Config

class TranslationService:
    """翻译服务"""
    
    # 默认翻译配置
    DEFAULT_TARGET_LANG = '中文'
    DEFAULT_TRANSLATION_STYLE = '准确、流畅'
    DEFAULT_TRANSLATION_PROMPT = '''
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
'''
    
    def __init__(self):
        """初始化OpenAI客户端"""
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_API_BASE or None,
            organization=Config.OPENAI_ORGANIZATION or None,
            timeout=Config.TIMEOUT
        )
        self.model = Config.OPENAI_MODEL

    def translate(self, text, target_lang=None, style=None, custom_prompt=None):
        """
        使用OpenAI API翻译文本
        :param text: 要翻译的文本
        :param target_lang: 目标语言
        :param style: 翻译风格
        :param custom_prompt: 自定义提示词
        :return: 翻译后的文本
        """
        try:
            # 使用自定义提示词或默认提示词
            if custom_prompt:
                prompt = custom_prompt.format(
                    text=text,
                    target_lang=target_lang or self.DEFAULT_TARGET_LANG,
                    style=style or self.DEFAULT_TRANSLATION_STYLE
                )
            else:
                prompt = self.DEFAULT_TRANSLATION_PROMPT.format(
                    text=text,
                    target_lang=target_lang or self.DEFAULT_TARGET_LANG,
                    style=style or self.DEFAULT_TRANSLATION_STYLE
                )

            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的翻译助手，精通多国语言，擅长保持原文风格的翻译。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS_PER_REQUEST,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            # 提取翻译结果
            translated_text = response.choices[0].message.content.strip()
            return translated_text

        except Exception as e:
            print(f"翻译出错: {str(e)}")
            return text  # 出错时返回原文 