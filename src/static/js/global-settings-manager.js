// 全局设置管理模块
class GlobalSettingsManager {
    constructor() {
        this.languages = [];
        this.styles = [];
        this.templates = [];
        this.initEventListeners();
    }

    // 初始化事件监听
    initEventListeners() {
        // 监听设置选项卡切换事件
        document.querySelectorAll('#settingsTabs button').forEach(button => {
            button.addEventListener('click', (e) => {
                const tabId = e.target.getAttribute('data-bs-target').substring(1);
                switch (tabId) {
                    case 'languages':
                        this.loadLanguages();
                        break;
                    case 'styles':
                        this.loadStyles();
                        break;
                    case 'templates':
                        this.loadTemplates();
                        break;
                }
            });
        });

        // 监听保存按钮点击事件
        document.getElementById('saveLanguageBtn')?.addEventListener('click', () => this.saveLanguage());
        document.getElementById('saveStyleBtn')?.addEventListener('click', () => this.saveStyle());
        document.getElementById('saveTemplateBtn')?.addEventListener('click', () => this.saveTemplate());
    }

    // 初始化设置
    async initSettings() {
        await Promise.all([
            this.loadLanguages(),
            this.loadStyles(),
            this.loadTemplates()
        ]);
    }

    // 加载语言列表
    async loadLanguages() {
        try {
            const response = await fetch('/api/languages');
            this.languages = await response.json();
            this.renderLanguagesTable();
        } catch (error) {
            console.error('加载语言列表失败:', error);
            showToast('加载语言列表失败', 'error');
        }
    }

    // 加载风格列表
    async loadStyles() {
        try {
            const response = await fetch('/api/styles');
            this.styles = await response.json();
            this.renderStylesTable();
        } catch (error) {
            console.error('加载风格列表失败:', error);
            showToast('加载风格列表失败', 'error');
        }
    }

    // 加载模板列表
    async loadTemplates() {
        try {
            const response = await fetch('/api/templates');
            this.templates = await response.json();
            this.renderTemplatesTable();
        } catch (error) {
            console.error('加载模板列表失败:', error);
            showToast('加载模板列表失败', 'error');
        }
    }

    // 渲染语言表格
    renderLanguagesTable() {
        const tbody = document.getElementById('languagesTableBody');
        tbody.innerHTML = this.languages.map(lang => `
            <tr>
                <td>${lang.name}</td>
                <td>${lang.description || ''}</td>
                <td>
                    <span class="badge ${lang.is_enabled ? 'bg-success' : 'bg-secondary'}">
                        ${lang.is_enabled ? '启用' : '禁用'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="globalSettingsManager.editLanguage(${lang.id})">编辑</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="globalSettingsManager.deleteLanguage(${lang.id})">删除</button>
                </td>
            </tr>
        `).join('');
    }

    // 渲染风格表格
    renderStylesTable() {
        const tbody = document.getElementById('stylesTableBody');
        tbody.innerHTML = this.styles.map(style => `
            <tr>
                <td>${style.name}</td>
                <td>${style.description || ''}</td>
                <td>
                    <span class="badge ${style.is_enabled ? 'bg-success' : 'bg-secondary'}">
                        ${style.is_enabled ? '启用' : '禁用'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="globalSettingsManager.editStyle(${style.id})">编辑</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="globalSettingsManager.deleteStyle(${style.id})">删除</button>
                </td>
            </tr>
        `).join('');
    }

    // 渲染模板表格
    renderTemplatesTable() {
        const tbody = document.getElementById('templatesTableBody');
        tbody.innerHTML = this.templates.map(template => `
            <tr>
                <td>${template.name}</td>
                <td>${template.description || ''}</td>
                <td>
                    <span class="badge ${template.is_system ? 'bg-info' : 'bg-primary'}">
                        ${template.is_system ? '系统' : '自定义'}
                    </span>
                </td>
                <td>
                    <span class="badge ${template.is_enabled ? 'bg-success' : 'bg-secondary'}">
                        ${template.is_enabled ? '启用' : '禁用'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="globalSettingsManager.editTemplate(${template.id})">
                        ${template.is_system ? '查看' : '编辑'}
                    </button>
                    ${!template.is_system ? `
                        <button class="btn btn-sm btn-outline-danger" onclick="globalSettingsManager.deleteTemplate(${template.id})">删除</button>
                    ` : ''}
                </td>
            </tr>
        `).join('');
    }

    // 语言管理相关方法
    showAddLanguageModal() {
        document.getElementById('languageModalTitle').textContent = '添加语言';
        document.getElementById('languageForm').reset();
        document.getElementById('languageId').value = '';
        new bootstrap.Modal(document.getElementById('languageModal')).show();
    }

    async editLanguage(id) {
        try {
            const response = await fetch(`/api/languages/${id}`);
            if (!response.ok) throw new Error('获取语言信息失败');
            const language = await response.json();
            
            document.getElementById('languageModalTitle').textContent = '编辑语言';
            document.getElementById('languageId').value = language.id;
            document.getElementById('languageName').value = language.name;
            document.getElementById('languageDescription').value = language.description || '';
            document.getElementById('languageEnabled').checked = language.is_enabled;
            
            new bootstrap.Modal(document.getElementById('languageModal')).show();
        } catch (error) {
            console.error('编辑语言失败:', error);
            showToast('编辑语言失败', 'error');
        }
    }

