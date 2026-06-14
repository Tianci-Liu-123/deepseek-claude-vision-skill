"""DeepSeek Vision API integration module"""

import requests
import base64
import os
from pathlib import Path
from typing import Optional, Union
from loguru import logger


class DeepSeekVisionTool:
    """DeepSeek Vision 图片识别工具"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 DeepSeek Vision 工具
        
        Args:
            api_key: DeepSeek API Key，如果不提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DeepSeek API Key 未提供。请设置 DEEPSEEK_API_KEY 环境变量或传入 api_key 参数。")
        
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1")
        self.model = "deepseek-vision"
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        
        logger.debug(f"DeepSeekVisionTool 初始化完成: {self.api_url}")

    def recognize_image(
        self,
        image_input: Union[str, Path],
        prompt: str = "请详细描述这张图片的内容"
    ) -> str:
        """
        识别图片内容
        
        Args:
            image_input: 图片URL或本地文件路径
            prompt: 识别提示词
        
        Returns:
            识别结果文本
        
        Raises:
            ValueError: 无效的图片输入
            requests.RequestException: API 请求失败
        """
        logger.info(f"开始识别图片: {image_input}")
        
        # 处理图片输入
        image_url = self._prepare_image(image_input)
        
        # 构建请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        }
        
        # 发送请求（带重试机制）
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"发送请求到 DeepSeek API (尝试 {attempt + 1}/{self.max_retries})")
                response = requests.post(
                    f"{self.api_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                
                if "choices" not in result:
                    raise ValueError(f"API 返回格式错误: {result}")
                
                content = result["choices"][0]["message"]["content"]
                logger.info(f"成功识别图片")
                return content
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    logger.error(f"API 请求失败: {e}")
                    raise
            except (ValueError, KeyError) as e:
                logger.error(f"响应处理错误: {e}")
                raise

    def _prepare_image(self, image_input: Union[str, Path]) -> str:
        """
        处理图片输入（URL或本地文件）
        
        Args:
            image_input: 图片URL或本地文件路径
        
        Returns:
            图片的 URL 或 Base64 编码的数据URI
        
        Raises:
            ValueError: 无效的图片输入
        """
        image_input_str = str(image_input)
        
        # 如果是 URL，直接返回
        if image_input_str.startswith(("http://", "https://")):
            logger.debug(f"使用网络 URL: {image_input_str}")
            return image_input_str
        
        # 如果是本地文件，转换为 Base64
        file_path = Path(image_input_str)
        if file_path.exists():
            logger.debug(f"读取本地文件: {file_path}")
            
            # 检查文件大小
            max_size = int(os.getenv("MAX_IMAGE_SIZE", "10485760"))  # 10MB
            file_size = file_path.stat().st_size
            if file_size > max_size:
                raise ValueError(f"图片文件过大: {file_size} bytes (最大: {max_size} bytes)")
            
            with open(file_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            
            # 推断图片格式
            suffix = file_path.suffix.lower()
            mime_type = self._get_mime_type(suffix)
            
            data_uri = f"data:image/{mime_type};base64,{img_data}"
            logger.debug(f"转换为 Base64 (MIME: {mime_type})")
            return data_uri
        
        # 如果既不是 URL 也不是本地文件
        raise ValueError(f"无效的图片输入: {image_input_str} (不是有效的 URL 或本地文件路径)")

    @staticmethod
    def _get_mime_type(suffix: str) -> str:
        """
        根据文件扩展名获取 MIME 类型
        
        Args:
            suffix: 文件扩展名
        
        Returns:
            MIME 类型
        """
        mime_types = {
            ".jpg": "jpeg",
            ".jpeg": "jpeg",
            ".png": "png",
            ".gif": "gif",
            ".webp": "webp",
            ".bmp": "bmp",
            ".tiff": "tiff"
        }
        return mime_types.get(suffix, "jpeg")

    def batch_recognize(
        self,
        image_inputs: list,
        prompt: str = "请详细描述这张图片的内容",
        show_progress: bool = True
    ) -> list:
        """
        批量识别多张图片
        
        Args:
            image_inputs: 图片输入列表
            prompt: 识别提示词
            show_progress: 是否显示进度
        
        Returns:
            识别结果列表
        """
        results = []
        total = len(image_inputs)
        
        for idx, image_input in enumerate(image_inputs, 1):
            try:
                if show_progress:
                    logger.info(f"处理 {idx}/{total}...")
                
                result = self.recognize_image(image_input, prompt)
                results.append({
                    "input": str(image_input),
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                logger.error(f"处理失败 {image_input}: {e}")
                results.append({
                    "input": str(image_input),
                    "status": "error",
                    "error": str(e)
                })
        
        logger.info(f"批量处理完成: 成功 {sum(1 for r in results if r['status'] == 'success')}/{total}")
        return results
