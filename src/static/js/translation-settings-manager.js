// 翻译设置管理模块
class TranslationSettingsManager {
    constructor() {
        this.currentBookId = null;
        this.initEventListeners();
    }

    // 初始化事件监听
    initEventListeners() {
        document.getElementById('saveTranslationSettings').addEventListener('click', this.saveSettings.bind(this));
    }

    // 显示翻译设置
    async showSettings(bookId) {
        this.currentBookId = bookId;
        try {
            // 加载可用的选项
            const [languagesResponse, stylesResponse, templatesResponse] = await Promise.all([
                fetch('/api/languages'),
                fetch('/api/styles'),
                fetch('/api/templates')
            ]);

            const languages = await languagesResponse.json();
            const styles = await stylesResponse.json();
            const templates = await templatesResponse.json();

            // 填充选项
            document.getElementById('targetLanguage').innerHTML = languages
                .filter(lang => lang.is_enabled)
                .map(lang => `<option value="${lang.name}">${lang.name}</option>`)
                .join('');

            document.getElementById('translationStyle').innerHTML = styles
                .filter(style => style.is_enabled)
                .map(style => `<option value="${style.name}">${style.name}</option>`)
                .join('');

            document.getElementById('promptTemplate').innerHTML = templates
                .filter(template => template.is_enabled)
                .map(template => `<option value="${template.name}">${template.name}</option>`)
                .join('');

            // 加载当前设置
            const settingsResponse = await fetch(`/api/translation_settings/${bookId}`);
            const settings = await settingsResponse.json();

            if (settings.has_settings) {
                document.getElementById('targetLanguage').value = settings.settings.target_language;
                document.getElementById('translationStyle').value = settings.settings.translation_style;
                document.getElementById('promptTemplate').value = settings.settings.prompt_template;
                document.getElementById('customPrompt').value = settings.settings.custom_prompt || '';
            }

            translationSettingsModal.show();
        } catch (error) {
            console.error('加载翻译设置失败:', error);
            showToast('加载翻译设置失败', 'error');
        }
    }

    // 保存翻译设置
    async saveSettings() {
        if (!this.currentBookId) return;
        
        const data = {
            target_language: document.getElementById('targetLanguage').value,
            translation_style: document.getElementById('translationStyle').value,
            prompt_template: document.getElementById('promptTemplate').value,
            custom_prompt: document.getElementById('customPrompt').value
        };
        
        try {
            const response = await fetch(`/api/save_translation_settings/${this.currentBookId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || '保存设置失败');
            }
            
            translationSettingsModal.hide();
            await bookManager.loadBooks();
            showToast('保存设置成功');
        } catch (error) {
            console.error('保存设置失败:', error);
            showToast(error.message || '保存设置失败', 'error');
        }
    }
}

// 创建全局实例
const translationSettingsManager = new TranslationSettingsManager(); 