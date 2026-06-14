"""Basic usage example"""

import os
from pathlib import Path

# 添加 src 到 Python 路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.deepseek_vision import DeepSeekVisionTool
from src.utils import setup_logging, load_config


def main():
    # 加载配置
    config = load_config()
    setup_logging(config["log_level"])
    
    # 初始化工具
    tool = DeepSeekVisionTool(api_key=config["deepseek_api_key"])
    
    # 示例 1: 识别网络图片
    print("\n=== 示例 1: 识别网络图片 ===")
    try:
        # 使用一个公开的测试图片 URL
        result = tool.recognize_image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg",
            "请描述这张图片中的食物"
        )
        print(f"识别结果:\n{result}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 示例 2: 识别本地图片（如果存在的话）
    print("\n=== 示例 2: 识别本地图片 ===")
    local_image_path = "./test_image.jpg"
    if Path(local_image_path).exists():
        try:
            result = tool.recognize_image(
                local_image_path,
                "请详细描述这张图片"
            )
            print(f"识别结果:\n{result}")
        except Exception as e:
            print(f"错误: {e}")
    else:
        print(f"本地图片不存在: {local_image_path}")
    
    # 示例 3: 文字识别 (OCR)
    print("\n=== 示例 3: 文字识别 ===")
    try:
        result = tool.recognize_image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg",
            "从这张图片中提取所有的文字"
        )
        print(f"提取的文字:\n{result}")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
