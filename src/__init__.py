"""DeepSeek Claude Vision Skill Package"""

__version__ = "0.1.0"
__author__ = "Tianci Liu"

from .deepseek_vision import DeepSeekVisionTool
from .claude_adapter import DeepSeekImageRecognitionAdapter

__all__ = [
    "DeepSeekVisionTool",
    "DeepSeekImageRecognitionAdapter",
]
