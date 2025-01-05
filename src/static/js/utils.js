// 工具函数模块

// 显示/隐藏加载动画
function showLoading() {
    document.getElementById('loading').classList.remove('d-none');
}

function hideLoading() {
    document.getElementById('loading').classList.add('d-none');
}

// 显示提示信息
function showToast(message, type = 'success') {
    // 创建提示框元素
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // 添加到容器
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.appendChild(toast);
    document.body.appendChild(container);
    
    // 初始化 Bootstrap toast
    const bsToast = new bootstrap.Toast(toast, {
        animation: true,
        autohide: true,
        delay: 3000
    });
    
    // 显示提示框
    bsToast.show();
    
    // 监听隐藏事件，移除元素
    toast.addEventListener('hidden.bs.toast', () => {
        container.remove();
    });
}

// 导出工具函数
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showToast = showToast; 