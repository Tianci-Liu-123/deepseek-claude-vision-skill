# DeepSeek Claude Vision Skill

一个完整的 Claude Code Skill 项目，集成 DeepSeek Vision 模型用于图片识别。

## 🎯 功能特性

- ✅ DeepSeek Vision 图片识别
- ✅ Claude Code 工具集成
- ✅ 支持本地文件和网络 URL
- ✅ Base64 编码支持
- ✅ 详细的错误处理
- ✅ 完整的示例代码
- ✅ 单元测试

## 📁 项目结构

```
deepseek-claude-vision-skill/
├── README.md                           # 项目说明
├── .env.example                        # 环境变量示例
├── requirements.txt                    # Python 依赖
├── setup.py                            # 安装配置
│
├── src/
│   ├── __init__.py
│   ├── deepseek_vision.py             # DeepSeek Vision 核心模块
│   ├── claude_adapter.py              # Claude 适配器
│   └── utils.py                       # 工具函数
│
├── tools/
│   ├── __init__.py
│   ├── deepseek_vision_tool.json      # 工具定义 (Manifest)
│   └── tool_handler.py                # 工具处理器
│
├── examples/
│   ├── basic_usage.py                 # 基础用法
│   ├── claude_integration.py          # Claude 集成示例
│   └── advanced_usage.py              # 高级用法
│
├── tests/
│   ├── __init__.py
│   ├── test_deepseek.py              # DeepSeek 单元测试
│   └── test_integration.py           # 集成测试
│
└── .copilot/
    └── tools.yml                      # Copilot 工具配置
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Tianci-Liu-123/deepseek-claude-vision-skill.git
cd deepseek-claude-vision-skill
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，添加你的 API Key
```

### 4. 运行示例

```bash
python examples/basic_usage.py
```

## 🔑 获取 API Key

### DeepSeek API Key
1. 访问 https://www.deepseek.com
2. 注册并登录
3. 进入 API 管理页面
4. 生成 API Key

### Claude API Key（可选）
1. 访问 https://console.anthropic.com
2. 创建 API Key

## 📖 使用方法

### 基础用法

```python
from src.deepseek_vision import DeepSeekVisionTool

# 初始化工具
tool = DeepSeekVisionTool(api_key="your_deepseek_api_key")

# 识别本地图片
result = tool.recognize_image("./photo.jpg", "请描述这张图片")
print(result)

# 识别网络图片
result = tool.recognize_image(
    "https://example.com/image.png",
    "这张图片里有什么?"
)
print(result)
```

### 与 Claude 集成

```python
from src.claude_adapter import DeepSeekImageRecognitionAdapter
import os

adapter = DeepSeekImageRecognitionAdapter(
    deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
    claude_api_key=os.getenv("ANTHROPIC_API_KEY")
)

response = adapter.chat_with_vision(
    "请识别这张图片并生成代码: https://example.com/ui.png"
)
print(response)
```

## 🛠️ 在 Claude Code 中集成

### 方法 1：GitHub Copilot

1. 将此项目克隆到本地
2. 在 VS Code 中打开项目
3. 在 Copilot Chat 中使用 `@deepseek-vision` 调用

### 方法 2：JetBrains IDE

1. 打开 IDE Settings
2. 导航到 AI Assistant → Custom Tools
3. 添加此项目的路径
4. 在代码编辑器中使用

### 方法 3：Cursor IDE

1. 在项目根目录创建 `.cursor` 文件夹
2. 复制 `.copilot/tools.yml` 到 `.cursor`
3. 重启 Cursor

## 🧪 测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_deepseek.py -v

# 生成覆盖率报告
pytest --cov=src tests/
```

## 📝 配置示例

### .env 文件

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxx
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEBUG=False
LOG_LEVEL=INFO
```

## 🎨 高级功能

### 自定义提示词

```python
custom_prompts = {
    "ocr": "从图片中提取所有文字",
    "object_detection": "列出图片中的所有物体",
    "scene_analysis": "分析图片的场景和背景",
    "code_generation": "根据这个UI设计生成代码"
}

result = tool.recognize_image(
    "image.png",
    prompt=custom_prompts["code_generation"]
)
```

### 批量处理图片

```python
from src.utils import batch_process_images

images = ["img1.jpg", "img2.jpg", "img3.jpg"]
results = batch_process_images(images, tool, "请描述每张图片")

for img, result in results:
    print(f"{img}: {result}")
```

## 🔧 工具配置详解

### deepseek_vision_tool.json

定义了工具的元数据、输入/输出schema、环境变量等。

### .copilot/tools.yml

配置了两个工具：
1. `deepseek_image_recognition` - 直接图片识别
2. `deepseek_claude_vision` - 通过 Claude 对话识别

## 📚 API 参考

### DeepSeekVisionTool

#### `recognize_image(image_input, prompt)`
识别图片内容

**参数：**
- `image_input` (str): 图片 URL 或本地文件路径
- `prompt` (str): 识别提示词

**返回：** 识别结果文本

#### `batch_recognize(image_inputs, prompt, show_progress)`
批量识别多张图片

**参数：**
- `image_inputs` (list): 图片输入列表
- `prompt` (str): 识别提示词
- `show_progress` (bool): 是否显示进度

**返回：** 结果列表

### DeepSeekImageRecognitionAdapter

#### `chat_with_vision(user_message, tools)`
通过 Claude 与图片识别进行对话

**参数：**
- `user_message` (str): 用户消息
- `tools` (list): 工具列表（可选）

**返回：** Claude 的回复

#### `direct_recognize(image_url, prompt)`
直接调用 DeepSeek Vision（不经过 Claude）

**参数：**
- `image_url` (str): 图片 URL 或本地路径
- `prompt` (str): 识别提示词

**返回：** 识别结果

## ⚙️ 环境要求

- Python >= 3.8
- 有效的 DeepSeek API Key
- （可选）有效的 Claude API Key

## 🐛 常见问题

### Q: 如何处理超大图片？
A: 工具会自动检查图片大小，默认限制为 10MB。可在 `.env` 中修改 `MAX_IMAGE_SIZE`。

### Q: 支持哪些图片格式？
A: 支持 JPG、PNG、GIF、WebP 等常见格式。

### Q: API 请求超时了怎么办？
A: 可在 `.env` 中调整 `REQUEST_TIMEOUT` 和 `MAX_RETRIES`。

### Q: 识别结果不准确怎么办？
A: 尝试优化提示词或改进图片质量。

## 📞 支持

- 📧 Email: your.email@example.com
- 🐛 Issues: https://github.com/Tianci-Liu-123/deepseek-claude-vision-skill/issues
- 📖 文档: [完整文档](./docs/README.md)

## 📄 许可证

MIT License

## 🚧 路线图

- [ ] 支持视频帧提取
- [ ] 本地模型支持
- [ ] 缓存机制
- [ ] 性能优化
- [ ] 更多示例
