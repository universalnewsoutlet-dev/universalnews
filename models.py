"""
Universal News - Core Data Models
Agent Communication Contracts

These Pydantic models define the contracts between all agents.
They serve as the source of truth for data structures across the platform.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any, Literal
from enum import Enum
from pydantic import BaseModel, Field, validator, HttpUrl
from uuid import UUID, uuid4


# ============================================================================
# ENUMERATIONS
# ============================================================================

class DistributionStatus(str, Enum):
    """Status of a distribution request throughout its lifecycle"""
    DRAFT = "draft"
    PENDING = "pending"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class UrgencyLevel(str, Enum):
    """How quickly the news needs to be distributed"""
    IMMEDIATE = "immediate"  # Within 1 hour
    URGENT = "urgent"        # Within 4 hours
    STANDARD = "standard"    # Within 24 hours
    SCHEDULED = "scheduled"  # At specific time


class ChannelType(str, Enum):
    """Available distribution channels"""
    NEWSWIRE = "newswire"              # PR Newswire, Business Wire, etc.
    JOURNALIST_OUTREACH = "journalist_outreach"  # Direct email to journalists
    SOCIAL_MEDIA = "social_media"      # Twitter, LinkedIn, Facebook
    OWNED_MEDIA = "owned_media"        # Company blog, website
    PAID_MEDIA = "paid_media"          # Sponsored content, ads
    SEO_OPTIMIZATION = "seo_optimization"  # Search engine optimization
    COMMUNITY = "community"            # Reddit, HackerNews, forums


class IndustryCategory(str, Enum):
    """Primary industry categories for news classification"""
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    ENERGY = "energy"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    REAL_ESTATE = "real_estate"
    TELECOMMUNICATIONS = "telecommunications"
    TRANSPORTATION = "transportation"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    GOVERNMENT = "government"
    NONPROFIT = "nonprofit"
    OTHER = "other"


class ComplianceRequirement(str, Enum):
    """Regulatory compliance types"""
    SEC_MATERIAL = "sec_material"      # SEC material disclosure
    GDPR = "gdpr"                      # EU data protection
    FINRA = "finra"                    # Financial industry
    HIPAA = "hipaa"                    # Healthcare privacy
    SOX = "sox"                        # Sarbanes-Oxley
    NONE = "none"                      # No special requirements


# ============================================================================
# INPUT MODELS (What agents receive)
# ============================================================================

class DistributionRequest(BaseModel):
    """
    CONTRACT: Input to Orchestrator Agent
    Represents a complete distribution request from the user
    """
    distribution_id: UUID = Field(default_factory=uuid4)
    organization_id: str = Field(..., description="Organization making the request")
    user_id: str = Field(..., description="User initiating the distribution")
    
    # Content
    headline: str = Field(..., min_length=10, max_length=200)
    content: str = Field(..., min_length=100, description="Full news content (text or HTML)")
    summary: Optional[str] = Field(None, max_length=500, description="Optional summary")
    media_urls: List[HttpUrl] = Field(default_factory=list, description="Images, videos, PDFs")
    
    # Distribution Parameters
    target_budget: float = Field(..., ge=0, description="Budget in USD")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.STANDARD)
    scheduled_time: Optional[datetime] = Field(None, description="For scheduled distributions")
    
    # Targeting (optional - AI will infer if not provided)
    target_industries: Optional[List[IndustryCategory]] = None
    target_audiences: Optional[List[str]] = None  # e.g., ["investors", "consumers", "developers"]
    target_channels: Optional[List[ChannelType]] = None  # Force specific channels
    
    # Compliance
    compliance_requirements: List[ComplianceRequirement] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    idempotency_key: Optional[str] = Field(None, description="For duplicate prevention")
    
    class Config:
        json_schema_extra = {
            "example": {
                "organization_id": "org_abc123",
                "user_id": "user_xyz789",
                "headline": "TechCorp Launches Revolutionary AI Platform",
                "content": "TechCorp today announced the launch of...",
                "target_budget": 1500.00,
                "urgency": "standard",
                "target_industries": ["technology", "finance"],
                "compliance_requirements": ["none"]
            }
        }


class ContentAnalysisRequest(BaseModel):
    """CONTRACT: Input to Market Intelligence Agent"""
    distribution_id: UUID
    headline: str
    content: str
    summary: Optional[str] = None
    provided_industries: Optional[List[IndustryCategory]] = None
    provided_audiences: Optional[List[str]] = None


class ChannelRoutingRequest(BaseModel):
    """CONTRACT: Input to Channel Router Agent"""
    distribution_id: UUID
    content_analysis: 'ContentAnalysis'  # Forward reference
    target_budget: float
    urgency: UrgencyLevel
    forced_channels: Optional[List[ChannelType]] = None
    compliance_requirements: List[ComplianceRequirement]


class JournalistTargetingRequest(BaseModel):
    """CONTRACT: Input to Journalist Targeting Agent"""
    distribution_id: UUID
    content_analysis: 'ContentAnalysis'
    number_of_targets: int = Field(default=50, ge=1, le=500)
    budget_allocation: float = Field(..., description="Budget allocated for this channel")


class DeploymentRequest(BaseModel):
    """CONTRACT: Input to Deployment Agent"""
    distribution_id: UUID
    channel_mix: 'ChannelMix'
    content: str
    headline: str
    media_urls: List[HttpUrl]
    journalist_targets: Optional[List['JournalistTarget']] = None


class AnalyticsRequest(BaseModel):
    """CONTRACT: Input to Analytics Agent"""
    distribution_id: UUID
    hours_since_deployment: int = Field(default=24, description="How long to analyze")


class ComplianceCheckRequest(BaseModel):
    """CONTRACT: Input to Compliance Agent"""
    distribution_id: UUID
    content_analysis: 'ContentAnalysis'
    compliance_requirements: List[ComplianceRequirement]
    channel_mix: Optional['ChannelMix'] = None


# ============================================================================
# OUTPUT MODELS (What agents return)
# ============================================================================

class Entity(BaseModel):
    """Named entity extracted from content"""
    text: str
    type: Literal["PERSON", "ORG", "GPE", "PRODUCT", "EVENT", "LAW", "MONEY"]
    relevance_score: float = Field(ge=0.0, le=1.0)


class AudienceSegment(BaseModel):
    """Identified target audience"""
    name: str  # e.g., "retail investors", "enterprise CTOs"
    relevance_score: float = Field(ge=0.0, le=1.0)
    characteristics: List[str]  # e.g., ["tech-savvy", "budget-conscious"]
    estimated_size: Optional[int] = None


class OutletMatch(BaseModel):
    """Matched media outlet or publication"""
    outlet_name: str
    outlet_type: str  # e.g., "newspaper", "trade publication", "blog"
    relevance_score: float = Field(ge=0.0, le=1.0)
    audience_overlap: float = Field(ge=0.0, le=1.0)
    typical_response_time: Optional[str] = None  # e.g., "2-4 hours"


class ContentAnalysis(BaseModel):
    """
    CONTRACT: Output from Market Intelligence Agent
    Complete analysis of news content
    """
    distribution_id: UUID
    
    # Classification
    primary_industry: IndustryCategory
    secondary_industries: List[IndustryCategory]
    topics: List[str]  # e.g., ["artificial intelligence", "product launch", "funding"]
    
    # Entities
    entities: List[Entity]
    keywords: List[str]  # SEO keywords
    
    # Audience
    target_audiences: List[AudienceSegment]
    
    # Media Targeting
    matched_outlets: List[OutletMatch]
    
    # Metadata
    sentiment: Literal["positive", "neutral", "negative"]
    newsworthiness_score: float = Field(ge=0.0, le=1.0, description="How newsworthy is this?")
    viral_potential: float = Field(ge=0.0, le=1.0)
    
    # AI Reasoning
    analysis_summary: str
    recommended_angles: List[str]  # Different ways to pitch the story
    
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChannelAllocation(BaseModel):
    """Budget allocation for a specific channel"""
    channel: ChannelType
    allocated_budget: float
    expected_reach: int
    expected_pickups: int
    expected_roi: float
    rationale: str  # Why this channel was selected


class ChannelMix(BaseModel):
    """
    CONTRACT: Output from Channel Router Agent
    Optimized selection and allocation of distribution channels
    """
    distribution_id: UUID
    
    # Selected Channels
    channels: List[ChannelAllocation]
    total_allocated_budget: float
    
    # Projections
    expected_total_reach: int
    expected_media_pickups: int
    expected_backlinks: int
    expected_roi_percentage: float
    
    # Strategy
    strategy_summary: str
    timing_recommendations: Dict[ChannelType, str]  # When to deploy each channel
    
    # Risk Assessment
    risk_factors: List[str]
    confidence_score: float = Field(ge=0.0, le=1.0)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JournalistTarget(BaseModel):
    """Individual journalist target with personalized pitch"""
    journalist_id: str
    name: str
    email: str
    outlet: str
    beat: List[str]  # Topics they cover
    relevance_score: float = Field(ge=0.0, le=1.0)
    
    # Personalization
    personalized_subject: str
    personalized_pitch: str
    why_relevant: str  # Explanation of the match
    
    # Historical data (if available)
    past_engagement: Optional[str] = None  # e.g., "opened 3/5 previous pitches"
    response_likelihood: Optional[float] = Field(None, ge=0.0, le=1.0)


class JournalistTargetingResult(BaseModel):
    """
    CONTRACT: Output from Journalist Targeting Agent
    List of targeted journalists with personalized pitches
    """
    distribution_id: UUID
    targets: List[JournalistTarget]
    total_targets: int
    average_relevance_score: float
    strategy_notes: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChannelDeploymentResult(BaseModel):
    """Result of deploying to a single channel"""
    channel: ChannelType
    status: Literal["success", "failed", "partial"]
    submission_id: Optional[str] = None  # External system ID
    url: Optional[HttpUrl] = None  # Public URL if available
    reach: Optional[int] = None  # Actual reach achieved
    error_message: Optional[str] = None
    deployed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DistributionResults(BaseModel):
    """
    CONTRACT: Output from Deployment Agent
    Results of multi-channel distribution execution
    """
    distribution_id: UUID
    
    # Per-channel results
    channel_results: List[ChannelDeploymentResult]
    
    # Summary
    total_channels_deployed: int
    successful_deployments: int
    failed_deployments: int
    
    # Immediate metrics
    initial_reach: int
    public_urls: List[HttpUrl]
    
    # Status
    overall_status: Literal["success", "partial", "failed"]
    error_summary: Optional[str] = None
    
    deployed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MediaPickup(BaseModel):
    """Individual media pickup/mention"""
    outlet_name: str
    url: HttpUrl
    published_at: datetime
    estimated_reach: int
    sentiment: Literal["positive", "neutral", "negative"]
    backlink_quality: float = Field(ge=0.0, le=1.0)


class ROIReport(BaseModel):
    """
    CONTRACT: Output from Analytics Agent
    Performance tracking and ROI calculation
    """
    distribution_id: UUID
    
    # Performance Metrics
    media_pickups: List[MediaPickup]
    total_pickups: int
    total_backlinks: int
    total_reach: int
    
    # Engagement
    social_shares: int
    social_engagement: int
    website_traffic: int
    
    # Financial
    actual_spend: float
    estimated_value: float  # Value of coverage earned
    roi_percentage: float
    cost_per_pickup: float
    
    # Insights
    top_performing_channels: List[ChannelType]
    audience_demographics: Dict[str, Any]
    key_insights: List[str]
    recommendations: List[str]
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    hours_since_deployment: int


class ComplianceIssue(BaseModel):
    """Individual compliance concern"""
    severity: Literal["critical", "warning", "info"]
    requirement: ComplianceRequirement
    issue: str
    recommendation: str


class ComplianceReport(BaseModel):
    """
    CONTRACT: Output from Compliance Agent
    Validation of regulatory requirements
    """
    distribution_id: UUID
    
    # Overall Status
    compliant: bool
    can_proceed: bool
    
    # Issues
    issues: List[ComplianceIssue]
    critical_issues: List[ComplianceIssue]
    warnings: List[ComplianceIssue]
    
    # Requirements
    required_channels: List[ChannelType]  # Must use these channels
    forbidden_channels: List[ChannelType]  # Cannot use these
    required_disclaimers: List[str]
    
    # Approval
    requires_human_approval: bool
    approval_workflow: Optional[str] = None
    
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OrchestratorOutput(BaseModel):
    """
    CONTRACT: Output from Orchestrator Agent
    Final result of the entire distribution process
    """
    distribution_id: UUID
    status: DistributionStatus
    
    # Agent Results (populated as they complete)
    content_analysis: Optional[ContentAnalysis] = None
    compliance_report: Optional[ComplianceReport] = None
    channel_mix: Optional[ChannelMix] = None
    journalist_targeting: Optional[JournalistTargetingResult] = None
    distribution_results: Optional[DistributionResults] = None
    roi_report: Optional[ROIReport] = None
    
    # Execution Metadata
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_execution_time_seconds: Optional[float] = None
    
    # Error Handling
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # State Management
    current_step: str
    steps_completed: List[str] = Field(default_factory=list)
    steps_remaining: List[str] = Field(default_factory=list)


# ============================================================================
# AGENT EXECUTION METADATA
# ============================================================================

class AgentExecutionLog(BaseModel):
    """Logging and observability for agent execution"""
    agent_name: str
    distribution_id: UUID
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    
    # LLM Usage
    llm_calls: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    
    # Decision Trail
    reasoning_steps: List[str] = Field(default_factory=list)
    decisions_made: Dict[str, Any] = Field(default_factory=dict)
    
    # Status
    success: bool = False
    error_message: Optional[str] = None


# Update forward references
ChannelRoutingRequest.model_rebuild()
DeploymentRequest.model_rebuild()
ComplianceCheckRequest.model_rebuild()
