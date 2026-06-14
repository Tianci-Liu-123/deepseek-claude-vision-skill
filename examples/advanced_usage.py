"""Advanced usage examples"""

import os
from pathlib import Path

# 添加 src 到 Python 路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.deepseek_vision import DeepSeekVisionTool
from src.utils import setup_logging, load_config, batch_process_images, save_results, format_results


def batch_processing_example():
    """批量处理图片示例"""
    print("\n=== 批量处理图片 ===")
    
    config = load_config()
    setup_logging(config["log_level"])
    tool = DeepSeekVisionTool(api_key=config["deepseek_api_key"])
    
    # 准备图片列表
    images = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Natural_Color_Landsat_8_Mosaic_Denali.jpg/640px-Natural_Color_Landsat_8_Mosaic_Denali.jpg",
    ]
    
    # 批量识别
    results = tool.batch_recognize(
        images,
        prompt="请详细描述这张图片"
    )
    
    # 显示结果
    print(format_results(results))
    
    # 保存结果
    save_results(results, "batch_results.json")


def custom_prompts_example():
    """自定义提示词示例"""
    print("\n=== 自定义提示词 ===")
    
    config = load_config()
    setup_logging(config["log_level"])
    tool = DeepSeekVisionTool(api_key=config["deepseek_api_key"])
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
    
    # 不同的提示词
    prompts = {
        "描述": "请详细描述这张图片",
        "物体检测": "列出这张图片中所有的物体",
        "颜色分析": "分析这张图片中的主要颜色",
        "场景理解": "这张图片的场景是什么？背景是什么？",
    }
    
    for task, prompt in prompts.items():
        print(f"\n--- {task} ---")
        try:
            result = tool.recognize_image(image_url, prompt)
            print(result)
        except Exception as e:
            print(f"错误: {e}")


def error_handling_example():
    """错误处理示例"""
    print("\n=== 错误处理 ===")
    
    config = load_config()
    setup_logging(config["log_level"])
    tool = DeepSeekVisionTool(api_key=config["deepseek_api_key"])
    
    # 测试各种错误情况
    test_cases = [
        ("invalid_url", "无效的URL"),
        ("./nonexistent_file.jpg", "不存在的本地文件"),
        ("https://example.com/404.jpg", "404 图片"),
    ]
    
    for input_val, description in test_cases:
        print(f"\n--- 测试: {description} ---")
        try:
            result = tool.recognize_image(input_val, "识别图片")
            print(f"结果: {result}")
        except Exception as e:
            print(f"捕获的错误: {type(e).__name__}: {e}")


def main():
    """运行所有示例"""
    print("="*60)
    print("高级用法示例")
    print("="*60)
    
    try:
        batch_processing_example()
    except Exception as e:
        print(f"批量处理示例失败: {e}")
    
    try:
        custom_prompts_example()
    except Exception as e:
        print(f"自定义提示词示例失败: {e}")
    
    try:
        error_handling_example()
    except Exception as e:
        print(f"错误处理示例失败: {e}")


if __name__ == "__main__":
    main()
