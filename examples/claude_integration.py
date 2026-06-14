"""Claude integration example"""

import os
from pathlib import Path

# 添加 src 到 Python 路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.claude_adapter import DeepSeekImageRecognitionAdapter
from src.utils import setup_logging, load_config


def main():
    # 加载配置
    config = load_config()
    setup_logging(config["log_level"])
    
    # 检查是否有 Claude API Key
    if not config["anthropic_api_key"]:
        print("错误: 未设置 ANTHROPIC_API_KEY 环境变量")
        print("请在 .env 文件中添加 ANTHROPIC_API_KEY")
        return
    
    # 初始化适配器
    adapter = DeepSeekImageRecognitionAdapter(
        deepseek_api_key=config["deepseek_api_key"],
        claude_api_key=config["anthropic_api_key"]
    )
    
    # 示例 1: 直接识别图片
    print("\n=== 示例 1: 直接识别图片（不使用 Claude）===")
    try:
        result = adapter.direct_recognize(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg",
            "请描述这张图片中的食物"
        )
        print(f"识别结果:\n{result}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 示例 2: 通过 Claude 对话识别图片
    print("\n=== 示例 2: 通过 Claude 对话识别图片 ===")
    try:
        response = adapter.chat_with_vision(
            "请帮我识别这张图片: https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg \n并告诉我图片中有什么食物"
        )
        print(f"Claude 的回复:\n{response}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 示例 3: 更复杂的对话任务
    print("\n=== 示例 3: 复杂的对话任务 ===")
    try:
        response = adapter.chat_with_vision(
            "我想根据一个 UI 设计图生成代码。\n"
            "这是图片: https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg\n"
            "首先请识别这张图片，然后告诉我如何用 React 组件来实现类似的布局。"
        )
        print(f"Claude 的回复:\n{response}")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
