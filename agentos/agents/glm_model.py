"""
Z.AI GLM Model Integration for AgentOS

This module provides a clean interface for using Z.AI GLM models
with the Agno framework through OpenAI compatibility.
"""

import os
from typing import Optional, Dict, Any, List
from agno.models.openai import OpenAIChat
import logging

# Import centralized configuration
try:
    from ..config.models import DEFAULT_MODEL, MODEL_CAPABILITIES
except ImportError:
    # Fallback if config not available
    DEFAULT_MODEL = "glm-4.6"
    MODEL_CAPABILITIES = {}

logger = logging.getLogger(__name__)


class GLMModel:
    """
    Z.AI GLM Model wrapper for Agno framework
    
    Uses OpenAI-compatible API to integrate GLM models with Agno agents
    """
    
    # Available GLM models
    AVAILABLE_MODELS = {
        "glm-4.6": {
            "description": "Latest GLM-4.6 model, most capable and intelligent",
            "context_window": 128000,
            "max_tokens": 8192
        },
        "glm-4-plus": {
            "description": "Most capable GLM-4 model, complex tasks",
            "context_window": 128000,
            "max_tokens": 8192
        },
        "glm-4": {
            "description": "Balanced GLM-4 model for general tasks",
            "context_window": 128000,
            "max_tokens": 8192
        },
        "glm-4-flash": {
            "description": "Fast GLM-4 model for simple tasks",
            "context_window": 128000,
            "max_tokens": 8192
        },
        "glm-4-long": {
            "description": "Long context GLM-4 model",
            "context_window": 1000000,
            "max_tokens": 4096
        },
        "glm-3-turbo": {
            "description": "Fast GLM-3 model for simple tasks",
            "context_window": 128000,
            "max_tokens": 4096
        }
    }
    
    def __init__(
        self,
        model_id: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        base_url: str = "https://open.bigmodel.cn/api/paas/v4/",
        **kwargs
    ):
        """
        Initialize GLM model
        
        Args:
            model_id: GLM model identifier
            api_key: Zhipu API key (defaults to ZHIPU_API_KEY env var)
            base_url: API base URL
            **kwargs: Additional arguments for OpenAIChat
        """
        if model_id not in self.AVAILABLE_MODELS:
            logger.warning(f"Unknown model: {model_id}. Available: {list(self.AVAILABLE_MODELS.keys())}")
        
        self.model_id = model_id
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "ZHIPU_API_KEY not found. Please set the environment variable "
                "or pass api_key parameter"
            )
        
        # Initialize OpenAI-compatible client
        self.client = OpenAIChat(
            model=model_id,
            api_key=self.api_key,
            base_url=base_url,
            **kwargs
        )
        
        logger.info(f"Initialized GLM model: {model_id}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model_id": self.model_id,
            "info": self.AVAILABLE_MODELS.get(self.model_id, {}),
            "provider": "Z.AI",
            "api_base": "https://open.bigmodel.cn/api/paas/v4/"
        }
    
    @classmethod
    def list_available_models(cls) -> Dict[str, Dict[str, Any]]:
        """List all available GLM models"""
        return cls.AVAILABLE_MODELS.copy()
    
    @property
    def model(self):
        """Get the underlying Agno model instance"""
        return self.client


def create_glm_agent(
    agent_class,
    model_id: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
    **agent_kwargs
):
    """
    Factory function to create agents with GLM models
    
    Args:
        agent_class: The agent class to instantiate
        model_id: GLM model identifier
        api_key: Zhipu API key
        **agent_kwargs: Additional arguments for the agent
    
    Returns:
        Agent instance with GLM model
    """
    glm_model = GLMModel(model_id=model_id, api_key=api_key)
    
    # Inject the model into agent kwargs
    agent_kwargs["model"] = glm_model.model
    
    return agent_class(**agent_kwargs)


# Recommended model configurations for different use cases
MODEL_RECOMMENDATIONS = {
    "content_creation": "glm-4.6",          # Latest and most capable
    "analysis": "glm-4.6",                # Best analytical capabilities
    "simple_tasks": "glm-4-flash",         # Fast and efficient
    "long_context": "glm-4-long",          # For large documents
    "cost_optimized": "glm-3-turbo",       # Most economical
    "vietnamese_content": "glm-4.6",       # Best for Vietnamese language
    "trend_analysis": "glm-4.6",           # Latest for trend insights
    "social_media": "glm-4.6"              # Most creative for social content
}


def get_recommended_model(use_case: str) -> str:
    """
    Get recommended GLM model for specific use case
    
    Args:
        use_case: Type of task (content_creation, analysis, simple_tasks, etc.)
    
    Returns:
        Recommended model ID
    """
    return MODEL_RECOMMENDATIONS.get(use_case, "glm-4.6")


# Vietnamese language optimization
VIETNAMESE_PROMPT_TEMPLATE = """
Bạn là một trợ lý AI thông minh hỗ trợ tiếng Việt. Hãy trả lời các câu hỏi bằng tiếng Việt một cách tự nhiên và chính xác.

Khi trả lời:
1. Sử dụng ngôn ngữ tự nhiên, gần gũi với người Việt
2. Định dạng câu trả lời rõ ràng, dễ đọc
3. Cung cấp thông tin chính xác và hữu ích
4. Sử dụng emoji phù hợp khi cần thiết để tăng tính thân thiện

Câu hỏi: {question}

Câu trả lời:
"""


def create_vietnamese_glm(model_id: str = DEFAULT_MODEL, **kwargs):
    """
    Create GLM model optimized for Vietnamese language tasks
    
    Args:
        model_id: GLM model identifier
        **kwargs: Additional arguments
    
    Returns:
        GLM model instance with Vietnamese optimization
    """
    return GLMModel(
        model_id=model_id,
        temperature=0.7,  # Slightly creative for natural language
        max_tokens=4096,  # Good for Vietnamese responses
        **kwargs
    )