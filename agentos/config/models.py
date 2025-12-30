"""
AgentOS Model Configuration

Centralized configuration for AI models used across the AgentOS system.
"""

# Default model settings
DEFAULT_MODEL = "glm-4.6"  # Latest and most capable GLM model

# Model configurations for different use cases
MODEL_CONFIG = {
    # Content Creation Models
    "text_creator": {
        "model": "glm-4.6",
        "temperature": 0.7,
        "max_tokens": 4096,
        "description": "Vietnamese social media copy generation"
    },
    
    "content_strategist": {
        "model": "glm-4.6", 
        "temperature": 0.6,
        "max_tokens": 8192,
        "description": "Content strategy and trend analysis"
    },
    
    "trend_monitor": {
        "model": "glm-4.6",
        "temperature": 0.5,
        "max_tokens": 4096,
        "description": "TikTok trend monitoring and analysis"
    }
}

# Fallback model configuration
FALLBACK_MODEL = "glm-4-plus"  # Backup if GLM-4.6 unavailable

# Model capabilities
MODEL_CAPABILITIES = {
    "glm-4.6": {
        "context_window": 128000,
        "max_tokens": 8192,
        "supports_vietnamese": True,
        "creative_writing": True,
        "analysis": True,
        "cost_tier": "premium"
    },
    "glm-4-plus": {
        "context_window": 128000,
        "max_tokens": 8192,
        "supports_vietnamese": True,
        "creative_writing": True,
        "analysis": True,
        "cost_tier": "high"
    },
    "glm-4": {
        "context_window": 128000,
        "max_tokens": 8192,
        "supports_vietnamese": True,
        "creative_writing": True,
        "analysis": True,
        "cost_tier": "medium"
    },
    "glm-4-flash": {
        "context_window": 128000,
        "max_tokens": 8192,
        "supports_vietnamese": True,
        "creative_writing": False,
        "analysis": False,
        "cost_tier": "low"
    },
    "glm-4-long": {
        "context_window": 1000000,
        "max_tokens": 4096,
        "supports_vietnamese": True,
        "creative_writing": True,
        "analysis": True,
        "cost_tier": "high"
    },
    "glm-3-turbo": {
        "context_window": 128000,
        "max_tokens": 4096,
        "supports_vietnamese": True,
        "creative_writing": False,
        "analysis": False,
        "cost_tier": "economy"
    }
}

def get_model_config(agent_name: str) -> dict:
    """
    Get model configuration for a specific agent
    
    Args:
        agent_name: Name of the agent (text_creator, content_strategist, trend_monitor)
    
    Returns:
        Model configuration dictionary
    """
    return MODEL_CONFIG.get(agent_name, {
        "model": DEFAULT_MODEL,
        "temperature": 0.7,
        "max_tokens": 4096,
        "description": "Default configuration"
    })

def get_model_capabilities(model_id: str) -> dict:
    """
    Get capabilities for a specific model
    
    Args:
        model_id: GLM model identifier
    
    Returns:
        Model capabilities dictionary
    """
    return MODEL_CAPABILITIES.get(model_id, MODEL_CAPABILITIES[DEFAULT_MODEL])

def is_model_supported(model_id: str) -> bool:
    """
    Check if a model is supported
    
    Args:
        model_id: GLM model identifier
    
    Returns:
        True if model is supported
    """
    return model_id in MODEL_CAPABILITIES

def get_best_model_for_task(
    requires_creativity: bool = False,
    requires_analysis: bool = False,
    long_context: bool = False,
    cost_conscious: bool = False
) -> str:
    """
    Get the best model for specific task requirements
    
    Args:
        requires_creativity: Task needs creative writing
        requires_analysis: Task needs analytical capabilities
        long_context: Task needs large context window
        cost_conscious: Optimize for cost
    
    Returns:
        Recommended model ID
    """
    if cost_conscious:
        return "glm-3-turbo" if not (requires_creativity or requires_analysis) else "glm-4-flash"
    
    if long_context:
        return "glm-4-long"
    
    if requires_creativity and requires_analysis:
        return "glm-4.6"
    
    if requires_creativity:
        return "glm-4.6"
    
    if requires_analysis:
        return "glm-4.6"
    
    return DEFAULT_MODEL