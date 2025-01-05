// 书籍管理模块
class BookManager {
    constructor() {
        this.initEventListeners();
    }

    // 初始化事件监听
    initEventListeners() {
        // 文件上传事件
        document.getElementById('bookFile').addEventListener('change', this.handleFileUpload.bind(this));
        
        // 文件拖拽事件
        const uploadZone = document.querySelector('.upload-zone');
        uploadZone.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadZone.addEventListener('drop', this.handleDrop.bind(this));
    }

    // 加载书籍列表
    async loadBooks() {
        try {
            const response = await fetch('/api/books');
            if (!response.ok) throw new Error('加载书籍列表失败');
            const books = await response.json();
            this.renderBooks(books);
        } catch (error) {
            console.error('加载书籍列表失败:', error);
            showToast('加载书籍列表失败', 'error');
        }
    }

    // 渲染书籍列表
    renderBooks(books) {
        const bookList = document.getElementById('bookList');
        bookList.innerHTML = books.map(book => `
            <div class="book-card">
                <div class="book-info">
                    <div class="book-title">
                        <i class="bi bi-book"></i>
                        ${book.name}
                    </div>
                    <div class="translation-settings">
                        ${book.has_translation_settings ? `
                            <span class="badge bg-info">目标语言: ${book.target_language}</span>
                            <span class="badge bg-info">翻译风格: ${book.translation_style}</span>
                            <span class="badge bg-info">提示词模板: ${book.prompt_template}</span>
                        ` : '<span class="badge bg-warning">未设置翻译参数</span>'}
                    </div>
                </div>
                <div class="progress-section">
                    <small class="text-muted">翻译进度: ${book.progress}%</small>
                    <div class="progress">
                        <div class="progress-bar" role="progressbar" style="width: ${book.progress}%" 
                            aria-valuenow="${book.progress}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                </div>
                <div class="action-buttons">
                    ${book.has_translation_settings ? `
                        ${book.progress === 0 ? `
                            <button class="btn btn-primary" onclick="bookManager.translateBook(${book.id})">
                                <i class="bi bi-translate"></i> 开始翻译
                            </button>
                        ` : book.progress < 100 ? `
                            <button class="btn btn-primary" onclick="bookManager.translateRemaining(${book.id})">
                                <i class="bi bi-translate"></i> 继续翻译
                            </button>
                        ` : ''}
                        ${book.progress === 0 ? `
                            <button class="btn btn-warning" onclick="translationSettingsManager.showSettings(${book.id})">
                                <i class="bi bi-gear"></i> 修改翻译参数
                            </button>
                        ` : ''}
                    ` : `
                        <button class="btn btn-primary" onclick="translationSettingsManager.showSettings(${book.id})">
                            <i class="bi bi-gear"></i> 设置翻译参数
                        </button>
                    `}
                    <button class="btn btn-info" onclick="bookManager.showFragments(${book.id})">
                        <i class="bi bi-list-ul"></i> 查看碎片
                    </button>
                    <button class="btn btn-success" onclick="bookManager.exportBook(${book.id})">
                        <i class="bi bi-download"></i> 导出
                    </button>
                    <button class="btn btn-danger" onclick="bookManager.deleteBook(${book.id})">
                        <i class="bi bi-trash"></i> 删除
                    </button>
                </div>
            </div>
        `).join('') || '<div class="text-center text-muted mt-4">暂无书籍</div>';
    }