    async saveLanguage() {
        const id = document.getElementById('languageId').value;
        const data = {
            name: document.getElementById('languageName').value,
            description: document.getElementById('languageDescription').value,
            is_enabled: document.getElementById('languageEnabled').checked
        };
        
        try {
            const url = id ? `/api/languages/${id}` : '/api/languages';
            const method = id ? 'PUT' : 'POST';
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) throw new Error('保存语言失败');
            
            bootstrap.Modal.getInstance(document.getElementById('languageModal')).hide();
            await this.loadLanguages();
            showToast('保存成功');
        } catch (error) {
            console.error('保存语言失败:', error);
            showToast('保存语言失败', 'error');
        }
    }

    async deleteLanguage(id) {
        if (confirm('确定要删除这个语言吗？')) {
            try {
                const response = await fetch(`/api/languages/${id}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) throw new Error('删除语言失败');
                
                await this.loadLanguages();
                showToast('删除成功');
            } catch (error) {
                console.error('删除语言失败:', error);
                showToast('删除语言失败', 'error');
            }
        }
    }

    // 风格管理相关方法
    showAddStyleModal() {
        document.getElementById('styleModalTitle').textContent = '添加风格';
        document.getElementById('styleForm').reset();
        document.getElementById('styleId').value = '';
        new bootstrap.Modal(document.getElementById('styleModal')).show();
    }

    async editStyle(id) {
        try {
            const response = await fetch(`/api/styles/${id}`);
            if (!response.ok) throw new Error('获取风格信息失败');
            const style = await response.json();
            
            document.getElementById('styleModalTitle').textContent = '编辑风格';
            document.getElementById('styleId').value = style.id;
            document.getElementById('styleName').value = style.name;
            document.getElementById('styleDescription').value = style.description || '';
            document.getElementById('styleEnabled').checked = style.is_enabled;
            
            new bootstrap.Modal(document.getElementById('styleModal')).show();
        } catch (error) {
            console.error('编辑风格失败:', error);
            showToast('编辑风格失败', 'error');
        }
    }

    async saveStyle() {
        const id = document.getElementById('styleId').value;
        const data = {
            name: document.getElementById('styleName').value,
            description: document.getElementById('styleDescription').value,
            is_enabled: document.getElementById('styleEnabled').checked
        };
        
        try {
            const url = id ? `/api/styles/${id}` : '/api/styles';
            const method = id ? 'PUT' : 'POST';
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) throw new Error('保存风格失败');
            
            bootstrap.Modal.getInstance(document.getElementById('styleModal')).hide();
            await this.loadStyles();
            showToast('保存成功');
        } catch (error) {
            console.error('保存风格失败:', error);
            showToast('保存风格失败', 'error');
        }
    }

    async deleteStyle(id) {
        if (confirm('确定要删除这个风格吗？')) {
            try {
                const response = await fetch(`/api/styles/${id}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) throw new Error('删除风格失败');
                
                await this.loadStyles();
                showToast('删除成功');
            } catch (error) {
                console.error('删除风格失败:', error);
                showToast('删除风格失败', 'error');
            }
        }
    }

    // 模板管理相关方法
    showAddTemplateModal() {
        document.getElementById('templateModalTitle').textContent = '添加模板';
        document.getElementById('templateForm').reset();
        document.getElementById('templateId').value = '';
        new bootstrap.Modal(document.getElementById('templateModal')).show();
    }

    async editTemplate(id) {
        try {
            const response = await fetch(`/api/templates/${id}`);
            if (!response.ok) throw new Error('获取模板信息失败');
            const template = await response.json();
            
            document.getElementById('templateModalTitle').textContent = template.is_system ? '查看模板' : '编辑模板';
            document.getElementById('templateId').value = template.id;
            document.getElementById('templateName').value = template.name;
            document.getElementById('templateDescription').value = template.description || '';
            document.getElementById('templateContent').value = template.template;
            document.getElementById('templateEnabled').checked = template.is_enabled;
            
            // 如果是系统模板，禁用编辑
            const isSystem = template.is_system;
            document.getElementById('templateName').disabled = isSystem;
            document.getElementById('templateDescription').disabled = isSystem;
            document.getElementById('templateContent').disabled = isSystem;
            document.getElementById('saveTemplateBtn').style.display = isSystem ? 'none' : 'block';
            
            new bootstrap.Modal(document.getElementById('templateModal')).show();
        } catch (error) {
            console.error('编辑模板失败:', error);
            showToast('编辑模板失败', 'error');
        }
    }

    async saveTemplate() {
        const id = document.getElementById('templateId').value;
        const data = {
            name: document.getElementById('templateName').value,
            description: document.getElementById('templateDescription').value,
            template: document.getElementById('templateContent').value,
            is_enabled: document.getElementById('templateEnabled').checked
        };
        
        try {
            const url = id ? `/api/templates/${id}` : '/api/templates';
            const method = id ? 'PUT' : 'POST';
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) throw new Error('保存模板失败');
            
            bootstrap.Modal.getInstance(document.getElementById('templateModal')).hide();
            await this.loadTemplates();
            showToast('保存成功');
        } catch (error) {
            console.error('保存模板失败:', error);
            showToast('保存模板失败', 'error');
        }
    }

    async deleteTemplate(id) {
        if (confirm('确定要删除这个模板吗？')) {
            try {
                const response = await fetch(`/api/templates/${id}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) throw new Error('删除模板失败');
                
                await this.loadTemplates();
                showToast('删除成功');
            } catch (error) {
                console.error('删除模板失败:', error);
                showToast('删除模板失败', 'error');
            }
        }
    }
}

// 创建全局实例
const globalSettingsManager = new GlobalSettingsManager(); 