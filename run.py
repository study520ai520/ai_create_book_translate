from src.app import create_app
import webbrowser
import threading
import time
import os
import sys

def open_browser():
    """延迟3秒后打开浏览器"""
    time.sleep(3)
    webbrowser.open('http://127.0.0.1:5000')

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
    # 确保上传目录存在
    uploads_dir = resource_path('uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # 创建应用实例
    app = create_app('development')
    
    # 在新线程中打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 启动应用
    app.run(debug=False, port=5000) 