from src.app import create_app
import webbrowser
import threading
import time
import os
import sys
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('translate_book.log', encoding='utf-8')
    ]
)

def open_browser():
    """延迟3秒后打开浏览器"""
    try:
        time.sleep(3)
        webbrowser.open('http://127.0.0.1:5000')
        logging.info("浏览器已打开")
    except Exception as e:
        logging.error(f"打开浏览器失败: {str(e)}")

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    except Exception as e:
        logging.error(f"获取资源路径失败: {str(e)}")
        return relative_path

def init_app():
    """初始化应用"""
    try:
        # 确保上传目录存在
        uploads_dir = resource_path('uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        logging.info(f"上传目录已创建: {uploads_dir}")
        
        # 创建应用实例
        app = create_app('development')
        logging.info("应用实例已创建")
        return app
    except Exception as e:
        logging.error(f"初始化应用失败: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        logging.info("启动翻译书籍应用")
        app = init_app()
        
        # 在新线程中打开浏览器
        threading.Thread(target=open_browser, daemon=True).start()
        
        # 启动应用
        logging.info("开始运行Flask应用")
        app.run(debug=False, port=5000, host='127.0.0.1')
    except Exception as e:
        logging.error(f"应用运行失败: {str(e)}")
        input("按回车键退出...") 