"""
Universal News - Configuration Management
Centralized configuration for all agents and system components
"""

import os
from typing import Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMConfig(BaseModel):
    """Configuration for LLM providers"""
    provider: str = Field(default="openai", description="LLM provider (openai, anthropic, etc.)")
    model_name: str = Field(default="gpt-4-turbo-preview", description="Model to use")
    api_key: str = Field(..., description="API key for the provider")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1)
    timeout_seconds: int = Field(default=60)
    
    # Cost tracking (per 1K tokens)
    input_cost_per_1k: float = Field(default=0.01)
    output_cost_per_1k: float = Field(default=0.03)


class NLPConfig(BaseModel):
    """Configuration for NLP processing"""
    spacy_model: str = Field(default="en_core_web_lg", description="SpaCy model to use")
    sentence_transformer_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Model for embeddings"
    )
    max_content_length: int = Field(default=50000, description="Max characters to process")


class AgentConfig(BaseModel):
    """Configuration for individual agents"""
    timeout_seconds: int = Field(default=120, description="Max execution time")
    max_retries: int = Field(default=3, description="Retry failed operations")
    enable_caching: bool = Field(default=True, description="Cache intermediate results")
    log_level: str = Field(default="INFO", description="Logging verbosity")


class DatabaseConfig(BaseModel):
    """Database connection settings"""
    # NOTE: For Step 1, we'll use in-memory storage
    # Full implementation will use PostgreSQL
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    database: str = Field(default="universal_news")
    username: str = Field(default="postgres")
    password: str = Field(default="")
    
    # Connection pool
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)


class ExternalAPIConfig(BaseModel):
    """Configuration for external service integrations"""
    
    # Newswire Services
    pr_newswire_api_key: str = Field(default="")
    business_wire_api_key: str = Field(default="")
    
    # Email/SMTP
    smtp_host: str = Field(default="smtp.sendgrid.net")
    smtp_port: int = Field(default=587)
    smtp_username: str = Field(default="")
    smtp_password: str = Field(default="")
    from_email: str = Field(default="news@universal-news.ai")
    
    # Social Media
    twitter_api_key: str = Field(default="")
    twitter_api_secret: str = Field(default="")
    linkedin_access_token: str = Field(default="")
    
    # Analytics
    google_analytics_id: str = Field(default="")
    
    # Journalist Database
    meltwater_api_key: str = Field(default="")
    cision_api_key: str = Field(default="")


class SystemConfig(BaseModel):
    """Overall system configuration"""
    environment: str = Field(default="development", description="development, staging, production")
    debug_mode: bool = Field(default=True)
    
    # Async execution
    max_concurrent_agents: int = Field(default=5, description="Max parallel agent execution")
    enable_async: bool = Field(default=True)
    
    # Performance
    target_processing_time_seconds: float = Field(default=120.0)
    
    # Storage
    temp_storage_path: str = Field(default="/tmp/universal_news")
    persistent_storage_path: str = Field(default="./data")
    
    # Monitoring
    enable_metrics: bool = Field(default=True)
    metrics_export_interval_seconds: int = Field(default=60)


class Config:
    """
    Master configuration class
    Loads all configuration from environment variables
    """
    
    def __init__(self):
        self.llm = LLMConfig(
            provider=os.getenv("LLM_PROVIDER", "openai"),
            model_name=os.getenv("LLM_MODEL", "gpt-4-turbo-preview"),
            api_key=os.getenv("OPENAI_API_KEY", "sk-mock-key-for-testing"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        )
        
        self.nlp = NLPConfig(
            spacy_model=os.getenv("SPACY_MODEL", "en_core_web_lg"),
        )
        
        self.agent = AgentConfig(
            timeout_seconds=int(os.getenv("AGENT_TIMEOUT", "120")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
        
        self.database = DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "universal_news"),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
        )
        
        self.external_apis = ExternalAPIConfig(
            pr_newswire_api_key=os.getenv("PR_NEWSWIRE_API_KEY", ""),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            twitter_api_key=os.getenv("TWITTER_API_KEY", ""),
            linkedin_access_token=os.getenv("LINKEDIN_ACCESS_TOKEN", ""),
        )
        
        self.system = SystemConfig(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug_mode=os.getenv("DEBUG", "true").lower() == "true",
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            "llm": self.llm.model_dump(),
            "nlp": self.nlp.model_dump(),
            "agent": self.agent.model_dump(),
            "database": self.database.model_dump(),
            "external_apis": self.external_apis.model_dump(exclude={"smtp_password", "twitter_api_secret"}),
            "system": self.system.model_dump(),
        }
    
    def validate(self) -> bool:
        """Validate critical configuration"""
        issues = []
        
        if not self.llm.api_key or self.llm.api_key == "sk-mock-key-for-testing":
            issues.append("LLM API key not configured")
        
        if self.system.environment == "production":
            if self.system.debug_mode:
                issues.append("Debug mode should be disabled in production")
            if not self.external_apis.smtp_password:
                issues.append("SMTP credentials required for production")
        
        if issues:
            print("⚠️  Configuration Issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        
        return True


# Global configuration instance
config = Config()


# Convenience getters
def get_llm_config() -> LLMConfig:
    """Get LLM configuration"""
    return config.llm


def get_agent_config() -> AgentConfig:
    """Get agent configuration"""
    return config.agent


def get_nlp_config() -> NLPConfig:
    """Get NLP configuration"""
    return config.nlp


def get_external_api_config() -> ExternalAPIConfig:
    """Get external API configuration"""
    return config.external_apis


def get_system_config() -> SystemConfig:
    """Get system configuration"""
    return config.system


# Initialize configuration on import
if __name__ == "__main__":
    print("Universal News Configuration")
    print("=" * 50)
    print(f"Environment: {config.system.environment}")
    print(f"Debug Mode: {config.system.debug_mode}")
    print(f"LLM Provider: {config.llm.provider}")
    print(f"LLM Model: {config.llm.model_name}")
    print("\nValidation:", "✅ PASSED" if config.validate() else "❌ FAILED")
