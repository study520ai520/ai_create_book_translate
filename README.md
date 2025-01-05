# 书籍翻译器

这是一个基于Python和Flask的书籍翻译工具，支持多种文档格式的上传和翻译。

## 功能特点

- 支持上传PDF、TXT、DOC、DOCX格式的文档
- 自动将文档分割成较小的文本碎片
- 显示每本书的翻译进度
- 支持查看和管理文本碎片
- 提供翻译功能（需要配置翻译API）

## 安装要求

1. Python 3.7+
2. 所需Python包（在requirements.txt中列出）

## 安装步骤

1. 克隆仓库：
```bash
git clone <repository-url>
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python app.py
```

## 使用说明

1. 访问 http://localhost:5000
2. 点击"上传"按钮上传文档
3. 在左侧面板查看已上传的书籍列表和翻译进度
4. 点击"查看碎片"按钮查看文档的详细内容
5. 点击"翻译"按钮翻译各个文本碎片

## 注意事项

- 目前翻译功能使用示例实现，需要替换为实际的翻译API
- 上传大文件时可能需要较长处理时间
- 建议将文档切割大小控制在合理范围内

## 目录结构

```
.
├── app.py              # Flask应用主文件
├── models.py           # 数据库模型
├── document_processor.py # 文档处理模块
├── translator.py       # 翻译模块
├── requirements.txt    # 项目依赖
├── templates/         # HTML模板
│   └── index.html    # 主页面
└── uploads/          # 上传文件存储目录
```

## 配置说明

- 在`app.py`中可以修改上传目录和数据库配置
- 在`document_processor.py`中可以调整文本切割的大小
- 在`translator.py`中需要配置实际的翻译API 