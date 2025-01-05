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
python run.py
```

## 使用说明

1. 访问 http://localhost:5000
2. 点击"上传"按钮上传文档
3. 在左侧面板查看已上传的书籍列表和翻译进度
4. 点击"查看碎片"按钮查看文档的详细内容
5. 点击"翻译"按钮翻译各个文本碎片

## 项目结构

```
.
├── config/             # 配置文件
│   └── config.py      # 应用配置
├── src/               # 源代码
│   ├── api/           # API路由
│   │   ├── book_api.py
│   │   └── translation_api.py
│   ├── database/      # 数据库相关
│   │   └── db.py
│   ├── models/        # 数据模型
│   │   ├── book.py
│   │   └── fragment.py
│   ├── services/      # 业务逻辑
│   │   ├── document_service.py
│   │   └── translation_service.py
│   └── templates/     # HTML模板
│       └── index.html
├── uploads/           # 上传文件存储
├── requirements.txt   # 项目依赖
└── run.py            # 应用入口
```

## 配置说明

- 在`config/config.py`中可以修改应用配置：
  - 上传目录
  - 数据库设置
  - 文本切割大小
  - 支持的文件类型等

## 开发说明

1. API模块：
   - `book_api.py`: 处理书籍相关的API
   - `translation_api.py`: 处理翻译相关的API

2. 服务模块：
   - `document_service.py`: 文档处理服务
   - `translation_service.py`: 翻译服务

3. 数据模型：
   - `book.py`: 书籍模型
   - `fragment.py`: 文本碎片模型

## 注意事项

- 目前翻译功能使用示例实现，需要在`services/translation_service.py`中配置实际的翻译API
- 上传大文件时可能需要较长处理时间
- 建议将文档切割大小控制在合理范围内 

## 高级配置

### 翻译API配置
在 `config/config.py` 中配置翻译API相关参数：
```python
TRANSLATION_API_KEY = "your_api_key"
TRANSLATION_API_URL = "https://api.translation.com"
```

### 数据库配置
修改数据库连接参数：
```python
DATABASE_URL = "sqlite:///books.db"  # 默认使用SQLite
# 或使用其他数据库
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

### 文件处理配置
```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传文件大小（16MB）
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
FRAGMENT_SIZE = 1000  # 文本碎片大小（字符数）
```

## 故障排除

1. 文件上传失败
   - 检查文件大小是否超过限制
   - 确认文件格式是否支持
   - 检查uploads目录权限

2. 翻译服务异常
   - 验证API密钥是否正确
   - 检查网络连接
   - 查看日志文件获取详细错误信息

3. 数据库连接问题
   - 确认数据库服务是否运行
   - 检查数据库连接参数
   - 验证数据库用户权限

## 贡献指南

1. Fork 项目仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m '添加新特性'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

### 代码规范
- 遵循 PEP 8 Python代码风格指南
- 添加适当的注释和文档字符串
- 确保代码通过所有测试

## 更新日志

### v1.0.0 (2024-01-20)
- 初始版本发布
- 支持基本的文档上传和翻译功能
- 实现文本碎片管理

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至：[your-email@example.com]

## 致谢

感谢所有为本项目做出贡献的开发者。 