    // 文件上传处理
    async handleFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        await this.uploadFile(file);
        e.target.value = '';  // 清空文件选择
    }

    // 处理拖拽
    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.style.borderColor = 'var(--primary-color)';
        e.currentTarget.style.backgroundColor = 'rgba(74, 144, 226, 0.05)';
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.style.borderColor = '#ddd';
        e.currentTarget.style.backgroundColor = '';
    }

    async handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        
        e.currentTarget.style.borderColor = '#ddd';
        e.currentTarget.style.backgroundColor = '';
        
        const file = e.dataTransfer.files[0];
        if (!file) return;
        await this.uploadFile(file);
    }

    // 上传文件
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            showLoading();
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error('上传失败');
            
            await this.loadBooks();
            showToast('上传成功');
        } catch (error) {
            console.error('上传失败:', error);
            showToast('上传失败', 'error');
        } finally {
            hideLoading();
        }
    }

    // 查看碎片
    async showFragments(bookId) {
        try {
            const response = await fetch(`/api/book/${bookId}/fragments`);
            if (!response.ok) throw new Error('加载碎片失败');
            const fragments = await response.json();
            
            document.getElementById('fragmentList').innerHTML = fragments.map(fragment => `
                <div class="fragment-card">
                    <div class="fragment-number">碎片 #${fragment.number}</div>
                    <div class="text-section">
                        <strong>原文：</strong>
                        <div>${fragment.original_text}</div>
                    </div>
                    ${fragment.translated_text ? `
                        <div class="text-section">
                            <strong>译文：</strong>
                            <div>${fragment.translated_text}</div>
                        </div>
                    ` : ''}
                </div>
            `).join('');
            
            fragmentModal.show();
        } catch (error) {
            console.error('加载碎片失败:', error);
            showToast('加载碎片失败', 'error');
        }
    }

    // 导出书籍
    exportBook(bookId) {
        window.location.href = `/api/export/${bookId}`;
    }

    // 删除书籍
    async deleteBook(bookId) {
        if (confirm('确定要删除这本书吗？此操作不可恢复。')) {
            try {
                const response = await fetch(`/api/delete/${bookId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) throw new Error('删除失败');
                
                await this.loadBooks();
                showToast('删除成功');
            } catch (error) {
                console.error('删除失败:', error);
                showToast('删除失败', 'error');
            }
        }
    }

    // 翻译整本书
    async translateBook(bookId) {
        if (!confirm('确定要开始翻译这本书吗？')) return;
        
        try {
            showLoading();
            const response = await fetch(`/api/translate_remaining/${bookId}`, {
                method: 'POST'
            });
            
            if (!response.ok) throw new Error('翻译失败');
            
            showToast('翻译任务已启动');
            this.startTranslationProgress(bookId);
        } catch (error) {
            console.error('翻译失败:', error);
            showToast('翻译失败', 'error');
            hideLoading();
        }
    }

    // 继续翻译未完成的部分
    async translateRemaining(bookId) {
        if (!confirm('确定要继续翻译未完成的部分吗？')) return;
        
        try {
            showLoading();
            const response = await fetch(`/api/translate_remaining/${bookId}`, {
                method: 'POST'
            });
            
            if (!response.ok) throw new Error('翻译失败');
            
            showToast('翻译任务已启动');
            this.startTranslationProgress(bookId);
        } catch (error) {
            console.error('翻译失败:', error);
            showToast('翻译失败', 'error');
            hideLoading();
        }
    }

    // 监控翻译进度
    startTranslationProgress(bookId) {
        const progressCheck = async () => {
            try {
                const response = await fetch(`/api/translation_progress/${bookId}`);
                if (!response.ok) throw new Error('获取进度失败');
                
                const progress = await response.json();
                if (progress.completed === progress.total) {
                    // 翻译完成
                    hideLoading();
                    await this.loadBooks();
                    showToast('翻译完成');
                    return;
                }
                
                // 更新进度显示
                const percent = Math.round((progress.completed / progress.total) * 100);
                showToast(`翻译进度: ${percent}%`, 'info');
                
                // 继续检查进度
                setTimeout(progressCheck, 2000);
            } catch (error) {
                console.error('获取翻译进度失败:', error);
                hideLoading();
            }
        };
        
        // 开始检查进度
        progressCheck();
    }
}

// 创建全局实例
const bookManager = new BookManager(); 