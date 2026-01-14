"""
Configuration management for the AI Smart Recruiter application.

Centralizes all configuration values and supports environment variable overrides.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class ModelConfig:
    """Configuration for embedding model."""
    name: str = "all-MiniLM-L6-v2"
    cache_dir: Optional[str] = None
    device: str = "cpu"  # or "cuda" if GPU available


@dataclass
class OllamaConfig:
    """Configuration for Ollama LLM."""
    base_url: str = "http://localhost:11434"
    model_name: str = "llama3"
    timeout: int = 30
    temperature: float = 0.7
    context_window: int = 4096
    max_resume_chars: int = 4000


@dataclass
class AppConfig:
    """General application configuration."""
    upload_dir: str = "uploads"
    max_file_size_mb: int = 10
    supported_formats: tuple = ("pdf",)
    default_top_n: int = 10
    ai_analysis_top_n: int = 3
    grid_columns: int = 3
    results_limit_options: List[int] = field(default_factory=lambda: [5, 10, 25, 50])


@dataclass
class Config:
    """Main configuration class."""
    model: ModelConfig
    ollama: OllamaConfig
    app: AppConfig

    @classmethod
    def from_env(cls):
        """
        Load configuration from environment variables.

        Returns:
            Config instance with values from environment or defaults
        """
        return cls(
            model=ModelConfig(
                name=os.getenv("MODEL_NAME", "all-MiniLM-L6-v2"),
                cache_dir=os.getenv("MODEL_CACHE_DIR"),
                device=os.getenv("MODEL_DEVICE", "cpu")
            ),
            ollama=OllamaConfig(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                model_name=os.getenv("OLLAMA_MODEL", "llama3"),
                timeout=int(os.getenv("OLLAMA_TIMEOUT", "30")),
                temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.7")),
                context_window=int(os.getenv("OLLAMA_CONTEXT", "4096")),
                max_resume_chars=int(os.getenv("MAX_RESUME_CHARS", "4000"))
            ),
            app=AppConfig(
                upload_dir=os.getenv("UPLOAD_DIR", "uploads"),
                max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "10")),
                default_top_n=int(os.getenv("DEFAULT_TOP_N", "10")),
                ai_analysis_top_n=int(os.getenv("AI_ANALYSIS_TOP_N", "3")),
                grid_columns=int(os.getenv("GRID_COLUMNS", "3"))
            )
        )


# Global config instance
config = Config.from_env()
