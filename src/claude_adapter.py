"""Claude API adapter for DeepSeek Vision integration"""

import os
from typing import Optional, Dict, List
from loguru import logger

try:
    import anthropic
except ImportError:
    anthropic = None

from .deepseek_vision import DeepSeekVisionTool


class DeepSeekImageRecognitionAdapter:
    """Claude 和 DeepSeek Vision 的适配器"""

    def __init__(
        self,
        deepseek_api_key: Optional[str] = None,
        claude_api_key: Optional[str] = None
    ):
        """
        初始化适配器
        
        Args:
            deepseek_api_key: DeepSeek API Key
            claude_api_key: Claude API Key
        """
        if anthropic is None:
            raise ImportError("需要安装 anthropic 包: pip install anthropic")
        
        self.deepseek_tool = DeepSeekVisionTool(deepseek_api_key)
        self.claude_api_key = claude_api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if self.claude_api_key:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            self.claude_client = None
            logger.warning("Claude API Key 未提供，将只使用 DeepSeek Vision")
    
    def register_tool(self) -> Dict:
        """定义工具给 Claude"""
        return {
            "name": "deepseek_image_recognition",
            "description": "使用 DeepSeek Vision 识别图片内容。支持本地文件路径和网络 URL。",
            "input_schema": {
                "type": "object",
                "properties": {
                    "image_url": {
                        "type": "string",
                        "description": "图片 URL 或本地文件路径"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "识别提示词（例如：请描述这张图片、请识别图片中的物体等）",
                        "default": "请详细描述这张图片的内容"
                    }
                },
                "required": ["image_url"]
            }
        }
    
    def process_tool_call(self, tool_name: str, tool_input: Dict) -> str:
        """
        处理 Claude 的工具调用
        
        Args:
            tool_name: 工具名称
            tool_input: 工具输入
        
        Returns:
            工具执行结果
        
        Raises:
            ValueError: 未知的工具
        """
        if tool_name == "deepseek_image_recognition":
            image_url = tool_input.get("image_url")
            prompt = tool_input.get("prompt", "请详细描述这张图片的内容")
            
            logger.debug(f"处理工具调用: image_url={image_url}, prompt={prompt}")
            return self.deepseek_tool.recognize_image(image_url, prompt)
        
        raise ValueError(f"未知的工具: {tool_name}")
    
    def chat_with_vision(self, user_message: str, tools: Optional[List[Dict]] = None) -> str:
        """
        使用 Claude 和图片识别进行对话
        
        Args:
            user_message: 用户消息
            tools: 工具列表
        
        Returns:
            Claude 的响应
        
        Raises:
            RuntimeError: Claude API 客户端未初始化
        """
        if not self.claude_client:
            raise RuntimeError("Claude API 客户端未初始化。请提供 ANTHROPIC_API_KEY。")
        
        if tools is None:
            tools = [self.register_tool()]
        
        messages = [{"role": "user", "content": user_message}]
        
        logger.debug(f"开始对话: {user_message[:100]}...")
        
        # 循环处理工具调用
        iteration = 0
        max_iterations = 10  # 防止无限循环
        
        while iteration < max_iterations:
            iteration += 1
            logger.debug(f"对话迭代 {iteration}")
            
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                tools=tools,
                messages=messages
            )
            
            logger.debug(f"Claude 响应 stop_reason: {response.stop_reason}")
            
            # 检查是否需要调用工具
            if response.stop_reason == "tool_use":
                # 找到工具使用块
                tool_use_block = None
                for content_block in response.content:
                    if content_block.type == "tool_use":
                        tool_use_block = content_block
                        break
                
                if tool_use_block:
                    logger.info(f"调用工具: {tool_use_block.name}")
                    
                    try:
                        tool_result = self.process_tool_call(
                            tool_use_block.name,
                            tool_use_block.input
                        )
                        
                        # 添加助手响应
                        messages.append({
                            "role": "assistant",
                            "content": response.content
                        })
                        
                        # 添加工具结果
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_block.id,
                                    "content": tool_result
                                }
                            ]
                        })
                    except Exception as e:
                        logger.error(f"工具执行失败: {e}")
                        # 添加错误消息
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_block.id,
                                    "content": f"工具执行失败: {str(e)}",
                                    "is_error": True
                                }
                            ]
                        })
            else:
                # 返回最终响应
                final_response = ""
                for content_block in response.content:
                    if hasattr(content_block, "text"):
                        final_response += content_block.text
                
                logger.debug(f"对话完成，返回响应")
                return final_response
        
        logger.warning(f"达到最大迭代次数 {max_iterations}")
        return "对话超出最大迭代次数"
    
    def direct_recognize(self, image_url: str, prompt: str = "请详细描述这张图片的内容") -> str:
        """
        直接调用 DeepSeek Vision（不经过 Claude）
        
        Args:
            image_url: 图片 URL 或本地路径
            prompt: 识别提示词
        
        Returns:
            识别结果
        """
        return self.deepseek_tool.recognize_image(image_url, prompt)
    
    def batch_chat(
        self,
        messages: List[str],
        tools: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        批量处理多个对话
        
        Args:
            messages: 消息列表
            tools: 工具列表
        
        Returns:
            响应列表
        """
        results = []
        for idx, message in enumerate(messages, 1):
            logger.info(f"处理对话 {idx}/{len(messages)}")
            try:
                response = self.chat_with_vision(message, tools)
                results.append({"status": "success", "response": response})
            except Exception as e:
                logger.error(f"对话处理失败: {e}")
                results.append({"status": "error", "error": str(e)})
        
        return results
