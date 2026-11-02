import os

try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        # Fallback if pydantic is not installed
        class BaseSettings:
            def __init__(self, **kwargs):
                pass

class Settings(BaseSettings):
    APP_NAME: str = "SentinelVultr - Blast Radius Zero Agent Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1")

    # Vultr Serverless Inference Configuration
    VULTR_API_KEY: str = os.getenv("VULTR_API_KEY", "")
    VULTR_INFERENCE_BASE_URL: str = os.getenv("VULTR_INFERENCE_BASE_URL", "https://api.vultrinference.com/v1")
    VULTR_MODEL: str = os.getenv("VULTR_MODEL", "meta-llama/llama-3.3-70b-instruct")

    # Fallback / Alternate models available on Vultr Serverless Inference
    AVAILABLE_MODELS: list[str] = [
        "meta-llama/llama-3.3-70b-instruct",
        "meta-llama/llama-3.1-70b-instruct",
        "meta-llama/llama-3.1-8b-instruct",
        "mistralai/mistral-nemo",
    ]

    # Sandbox Configuration & Resource Constraints
    SANDBOX_DRIVER: str = os.getenv("SANDBOX_DRIVER", "auto")  # "docker", "local", "auto"
    CODE_SANDBOX_IMAGE: str = os.getenv("CODE_SANDBOX_IMAGE", "sentinel-vultr-code:latest")
    BROWSER_SANDBOX_IMAGE: str = os.getenv("BROWSER_SANDBOX_IMAGE", "sentinel-vultr-browser:latest")

    # Containment Hard Limits
    MAX_MEMORY_MB: int = int(os.getenv("MAX_MEMORY_MB", "512"))
    MAX_CPU_QUOTA: float = float(os.getenv("MAX_CPU_QUOTA", "1.0"))
    MAX_EXECUTION_TIMEOUT_SECONDS: int = int(os.getenv("MAX_EXECUTION_TIMEOUT_SECONDS", "30"))
    BLOCK_NETWORK_FOR_CODE: bool = os.getenv("BLOCK_NETWORK_FOR_CODE", "true").lower() in ("true", "1")

    # Host Protection
    ALLOWED_HOST_BINARIES: list[str] = ["python", "python3", "node", "bash", "sh"]
    HOST_SECRET_PATTERNS: list[str] = [
        "VULTR_API_KEY",
        "API_KEY",
        "SECRET",
        "TOKEN",
        "PASSWORD",
        "PRIVATE_KEY",
        "AWS_",
        "OPENAI_",
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
