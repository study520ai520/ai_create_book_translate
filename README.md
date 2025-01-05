# AI 翻译助手

一个基于 AI 的智能翻译工具，支持多语言翻译、多种翻译风格和自定义提示词模板。

## 功能特点

- 支持多种文档格式上传和翻译
- 智能文本分段，确保翻译质量
- 支持多语言翻译目标
- 可选择不同翻译风格
- 自定义提示词模板
- 实时翻译进度显示
- 支持多书籍同时翻译
- 翻译队列管理
- 导出双语对照文档

## 项目结构

```
translate_book/
├── config/                 # 配置文件目录
│   └── config.py          # 应用配置
├── src/                   # 源代码目录
│   ├── api/              # API 接口
│   │   ├── book_api.py   # 书籍相关接口
│   │   ├── settings_api.py # 设置相关接口
│   │   └── translation_api.py # 翻译相关接口
│   ├── models/           # 数据模型
│   │   ├── book.py      # 书籍和片段模型
│   │   └── settings.py  # 设置相关模型
│   ├── services/        # 业务服务
│   │   ├── document_service.py # 文档处理服务
│   │   └── translation_service.py # 翻译服务
│   ├── static/          # 静态资源
│   │   ├── css/        # 样式文件
│   │   └── js/         # JavaScript 文件
│   │       ├── book-manager.js          # 书籍管理模块
│   │       ├── translation-queue-manager.js # 翻译队列管理
│   │       ├── translation-settings-manager.js # 翻译设置管理
│   │       └── global-settings-manager.js # 全局设置管理
│   ├── templates/       # 模板文件
│   │   └── index.html  # 主页面
│   ├── app.py          # 应用入口
│   └── database.py     # 数据库配置
└── uploads/            # 上传文件存储目录
```

## 核心模块说明

### 后端模块

1. **API 模块** (`src/api/`)
   - `book_api.py`: 处理书籍上传、查询、翻译和导出
   - `settings_api.py`: 管理翻译语言、风格和模板设置
   - `translation_api.py`: 处理单个片段的翻译请求

2. **数据模型** (`src/models/`)
   - `book.py`: 定义书籍和文本片段的数据结构
   - `settings.py`: 定义翻译设置相关的数据结构

3. **服务层** (`src/services/`)
   - `document_service.py`: 处理文档解析和分段
   - `translation_service.py`: 对接 AI 翻译服务

### 前端模块

1. **书籍管理** (`static/js/book-manager.js`)
   - 书籍列表展示
   - 上传和删除功能
   - 翻译进度显示
   - 导出功能

2. **翻译队列管理** (`static/js/translation-queue-manager.js`)
   - 翻译任务队列
   - 进度显示
   - 错误处理
   - 实时日志

3. **翻译设置管理** (`static/js/translation-settings-manager.js`)
   - 翻译参数配置
   - 语言选择
   - 风格设置
   - 模板管理

4. **全局设置管理** (`static/js/global-settings-manager.js`)
   - 系统设置管理
   - 语言类型管理
   - 翻译风格管理
   - 提示词模板管理

## 环境要求

- Python 3.8+
- Flask
- SQLAlchemy
- OpenAI API Key

## 配置说明

1. 创建 `.env` 文件，包含以下配置：
```
OPENAI_API_KEY=your_api_key
MAX_TOKENS_PER_REQUEST=8000
FRAGMENT_SIZE=2000
FRAGMENT_MIN_SIZE=100
FRAGMENT_OVERLAP=50
```

2. 配置数据库：
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///translate_book.db'
```

## 使用说明

1. 上传文档：
   - 支持 TXT、DOCX 等格式
   - 自动分段处理

2. 设置翻译参数：
   - 选择目标语言
   - 选择翻译风格
   - 选择或自定义提示词模板

3. 开始翻译：
   - 点击"开始翻译"按钮
   - 实时查看翻译进度
   - 支持多本书籍同时翻译

4. 导出结果：
   - 导出双语对照文档
   - 支持 DOCX 格式

## 开发说明

1. 克隆项目：
```bash
git clone https://github.com/your-repo/translate_book.git
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库：
```bash
flask db upgrade
```

4. 运行项目：
```bash
flask run
``` 