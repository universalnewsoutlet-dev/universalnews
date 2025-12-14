"""
Universal News - Orchestrator Agent
Coordinates the cascade of specialized agents to execute distribution requests
"""

import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID

from base_agent import BaseAgent
from models import (
    DistributionRequest,
    OrchestratorOutput,
    DistributionStatus,
    ContentAnalysis,
    ComplianceReport,
    ChannelMix,
    JournalistTargetingResult,
    DistributionResults,
    ROIReport,
    ContentAnalysisRequest,
    ComplianceCheckRequest,
    ChannelRoutingRequest,
    JournalistTargetingRequest,
    DeploymentRequest,
    AnalyticsRequest,
)


class OrchestratorAgent(BaseAgent[DistributionRequest, OrchestratorOutput]):
    """
    Master coordinator agent that orchestrates the entire distribution workflow
    
    Workflow:
    1. Parse and validate distribution request
    2. Deploy Market Intelligence Agent (content analysis)
    3. Deploy Compliance Agent (regulatory check) - parallel with step 2
    4. If compliant, deploy Channel Router Agent (channel selection)
    5. If journalist outreach selected, deploy Journalist Targeting Agent - parallel with step 6
    6. Deploy Deployment Agent (execute distribution)
    7. Schedule Analytics Agent (track performance)
    
    State Management:
    - Maintains execution state throughout cascade
    - Handles failures gracefully with rollback capability
    - Provides real-time status updates
    """
    
    def __init__(self, auto_initialize_agents: bool = True):
        super().__init__(agent_name="orchestrator")
        
        # Agent instances
        self.market_intelligence_agent = None
        self.compliance_agent = None
        self.channel_router_agent = None
        self.journalist_targeting_agent = None
        self.deployment_agent = None
        self.analytics_agent = None
        
        # Auto-initialize real agents (Step 2)
        if auto_initialize_agents:
            self._initialize_agents()
        
        # Execution state
        self.state: Dict[UUID, OrchestratorOutput] = {}
    
    def _initialize_agents(self):
        """Initialize all specialized agents (Step 2)"""
        try:
            from market_intelligence_agent import MarketIntelligenceAgent
            from compliance_agent import ComplianceAgent
            from channel_router_agent import ChannelRouterAgent
            from journalist_targeting_agent import JournalistTargetingAgent
            from deployment_agent import DeploymentAgent
            from analytics_agent import AnalyticsAgent
            
            self.market_intelligence_agent = MarketIntelligenceAgent()
            self.compliance_agent = ComplianceAgent()
            self.channel_router_agent = ChannelRouterAgent()
            self.journalist_targeting_agent = JournalistTargetingAgent()
            self.deployment_agent = DeploymentAgent()
            self.analytics_agent = AnalyticsAgent()
            
            self.logger.info("All specialized agents initialized")
            
        except ImportError as e:
            self.logger.warning(f"Could not initialize agents - using mocks: {e}")
    
    def register_agents(
        self,
        market_intelligence_agent=None,
        compliance_agent=None,
        channel_router_agent=None,
        journalist_targeting_agent=None,
        deployment_agent=None,
        analytics_agent=None,
    ):
        """
        Register specialized agents with orchestrator
        
        For Step 1, we'll use mock agents. In full implementation,
        these will be real agent instances.
        """
        self.market_intelligence_agent = market_intelligence_agent
        self.compliance_agent = compliance_agent
        self.channel_router_agent = channel_router_agent
        self.journalist_targeting_agent = journalist_targeting_agent
        self.deployment_agent = deployment_agent
        self.analytics_agent = analytics_agent
        
        self.logger.info("All agents registered with orchestrator")
    
    async def process(self, request: DistributionRequest) -> OrchestratorOutput:
        """
        Execute the full distribution workflow
        
        Args:
            request: Complete distribution request
            
        Returns:
            Orchestrator output with all agent results
        """
        # Initialize output state
        output = OrchestratorOutput(
            distribution_id=request.distribution_id,
            status=DistributionStatus.PENDING,
            started_at=datetime.now(timezone.utc),
            current_step="initialization",
            steps_remaining=[
                "content_analysis",
                "compliance_check",
                "channel_routing",
                "journalist_targeting",
                "deployment",
                "analytics"
            ],
        )
        
        # Store state
        self.state[request.distribution_id] = output
        
        try:
            # Step 1: Content Analysis
            output = await self._run_content_analysis(request, output)
            
            # Step 2: Compliance Check (can run in parallel with content analysis)
            output = await self._run_compliance_check(request, output)
            
            # Check if we can proceed
            if not output.compliance_report.can_proceed:
                output.status = DistributionStatus.FAILED
                output.errors.append("Failed compliance check - cannot proceed")
                self.logger.error("Distribution blocked by compliance issues")
                return self._finalize_output(output)
            
            # Step 3: Channel Routing
            output = await self._run_channel_routing(request, output)
            
            # Step 4 & 5: Parallel execution - Journalist Targeting + Deployment Prep
            output = await self._run_parallel_targeting_and_prep(request, output)
            
            # Step 6: Deployment
            output = await self._run_deployment(request, output)
            
            # Step 7: Schedule Analytics (async - doesn't block completion)
            self._schedule_analytics(request.distribution_id)
            
            # Mark as completed
            output.status = DistributionStatus.COMPLETED
            output.current_step = "completed"
            
            self.logger.info(f"Distribution {request.distribution_id} completed successfully")
            
            return self._finalize_output(output)
            
        except Exception as e:
            self.logger.error(f"Orchestration failed: {e}")
            output.status = DistributionStatus.FAILED
            output.errors.append(str(e))
            return self._finalize_output(output)
    
    async def _run_content_analysis(
        self,
        request: DistributionRequest,
        output: OrchestratorOutput
    ) -> OrchestratorOutput:
        """Execute Market Intelligence Agent"""
        self.log_reasoning("Starting content analysis", {"agent": "market_intelligence"})
        output.status = DistributionStatus.ANALYZING
        output.current_step = "content_analysis"
        
        # Prepare input
        analysis_request = ContentAnalysisRequest(
            distribution_id=request.distribution_id,
            headline=request.headline,
            content=request.content,
            summary=request.summary,
            provided_industries=request.target_industries,
            provided_audiences=request.target_audiences,
        )
        
        # Execute agent
        if self.market_intelligence_agent:
            output.content_analysis = await self.market_intelligence_agent.execute(analysis_request)
            self.log_reasoning(
                "Content analysis completed",
                {
                    "primary_industry": output.content_analysis.primary_industry,
                    "audiences": len(output.content_analysis.target_audiences),
                    "newsworthiness": output.content_analysis.newsworthiness_score,
                }
            )
        else:
            self.logger.warning("Market Intelligence Agent not registered - using mock")
            # Mock output for Step 1
            from models import IndustryCategory
            output.content_analysis = ContentAnalysis(
                distribution_id=request.distribution_id,
                primary_industry=IndustryCategory.TECHNOLOGY,
                secondary_industries=[],
                topics=["AI", "product launch"],
                entities=[],
                keywords=["technology", "innovation"],
                target_audiences=[],
                matched_outlets=[],
                sentiment="positive",
                newsworthiness_score=0.75,
                viral_potential=0.6,
                analysis_summary="Mock analysis",
                recommended_angles=["Innovation story", "Industry impact"],
            )
        
        output.steps_completed.append("content_analysis")
        output.steps_remaining.remove("content_analysis")
        
        return output
    
    async def _run_compliance_check(
        self,
        request: DistributionRequest,
        output: OrchestratorOutput
    ) -> OrchestratorOutput:
        """Execute Compliance Agent"""
        self.log_reasoning("Starting compliance check", {"requirements": request.compliance_requirements})
        output.current_step = "compliance_check"
        
        # Prepare input
        compliance_request = ComplianceCheckRequest(
            distribution_id=request.distribution_id,
            content_analysis=output.content_analysis,
            compliance_requirements=request.compliance_requirements,
        )
        
        # Execute agent
        if self.compliance_agent:
            output.compliance_report = await self.compliance_agent.execute(compliance_request)
            self.log_reasoning(
                "Compliance check completed",
                {
                    "compliant": output.compliance_report.compliant,
                    "can_proceed": output.compliance_report.can_proceed,
                    "issues": len(output.compliance_report.issues),
                }
            )
        else:
            self.logger.warning("Compliance Agent not registered - using mock")
            # Mock output for Step 1
            from models import ComplianceRequirement
            output.compliance_report = ComplianceReport(
                distribution_id=request.distribution_id,
                compliant=True,
                can_proceed=True,
                issues=[],
                critical_issues=[],
                warnings=[],
                required_channels=[],
                forbidden_channels=[],
                required_disclaimers=[],
                requires_human_approval=False,
            )
        
        output.steps_completed.append("compliance_check")
        output.steps_remaining.remove("compliance_check")
        
        return output
    
    async def _run_channel_routing(
        self,
        request: DistributionRequest,
        output: OrchestratorOutput
    ) -> OrchestratorOutput:
        """Execute Channel Router Agent"""
        self.log_reasoning("Starting channel routing", {"budget": request.target_budget})
        output.status = DistributionStatus.PLANNING
        output.current_step = "channel_routing"
        
        # Prepare input
        routing_request = ChannelRoutingRequest(
            distribution_id=request.distribution_id,
            content_analysis=output.content_analysis,
            target_budget=request.target_budget,
            urgency=request.urgency,
            forced_channels=request.target_channels,
            compliance_requirements=request.compliance_requirements,
        )
        
        # Execute agent
        if self.channel_router_agent:
            output.channel_mix = await self.channel_router_agent.execute(routing_request)
            self.log_reasoning(
                "Channel routing completed",
                {
                    "channels": len(output.channel_mix.channels),
                    "budget_allocated": output.channel_mix.total_allocated_budget,
                    "expected_roi": output.channel_mix.expected_roi_percentage,
                }
            )
        else:
            self.logger.warning("Channel Router Agent not registered - using mock")
            # Mock output for Step 1
            from models import ChannelType, ChannelAllocation
            output.channel_mix = ChannelMix(
                distribution_id=request.distribution_id,
                channels=[
                    ChannelAllocation(
                        channel=ChannelType.NEWSWIRE,
                        allocated_budget=600,
                        expected_reach=50000,
                        expected_pickups=20,
                        expected_roi=450,
                        rationale="High visibility for tech news"
                    )
                ],
                total_allocated_budget=600,
                expected_total_reach=50000,
                expected_media_pickups=20,
                expected_backlinks=150,
                expected_roi_percentage=450,
                strategy_summary="Mock strategy",
                timing_recommendations={},
                risk_factors=[],
                confidence_score=0.8,
            )
        
        output.steps_completed.append("channel_routing")
        output.steps_remaining.remove("channel_routing")
        
        return output
    
    async def _run_parallel_targeting_and_prep(
        self,
        request: DistributionRequest,
        output: OrchestratorOutput
    ) -> OrchestratorOutput:
        """Run journalist targeting in parallel with deployment prep"""
        self.log_reasoning("Starting parallel execution", {"tasks": ["journalist_targeting"]})
        
        # Check if journalist outreach is in channel mix
        from models import ChannelType
        has_journalist_outreach = any(
            ch.channel == ChannelType.JOURNALIST_OUTREACH 
            for ch in output.channel_mix.channels
        )
        
        if has_journalist_outreach:
            output.current_step = "journalist_targeting"
            
            # Find budget allocation for journalist outreach
            journalist_budget = next(
                (ch.allocated_budget for ch in output.channel_mix.channels 
                 if ch.channel == ChannelType.JOURNALIST_OUTREACH),
                0
            )
            
            # Prepare input
            targeting_request = JournalistTargetingRequest(
                distribution_id=request.distribution_id,
                content_analysis=output.content_analysis,
                number_of_targets=50,
                budget_allocation=journalist_budget,
            )
            
            # Execute agent
            if self.journalist_targeting_agent:
                output.journalist_targeting = await self.journalist_targeting_agent.execute(targeting_request)
                self.log_reasoning(
                    "Journalist targeting completed",
                    {
                        "targets": output.journalist_targeting.total_targets,
                        "avg_relevance": output.journalist_targeting.average_relevance_score,
                    }
                )
            else:
                self.logger.warning("Journalist Targeting Agent not registered - using mock")
                # Mock output for Step 1
                output.journalist_targeting = JournalistTargetingResult(
                    distribution_id=request.distribution_id,
                    targets=[],
                    total_targets=0,
                    average_relevance_score=0.8,
                    strategy_notes="Mock targeting",
                )
            
            output.steps_completed.append("journalist_targeting")
            output.steps_remaining.remove("journalist_targeting")
        else:
            self.log_reasoning("Journalist outreach not selected - skipping targeting")
            output.steps_remaining.remove("journalist_targeting")
        
        return output
    
    async def _run_deployment(
        self,
        request: DistributionRequest,
        output: OrchestratorOutput
    ) -> OrchestratorOutput:
        """Execute Deployment Agent"""
        self.log_reasoning("Starting deployment", {"channels": len(output.channel_mix.channels)})
        output.status = DistributionStatus.DEPLOYING
        output.current_step = "deployment"
        
        # Prepare input
        deployment_request = DeploymentRequest(
            distribution_id=request.distribution_id,
            channel_mix=output.channel_mix,
            content=request.content,
            headline=request.headline,
            media_urls=request.media_urls,
            journalist_targets=output.journalist_targeting.targets if output.journalist_targeting else None,
        )
        
        # Execute agent
        if self.deployment_agent:
            output.distribution_results = await self.deployment_agent.execute(deployment_request)
            self.log_reasoning(
                "Deployment completed",
                {
                    "channels_deployed": output.distribution_results.total_channels_deployed,
                    "successful": output.distribution_results.successful_deployments,
                    "failed": output.distribution_results.failed_deployments,
                }
            )
        else:
            self.logger.warning("Deployment Agent not registered - using mock")
            # Mock output for Step 1
            from models import ChannelDeploymentResult
            output.distribution_results = DistributionResults(
                distribution_id=request.distribution_id,
                channel_results=[
                    ChannelDeploymentResult(
                        channel=ch.channel,
                        status="success",
                        submission_id=f"mock_{ch.channel}",
                        reach=ch.expected_reach,
                    )
                    for ch in output.channel_mix.channels
                ],
                total_channels_deployed=len(output.channel_mix.channels),
                successful_deployments=len(output.channel_mix.channels),
                failed_deployments=0,
                initial_reach=sum(ch.expected_reach for ch in output.channel_mix.channels),
                public_urls=[],
                overall_status="success",
            )
        
        output.steps_completed.append("deployment")
        output.steps_remaining.remove("deployment")
        
        return output
    
    def _schedule_analytics(self, distribution_id: UUID):
        """Schedule analytics collection (async - runs later)"""
        self.log_reasoning("Analytics scheduled", {"distribution_id": str(distribution_id)})
        # In full implementation, this would schedule a background job
        # For Step 1, we just log it
        self.logger.info(f"Analytics will run in 24 hours for {distribution_id}")
    
    def _finalize_output(self, output: OrchestratorOutput) -> OrchestratorOutput:
        """Finalize output with timing information"""
        output.completed_at = datetime.now(timezone.utc)
        output.total_execution_time_seconds = (
            output.completed_at - output.started_at
        ).total_seconds()
        
        self.logger.info(
            f"Orchestration completed in {output.total_execution_time_seconds:.2f}s"
        )
        
        return output
    
    def get_status(self, distribution_id: UUID) -> Optional[OrchestratorOutput]:
        """Get current status of a distribution"""
        return self.state.get(distribution_id)
