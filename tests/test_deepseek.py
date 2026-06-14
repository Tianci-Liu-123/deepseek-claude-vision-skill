"""Tests for DeepSeek Vision module"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加 src 到 Python 路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.deepseek_vision import DeepSeekVisionTool


class TestDeepSeekVisionTool:
    """DeepSeekVisionTool 测试类"""
    
    def test_initialization_with_api_key(self):
        """测试使用 API Key 初始化"""
        api_key = "test_api_key"
        tool = DeepSeekVisionTool(api_key=api_key)
        assert tool.api_key == api_key
    
    def test_initialization_without_api_key(self):
        """测试没有 API Key 时的初始化"""
        # 移除环境变量
        if "DEEPSEEK_API_KEY" in os.environ:
            del os.environ["DEEPSEEK_API_KEY"]
        
        with pytest.raises(ValueError):
            DeepSeekVisionTool()
    
    def test_mime_type_detection(self):
        """测试 MIME 类型检测"""
        test_cases = [
            (".jpg", "jpeg"),
            (".jpeg", "jpeg"),
            (".png", "png"),
            (".gif", "gif"),
            (".webp", "webp"),
            (".unknown", "jpeg"),  # 默认
        ]
        
        for suffix, expected in test_cases:
            result = DeepSeekVisionTool._get_mime_type(suffix)
            assert result == expected
    
    def test_url_validation(self):
        """测试 URL 验证"""
        tool = DeepSeekVisionTool(api_key="test_key")
        
        # 测试有效的 URL
        urls = [
            "https://example.com/image.jpg",
            "http://example.com/image.png",
        ]
        
        for url in urls:
            result = tool._prepare_image(url)
            assert result == url
    
    def test_invalid_image_input(self):
        """测试无效的图片输入"""
        tool = DeepSeekVisionTool(api_key="test_key")
        
        with pytest.raises(ValueError):
            tool._prepare_image("invalid_input")
    
    @patch('requests.post')
    def test_recognize_image_success(self, mock_post):
        """测试成功识别图片"""
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "这是一张图片的描述"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        tool = DeepSeekVisionTool(api_key="test_key")
        result = tool.recognize_image(
            "https://example.com/image.jpg",
            "请描述这张图片"
        )
        
        assert result == "这是一张图片的描述"
        assert mock_post.called
    
    @patch('requests.post')
    def test_recognize_image_api_error(self, mock_post):
        """测试 API 错误处理"""
        # 模拟 API 错误
        mock_post.side_effect = Exception("API Error")
        
        tool = DeepSeekVisionTool(api_key="test_key")
        
        with pytest.raises(Exception):
            tool.recognize_image(
                "https://example.com/image.jpg",
                "请描述这张图片"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
