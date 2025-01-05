// 翻译队列管理器
class TranslationQueueManager {
    constructor() {
        this.queue = new Map(); // 使用Map存储队列中的任务，key为bookId_fragmentId
        this.processing = false; // 是否正在处理任务
        this.currentTask = null; // 当前正在处理的任务
        
        // 不在构造函数中显示窗口，而是在添加任务时显示
        this.initEventListeners();
    }

    // 初始化事件监听
    initEventListeners() {
        // 可以添加一些事件监听，比如清空队列等
    }

    // 添加翻译任务到队列
    addTask(bookId, bookName, fragmentId, text) {
        const taskId = `${bookId}_${fragmentId}`;
        
        // 如果任务已经在队列中，则不重复添加
        if (this.queue.has(taskId)) {
            console.log(`任务已在队列中: ${taskId}`);
            return;
        }

        // 创建新任务
        const task = {
            bookId,
            bookName,
            fragmentId,
            text,
            status: 'pending', // pending, processing, completed, error
            progress: 0
        };

        console.log('添加新任务到队列:', task);
        this.addLogMessage(`添加任务: ${bookName} - 片段 #${fragmentId}`);

        // 添加到队列
        this.queue.set(taskId, task);
        
        // 显示队列和日志窗口
        document.getElementById('translationQueue').classList.add('active');
        document.getElementById('translationLog').classList.add('active');
        
        // 更新队列显示
        this.updateQueueDisplay();
        
        // 如果当前没有正在处理的任务，开始处理
        if (!this.processing) {
            console.log('开始处理队列中的任务');
            this.processNextTask();
        }
    }

    // 更新队列显示
    updateQueueDisplay() {
        const queueContent = document.getElementById('queueContent');
        let html = '';

        this.queue.forEach((task, taskId) => {
            html += `
                <div class="queue-item">
                    <div class="book-name">${task.bookName}</div>
                    <div class="fragment-info">片段 #${task.fragmentId}</div>
                    <div class="status">${this.getStatusText(task.status)}</div>
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: ${task.progress}%"></div>
                    </div>
                </div>
            `;
        });

        queueContent.innerHTML = html || '<div class="text-muted">队列为空</div>';
    }

    // 获取状态文本
    getStatusText(status) {
        const statusMap = {
            'pending': '等待中',
            'processing': '翻译中',
            'completed': '已完成',
            'error': '失败'
        };
        return statusMap[status] || status;
    }

    // 处理下一个任务
    async processNextTask() {
        if (this.processing || this.queue.size === 0) {
            console.log('当前无法处理任务:', { processing: this.processing, queueSize: this.queue.size });
            return;
        }

        this.processing = true;
        const [taskId, task] = Array.from(this.queue.entries())[0];
        this.currentTask = task;

        console.log('开始处理任务:', task);
        this.addLogMessage(`开始翻译: ${task.bookName} - 片段 #${task.fragmentId}`);

        try {
            // 更新任务状态
            task.status = 'processing';
            task.progress = 0;
            this.updateQueueDisplay();

            // 调用翻译API
            const response = await fetch(`/api/book/${task.bookId}/translate_fragment/${task.fragmentId}`, {
                method: 'POST'
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || '翻译请求失败');
            }

            console.log('翻译成功:', result);
            this.addLogMessage(`翻译成功: ${task.bookName} - 片段 #${task.fragmentId}`);

            // 更新任务状态
            task.status = 'completed';
            task.progress = 100;
            this.updateQueueDisplay();

            // 从队列中移除已完成的任务
            this.queue.delete(taskId);

            // 刷新书籍列表以更新进度
            await bookManager.loadBooks();

        } catch (error) {
            console.error('翻译失败:', error);
            this.addLogMessage(`翻译失败: ${task.bookName} - 片段 #${task.fragmentId} - ${error.message}`, 'error');
            
            task.status = 'error';
            this.updateQueueDisplay();
            
            // 从队列中移除失败的任务
            this.queue.delete(taskId);
        }

        this.processing = false;
        this.currentTask = null;

        // 继续处理下一个任务
        if (this.queue.size > 0) {
            console.log('继续处理下一个任务');
            setTimeout(() => this.processNextTask(), 1000); // 添加1秒延迟，避免请求过于频繁
        } else {
            console.log('所有任务处理完成');
            this.addLogMessage('所有翻译任务已完成');
        }
    }

    // 添加日志消息
    addLogMessage(message, type = 'info') {
        const logContent = document.getElementById('logContent');
        const timestamp = new Date().toLocaleTimeString();
        const className = type === 'error' ? 'error-info' : 'progress-info';
        
        logContent.innerHTML += `
            <div class="log-item ${className}">
                [${timestamp}] ${message}
            </div>
        `;
        
        // 滚动到底部
        logContent.scrollTop = logContent.scrollHeight;
    }

    // 清空队列
    clearQueue() {
        this.queue.clear();
        this.updateQueueDisplay();
        this.addLogMessage('已清空翻译队列');
    }
}

// 创建全局实例
const translationQueueManager = new TranslationQueueManager(); 