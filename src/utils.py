"""Utility functions"""

import os
import json
from pathlib import Path
from typing import List, Dict
from loguru import logger


def load_config(config_path: str = ".env") -> Dict:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
    
    Returns:
        配置字典
    """
    from dotenv import load_dotenv
    load_dotenv(config_path)
    
    config = {
        "deepseek_api_key": os.getenv("DEEPSEEK_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }
    
    return config


def setup_logging(log_level: str = "INFO"):
    """
    设置日志
    
    Args:
        log_level: 日志级别
    """
    logger.remove()  # 移除默认处理器
    
    # 创建日志目录
    Path("logs").mkdir(exist_ok=True)
    
    logger.add(
        "logs/deepseek_vision.log",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="500 MB"
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level,
        format="<level>{time:YYYY-MM-DD HH:mm:ss}</level> | <level>{level: <8}</level> | {message}"
    )


def batch_process_images(
    image_paths: List[str],
    tool,
    prompt: str = "请详细描述这张图片的内容"
) -> List[Dict]:
    """
    批量处理图片
    
    Args:
        image_paths: 图片路径列表
        tool: DeepSeekVisionTool 实例
        prompt: 识别提示词
    
    Returns:
        处理结果列表
    """
    return tool.batch_recognize(image_paths, prompt)


def save_results(results: List[Dict], output_file: str = "results.json"):
    """
    保存识别结果到文件
    
    Args:
        results: 结果列表
        output_file: 输出文件路径
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"结果已保存到: {output_path}")


def load_results(input_file: str) -> List[Dict]:
    """
    从文件加载识别结果
    
    Args:
        input_file: 输入文件路径
    
    Returns:
        结果列表
    """
    with open(input_file, "r", encoding="utf-8") as f:
        results = json.load(f)
    
    return results


def format_results(results: List[Dict]) -> str:
    """
    格式化识别结果
    
    Args:
        results: 结果列表
    
    Returns:
        格式化的结果字符串
    """
    output = []
    for idx, result in enumerate(results, 1):
        output.append(f"\n{'='*60}")
        output.append(f"图片 {idx}: {result.get('input', 'Unknown')}")
        output.append(f"{'='*60}")
        
        if result["status"] == "success":
            output.append(result["result"])
        else:
            output.append(f"错误: {result.get('error', 'Unknown error')}")
    
    return "\n".join(output)
