from src.app import create_app
import webbrowser
import threading
import time
import os
import sys
import logging
import shutil

# 配置日志
def setup_logging(base_path):
    """设置日志配置"""
    log_file = os.path.join(base_path, 'translate_book.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )

def get_base_path():
    """获取应用基础路径"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        return os.path.dirname(sys.executable)
    else:
        # 如果是开发环境
        return os.path.abspath(os.path.dirname(__file__))

def ensure_directory_structure(base_path):
    """确保必要的目录结构存在"""
    try:
        # 创建必要的目录
        dirs = ['uploads', 'database']
        for dir_name in dirs:
            dir_path = os.path.join(base_path, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"目录已创建/确认: {dir_path}")

        # 确保配置文件存在
        env_file = os.path.join(base_path, '.env')
        if not os.path.exists(env_file):
            default_env = os.path.join(base_path, '.env.example')
            if os.path.exists(default_env):
                shutil.copy2(default_env, env_file)
                logging.info(f"已创建配置文件: {env_file}")
            else:
                logging.warning("未找到默认配置文件模板")

    except Exception as e:
        logging.error(f"创建目录结构失败: {str(e)}")
        raise

def open_browser():
    """延迟3秒后打开浏览器"""
    try:
        time.sleep(3)
        webbrowser.open('http://127.0.0.1:5000')
        logging.info("浏览器已打开")
    except Exception as e:
        logging.error(f"打开浏览器失败: {str(e)}")

def init_app(base_path):
    """初始化应用"""
    try:
        # 确保目录结构存在
        ensure_directory_structure(base_path)
        
        # 设置环境变量
        os.environ['WORKSPACE_ROOT'] = base_path
        
        # 创建应用实例
        app = create_app('development')
        logging.info("应用实例已创建")
        return app
    except Exception as e:
        logging.error(f"初始化应用失败: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        # 获取基础路径
        base_path = get_base_path()
        
        # 设置日志
        setup_logging(base_path)
        
        logging.info(f"应用基础路径: {base_path}")
        logging.info("启动翻译书籍应用")
        
        # 初始化应用
        app = init_app(base_path)
        
        # 在新线程中打开浏览器
        threading.Thread(target=open_browser, daemon=True).start()
        
        # 启动应用
        logging.info("开始运行Flask应用")
        app.run(debug=False, port=5000, host='127.0.0.1')
    except Exception as e:
        logging.error(f"应用运行失败: {str(e)}")
        input("按回车键退出...") 