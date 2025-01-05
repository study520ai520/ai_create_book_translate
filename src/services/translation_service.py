import openai
from config.config import Config

class TranslationService:
    """翻译服务"""
    
    def __init__(self):
        """初始化OpenAI配置"""
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.default_prompt = Config.DEFAULT_TRANSLATION_PROMPT
        self.default_target_lang = Config.DEFAULT_TARGET_LANG
        self.default_style = Config.DEFAULT_TRANSLATION_STYLE

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
                    target_lang=target_lang or self.default_target_lang,
                    style=style or self.default_style
                )
            else:
                prompt = self.default_prompt.format(
                    text=text,
                    target_lang=target_lang or self.default_target_lang
                )
                if style:
                    prompt += f"\n\n翻译风格：{style}"

            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的翻译助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
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