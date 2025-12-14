"""
Universal News - Intelligent News Distribution Platform
Code Implementation Package (Work Package 1)

This package contains the AI agent system that powers automated,
intelligent news distribution across multiple channels.
"""

__version__ = "0.1.0"
__status__ = "Step 1: Foundation Architecture Complete"

from models import (
    DistributionRequest,
    OrchestratorOutput,
    ContentAnalysis,
    ComplianceReport,
    ChannelMix,
    JournalistTargetingResult,
    DistributionResults,
    ROIReport,
    DistributionStatus,
    UrgencyLevel,
    ChannelType,
    IndustryCategory,
    ComplianceRequirement,
)

from base_agent import BaseAgent, MockAgent
from orchestrator_agent import OrchestratorAgent
from config import config, Config

__all__ = [
    # Core Agent Framework
    "BaseAgent",
    "MockAgent",
    "OrchestratorAgent",
    
    # Configuration
    "config",
    "Config",
    
    # Request/Response Models
    "DistributionRequest",
    "OrchestratorOutput",
    "ContentAnalysis",
    "ComplianceReport",
    "ChannelMix",
    "JournalistTargetingResult",
    "DistributionResults",
    "ROIReport",
    
    # Enumerations
    "DistributionStatus",
    "UrgencyLevel",
    "ChannelType",
    "IndustryCategory",
    "ComplianceRequirement",
]
