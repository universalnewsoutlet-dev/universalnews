"""
Universal News - Channel Router Agent
Optimizes channel selection and budget allocation for maximum ROI

This agent:
1. Evaluates all available distribution channels
2. Estimates performance for each channel
3. Optimizes budget allocation
4. Forecasts ROI and reach
5. Creates timing recommendations
6. Assesses risks
"""

from typing import List, Dict, Tuple
from datetime import datetime, timezone

from base_agent import BaseAgent
from models import (
    ChannelRoutingRequest,
    ChannelMix,
    ChannelAllocation,
    ChannelType,
    UrgencyLevel,
    IndustryCategory,
)


class ChannelRouterAgent(BaseAgent[ChannelRoutingRequest, ChannelMix]):
    """
    Optimizes channel selection and budget allocation
    
    Capabilities:
    - Channel performance estimation
    - Budget optimization
    - ROI forecasting
    - Timing strategy
    - Risk assessment
    """
    
    def __init__(self):
        super().__init__(agent_name="channel_router")
        
        # Channel performance database (historical data simulation)
        self.channel_performance = self._initialize_channel_data()
    
    def _initialize_channel_data(self) -> Dict:
        """Initialize channel performance data"""
        return {
            ChannelType.NEWSWIRE: {
                'base_cost': 500,
                'reach_per_dollar': 200,  # Reach per $ spent
                'pickup_rate': 0.15,  # % chance of media pickup
                'roi_multiplier': 4.5,
                'industries': [IndustryCategory.TECHNOLOGY, IndustryCategory.FINANCE],
                'urgency_bonus': {UrgencyLevel.IMMEDIATE: 1.3, UrgencyLevel.URGENT: 1.2},
            },
            ChannelType.JOURNALIST_OUTREACH: {
                'base_cost': 300,
                'reach_per_dollar': 150,
                'pickup_rate': 0.25,
                'roi_multiplier': 5.0,
                'industries': 'all',
                'urgency_bonus': {UrgencyLevel.IMMEDIATE: 1.1, UrgencyLevel.URGENT: 1.0},
            },
            ChannelType.SOCIAL_MEDIA: {
                'base_cost': 0,  # Organic
                'reach_per_dollar': 500,  # Very high organic reach
                'pickup_rate': 0.05,
                'roi_multiplier': 3.0,
                'industries': [IndustryCategory.TECHNOLOGY, IndustryCategory.RETAIL],
                'urgency_bonus': {UrgencyLevel.IMMEDIATE: 1.5, UrgencyLevel.URGENT: 1.3},
            },
            ChannelType.OWNED_MEDIA: {
                'base_cost': 0,
                'reach_per_dollar': 300,
                'pickup_rate': 0.02,
                'roi_multiplier': 2.0,
                'industries': 'all',
                'urgency_bonus': {},
            },
            ChannelType.PAID_MEDIA: {
                'base_cost': 1000,
                'reach_per_dollar': 100,
                'pickup_rate': 0.08,
                'roi_multiplier': 3.5,
                'industries': [IndustryCategory.RETAIL, IndustryCategory.FINANCE],
                'urgency_bonus': {UrgencyLevel.IMMEDIATE: 1.2},
            },
            ChannelType.SEO_OPTIMIZATION: {
                'base_cost': 200,
                'reach_per_dollar': 400,  # Long-term value
                'pickup_rate': 0.10,
                'roi_multiplier': 6.0,  # High long-term ROI
                'industries': 'all',
                'urgency_bonus': {},
            },
            ChannelType.COMMUNITY: {
                'base_cost': 0,
                'reach_per_dollar': 250,
                'pickup_rate': 0.12,
                'roi_multiplier': 4.0,
                'industries': [IndustryCategory.TECHNOLOGY],
                'urgency_bonus': {UrgencyLevel.IMMEDIATE: 1.4},
            },
        }
    
    async def process(self, request: ChannelRoutingRequest) -> ChannelMix:
        """
        Optimize channel selection and budget allocation
        
        Args:
            request: Channel routing request
            
        Returns:
            Optimized channel mix with allocations
        """
        self.log_reasoning("Starting channel routing", {
            "budget": request.target_budget,
            "urgency": request.urgency.value,
            "industry": request.content_analysis.primary_industry.value,
        })
        
        # Step 1: Filter channels based on compliance
        available_channels = self._filter_channels_by_compliance(
            request.compliance_requirements,
            request.forced_channels
        )
        self.log_reasoning(f"Available channels after compliance: {[ch.value for ch in available_channels]}")
        
        # Step 2: Score each channel
        channel_scores = await self._score_channels(
            available_channels,
            request.content_analysis,
            request.urgency,
            request.target_budget
        )
        self.log_reasoning(f"Channel scores calculated for {len(channel_scores)} channels")
        
        # Step 3: Optimize budget allocation
        allocations = await self._optimize_budget_allocation(
            channel_scores,
            request.target_budget,
            request.urgency
        )
        self.log_reasoning(f"Budget allocated across {len(allocations)} channels")
        
        # Step 4: Calculate projections
        projections = self._calculate_projections(allocations)
        
        # Step 5: Generate strategy summary
        strategy = await self._generate_strategy(
            allocations,
            request.content_analysis,
            request.urgency
        )
        
        # Step 6: Create timing recommendations
        timing = self._create_timing_recommendations(allocations, request.urgency)
        
        # Step 7: Assess risks
        risks = self._assess_risks(allocations, request.content_analysis)
        
        # Step 8: Calculate confidence
        confidence = self._calculate_confidence(allocations, request.content_analysis)
        
        return ChannelMix(
            distribution_id=request.distribution_id,
            channels=allocations,
            total_allocated_budget=sum(ch.allocated_budget for ch in allocations),
            expected_total_reach=projections['reach'],
            expected_media_pickups=projections['pickups'],
            expected_backlinks=projections['backlinks'],
            expected_roi_percentage=projections['roi_percentage'],
            strategy_summary=strategy,
            timing_recommendations=timing,
            risk_factors=risks,
            confidence_score=confidence,
            created_at=datetime.now(timezone.utc),
        )
    
    def _filter_channels_by_compliance(
        self,
        compliance_requirements: List,
        forced_channels: List[ChannelType] = None
    ) -> List[ChannelType]:
        """Filter channels based on compliance and user preferences"""
        
        # Start with all channels
        available = list(ChannelType)
        
        # If specific channels forced, use only those
        if forced_channels:
            return forced_channels
        
        # In production, would filter based on compliance rules
        # For now, return all channels
        return available
    
    async def _score_channels(
        self,
        channels: List[ChannelType],
        content_analysis,
        urgency: UrgencyLevel,
        budget: float
    ) -> List[Tuple[ChannelType, float, Dict]]:
        """Score each channel for this content"""
        
        scores = []
        
        for channel in channels:
            perf = self.channel_performance.get(channel)
            if not perf:
                continue
            
            # Base score starts at 0.5
            score = 0.5
            
            # Industry fit
            if perf['industries'] == 'all' or content_analysis.primary_industry in perf['industries']:
                score += 0.2
            
            # Urgency bonus
            urgency_mult = perf['urgency_bonus'].get(urgency, 1.0)
            if urgency_mult > 1.0:
                score += 0.1 * (urgency_mult - 1.0)
            
            # Newsworthiness fit
            if content_analysis.newsworthiness_score > 0.7:
                if channel in [ChannelType.NEWSWIRE, ChannelType.JOURNALIST_OUTREACH]:
                    score += 0.15
            
            # Viral potential fit
            if content_analysis.viral_potential > 0.7:
                if channel in [ChannelType.SOCIAL_MEDIA, ChannelType.COMMUNITY]:
                    score += 0.15
            
            # Cost effectiveness
            if perf['base_cost'] == 0:  # Free channels
                score += 0.1
            elif perf['base_cost'] < budget * 0.3:  # Affordable
                score += 0.05
            
            # Cap at 1.0
            score = min(1.0, score)
            
            scores.append((channel, score, perf))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores
    
    async def _optimize_budget_allocation(
        self,
        channel_scores: List[Tuple[ChannelType, float, Dict]],
        total_budget: float,
        urgency: UrgencyLevel
    ) -> List[ChannelAllocation]:
        """Optimize budget allocation using LLM-guided strategy"""
        
        # Build channel options for LLM
        channel_options = []
        for channel, score, perf in channel_scores[:7]:  # Top 7 channels
            channel_options.append({
                'channel': channel.value,
                'score': round(score, 2),
                'base_cost': perf['base_cost'],
                'roi_multiplier': perf['roi_multiplier'],
                'reach_per_dollar': perf['reach_per_dollar'],
            })
        
        prompt = f"""Optimize budget allocation for news distribution.

Total Budget: ${total_budget}
Urgency: {urgency.value}

Available Channels:
{self._format_channels_for_llm(channel_options)}

Guidelines:
1. Allocate to 2-4 channels (don't spread too thin)
2. Prioritize higher-scoring channels
3. Always include at least one major channel (newswire or journalist outreach)
4. Free channels (cost=0) should always be included
5. Spend at least 70% of budget

Return JSON:
{{
    "allocations": [
        {{
            "channel": "newswire",
            "budget": 600,
            "reasoning": "High newsworthiness justifies premium channel"
        }}
    ],
    "strategy": "Overall strategy explanation"
}}"""

        try:
            response = await self.call_llm_json(prompt)
            
            allocations = []
            for alloc in response.get('allocations', []):
                try:
                    channel = ChannelType(alloc['channel'])
                    budget = float(alloc['budget'])
                    
                    # Find performance data
                    perf = next((p for ch, s, p in channel_scores if ch == channel), None)
                    if not perf:
                        continue
                    
                    # Calculate metrics
                    expected_reach = int(budget * perf['reach_per_dollar'])
                    expected_pickups = int(expected_reach * perf['pickup_rate'])
                    expected_roi = perf['roi_multiplier'] * 100
                    
                    allocations.append(ChannelAllocation(
                        channel=channel,
                        allocated_budget=budget,
                        expected_reach=expected_reach,
                        expected_pickups=expected_pickups,
                        expected_roi=expected_roi,
                        rationale=alloc.get('reasoning', 'LLM recommendation')
                    ))
                    
                except Exception as e:
                    self.logger.warning(f"Skipping allocation: {e}")
                    continue
            
            return allocations if allocations else self._fallback_allocation(channel_scores, total_budget)
            
        except Exception as e:
            self.logger.warning(f"LLM allocation failed, using fallback: {e}")
            return self._fallback_allocation(channel_scores, total_budget)
    
    def _format_channels_for_llm(self, channel_options: List[Dict]) -> str:
        """Format channel options for LLM prompt"""
        lines = []
        for opt in channel_options:
            lines.append(
                f"- {opt['channel']}: Score {opt['score']}, "
                f"Cost ${opt['base_cost']}, "
                f"ROI {opt['roi_multiplier']}x, "
                f"Reach {opt['reach_per_dollar']}/dollar"
            )
        return '\n'.join(lines)
    
    def _fallback_allocation(
        self,
        channel_scores: List[Tuple[ChannelType, float, Dict]],
        total_budget: float
    ) -> List[ChannelAllocation]:
        """Fallback allocation strategy"""
        
        allocations = []
        remaining_budget = total_budget
        
        # Always include top 2 scored channels
        for channel, score, perf in channel_scores[:3]:
            if remaining_budget <= 0:
                break
            
            # Allocate proportional to score
            if perf['base_cost'] == 0:
                # Free channel - always include
                budget = 0
            else:
                budget = min(
                    perf['base_cost'] + (remaining_budget * 0.3),
                    remaining_budget
                )
            
            expected_reach = int(budget * perf['reach_per_dollar']) if budget > 0 else 10000
            expected_pickups = int(expected_reach * perf['pickup_rate'])
            expected_roi = perf['roi_multiplier'] * 100
            
            allocations.append(ChannelAllocation(
                channel=channel,
                allocated_budget=budget,
                expected_reach=expected_reach,
                expected_pickups=expected_pickups,
                expected_roi=expected_roi,
                rationale=f"Score: {score:.2f} - {channel.value} recommended"
            ))
            
            remaining_budget -= budget
        
        return allocations
    
    def _calculate_projections(self, allocations: List[ChannelAllocation]) -> Dict:
        """Calculate overall projections"""
        
        total_reach = sum(ch.expected_reach for ch in allocations)
        total_pickups = sum(ch.expected_pickups for ch in allocations)
        total_budget = sum(ch.allocated_budget for ch in allocations)
        
        # Backlinks estimation (rough heuristic)
        backlinks = total_pickups * 8  # ~8 backlinks per pickup
        
        # ROI calculation
        avg_pickup_value = 1500  # Average media pickup value
        estimated_value = total_pickups * avg_pickup_value
        roi_percentage = ((estimated_value - total_budget) / total_budget * 100) if total_budget > 0 else 0
        
        return {
            'reach': total_reach,
            'pickups': total_pickups,
            'backlinks': backlinks,
            'roi_percentage': roi_percentage,
        }
    
    async def _generate_strategy(
        self,
        allocations: List[ChannelAllocation],
        content_analysis,
        urgency: UrgencyLevel
    ) -> str:
        """Generate strategy summary"""
        
        channels_desc = ", ".join([f"{ch.channel.value} (${ch.allocated_budget:.0f})" for ch in allocations])
        
        strategy = f"Multi-channel distribution strategy leveraging {len(allocations)} channels: {channels_desc}. "
        strategy += f"Optimized for {content_analysis.primary_industry.value} industry with {urgency.value} urgency. "
        strategy += f"Expected to reach {sum(ch.expected_reach for ch in allocations):,} people "
        strategy += f"with {sum(ch.expected_pickups for ch in allocations)} media pickups."
        
        return strategy
    
    def _create_timing_recommendations(
        self,
        allocations: List[ChannelAllocation],
        urgency: UrgencyLevel
    ) -> Dict[ChannelType, str]:
        """Create timing recommendations for each channel"""
        
        timing = {}
        
        if urgency in [UrgencyLevel.IMMEDIATE, UrgencyLevel.URGENT]:
            # Deploy all immediately
            for alloc in allocations:
                timing[alloc.channel] = "Deploy immediately"
        else:
            # Stagger deployment
            for i, alloc in enumerate(allocations):
                if i == 0:
                    timing[alloc.channel] = "Deploy first (T+0)"
                elif i == 1:
                    timing[alloc.channel] = "Deploy after 2 hours (T+2h)"
                else:
                    timing[alloc.channel] = "Deploy after 4 hours (T+4h)"
        
        return timing
    
    def _assess_risks(
        self,
        allocations: List[ChannelAllocation],
        content_analysis
    ) -> List[str]:
        """Assess risks with this channel mix"""
        
        risks = []
        
        total_budget = sum(ch.allocated_budget for ch in allocations)
        
        # Budget concentration risk
        if len(allocations) == 1:
            risks.append("Single channel dependency - no redundancy")
        
        # High spend risk
        if total_budget > 2000:
            risks.append("High budget allocation - ensure content quality justifies spend")
        
        # Low newsworthiness with expensive channels
        if content_analysis.newsworthiness_score < 0.5:
            expensive_channels = [ch for ch in allocations if ch.allocated_budget > 500]
            if expensive_channels:
                risks.append("Low newsworthiness score with premium channels - may underperform")
        
        return risks if risks else ["No significant risks identified"]
    
    def _calculate_confidence(
        self,
        allocations: List[ChannelAllocation],
        content_analysis
    ) -> float:
        """Calculate confidence in this strategy"""
        
        confidence = 0.7  # Base confidence
        
        # Boost for multiple channels
        if len(allocations) >= 3:
            confidence += 0.1
        
        # Boost for high newsworthiness
        if content_analysis.newsworthiness_score > 0.7:
            confidence += 0.1
        
        # Reduce for low newsworthiness
        if content_analysis.newsworthiness_score < 0.4:
            confidence -= 0.2
        
        return min(1.0, max(0.3, confidence))
