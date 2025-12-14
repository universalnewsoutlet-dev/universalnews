"""
Universal News - Journalist Targeting Agent
Identifies and targets relevant journalists with personalized pitches

This agent:
1. Discovers journalists based on beat/topics
2. Scores relevance to the news content
3. Generates personalized email subjects
4. Creates customized pitch emails
5. Predicts response likelihood
"""

from typing import List, Dict, Tuple
from datetime import datetime, timezone
import random

from base_agent import BaseAgent
from models import (
    JournalistTargetingRequest,
    JournalistTargetingResult,
    JournalistTarget,
    IndustryCategory,
)


class JournalistTargetingAgent(BaseAgent[JournalistTargetingRequest, JournalistTargetingResult]):
    """
    Targets journalists with personalized pitches
    
    Capabilities:
    - Journalist discovery by beat/topic
    - Relevance scoring
    - Personalized subject line generation
    - Custom pitch creation
    - Response prediction
    """
    
    def __init__(self):
        super().__init__(agent_name="journalist_targeting")
        
        # Simulated journalist database (in production, would use Meltwater/Cision API)
        self.journalist_database = self._initialize_journalist_database()
    
    def _initialize_journalist_database(self) -> List[Dict]:
        """Initialize journalist database (mock data)"""
        
        # In production, this would query external journalist databases
        # For now, we'll create realistic mock data
        
        journalists = [
            {
                'id': 'j001',
                'name': 'Sarah Chen',
                'email': 'schen@techcrunch.com',
                'outlet': 'TechCrunch',
                'beat': ['artificial intelligence', 'machine learning', 'startups', 'enterprise software'],
                'industries': [IndustryCategory.TECHNOLOGY],
                'engagement_rate': 0.35,
            },
            {
                'id': 'j002',
                'name': 'Michael Rodriguez',
                'email': 'mrodriguez@bloomberg.com',
                'outlet': 'Bloomberg',
                'beat': ['finance', 'venture capital', 'ipos', 'markets'],
                'industries': [IndustryCategory.FINANCE, IndustryCategory.TECHNOLOGY],
                'engagement_rate': 0.28,
            },
            {
                'id': 'j003',
                'name': 'Emily Watson',
                'email': 'ewatson@theverge.com',
                'outlet': 'The Verge',
                'beat': ['consumer tech', 'ai', 'product launches', 'reviews'],
                'industries': [IndustryCategory.TECHNOLOGY],
                'engagement_rate': 0.42,
            },
            {
                'id': 'j004',
                'name': 'David Kim',
                'email': 'dkim@wsj.com',
                'outlet': 'Wall Street Journal',
                'beat': ['enterprise', 'cloud computing', 'cybersecurity', 'business technology'],
                'industries': [IndustryCategory.TECHNOLOGY, IndustryCategory.FINANCE],
                'engagement_rate': 0.31,
            },
            {
                'id': 'j005',
                'name': 'Jessica Martinez',
                'email': 'jmartinez@forbes.com',
                'outlet': 'Forbes',
                'beat': ['startups', 'entrepreneurship', 'funding', 'innovation'],
                'industries': [IndustryCategory.TECHNOLOGY, IndustryCategory.FINANCE],
                'engagement_rate': 0.38,
            },
            {
                'id': 'j006',
                'name': 'Robert Thompson',
                'email': 'rthompson@reuters.com',
                'outlet': 'Reuters',
                'beat': ['breaking news', 'technology', 'corporate', 'announcements'],
                'industries': [IndustryCategory.TECHNOLOGY],
                'engagement_rate': 0.25,
            },
            {
                'id': 'j007',
                'name': 'Amanda Foster',
                'email': 'afoster@wired.com',
                'outlet': 'Wired',
                'beat': ['emerging tech', 'ai ethics', 'future of work', 'digital transformation'],
                'industries': [IndustryCategory.TECHNOLOGY],
                'engagement_rate': 0.33,
            },
            {
                'id': 'j008',
                'name': 'James Wilson',
                'email': 'jwilson@ft.com',
                'outlet': 'Financial Times',
                'beat': ['fintech', 'banking', 'payments', 'financial services'],
                'industries': [IndustryCategory.FINANCE],
                'engagement_rate': 0.29,
            },
            {
                'id': 'j009',
                'name': 'Lisa Anderson',
                'email': 'landerson@businessinsider.com',
                'outlet': 'Business Insider',
                'beat': ['tech industry', 'startups', 'leadership', 'strategy'],
                'industries': [IndustryCategory.TECHNOLOGY, IndustryCategory.FINANCE],
                'engagement_rate': 0.36,
            },
            {
                'id': 'j010',
                'name': 'Christopher Lee',
                'email': 'clee@zdnet.com',
                'outlet': 'ZDNet',
                'beat': ['enterprise tech', 'cloud', 'saas', 'it infrastructure'],
                'industries': [IndustryCategory.TECHNOLOGY],
                'engagement_rate': 0.27,
            },
        ]
        
        # Generate more journalists programmatically
        for i in range(11, 101):
            journalists.append({
                'id': f'j{i:03d}',
                'name': f'Journalist {i}',
                'email': f'journalist{i}@newsoutlet.com',
                'outlet': random.choice(['TechInsider', 'NewsWire', 'Industry Daily']),
                'beat': random.sample(['technology', 'business', 'innovation', 'startups'], k=2),
                'industries': [random.choice(list(IndustryCategory))],
                'engagement_rate': round(random.uniform(0.15, 0.45), 2),
            })
        
        return journalists
    
    async def process(self, request: JournalistTargetingRequest) -> JournalistTargetingResult:
        """
        Target journalists with personalized pitches
        
        Args:
            request: Journalist targeting request
            
        Returns:
            List of targeted journalists with personalized pitches
        """
        self.log_reasoning("Starting journalist targeting", {
            "target_count": request.number_of_targets,
            "budget": request.budget_allocation,
            "industry": request.content_analysis.primary_industry.value,
        })
        
        # Step 1: Discover relevant journalists
        candidates = self._discover_journalists(request.content_analysis)
        self.log_reasoning(f"Discovered {len(candidates)} candidate journalists")
        
        # Step 2: Score relevance
        scored_candidates = await self._score_relevance(
            candidates,
            request.content_analysis
        )
        self.log_reasoning(f"Scored {len(scored_candidates)} journalists")
        
        # Step 3: Select top N targets
        selected = self._select_targets(
            scored_candidates,
            request.number_of_targets,
            request.budget_allocation
        )
        self.log_reasoning(f"Selected {len(selected)} target journalists")
        
        # Step 4: Generate personalized pitches
        targets = await self._generate_pitches(
            selected,
            request.content_analysis
        )
        self.log_reasoning(f"Generated personalized pitches for {len(targets)} journalists")
        
        # Step 5: Calculate average relevance
        avg_relevance = sum(t.relevance_score for t in targets) / len(targets) if targets else 0.0
        
        # Step 6: Generate strategy notes
        strategy_notes = self._generate_strategy_notes(targets, request.content_analysis)
        
        return JournalistTargetingResult(
            distribution_id=request.distribution_id,
            targets=targets,
            total_targets=len(targets),
            average_relevance_score=avg_relevance,
            strategy_notes=strategy_notes,
            created_at=datetime.now(timezone.utc),
        )
    
    def _discover_journalists(self, content_analysis) -> List[Dict]:
        """Discover journalists matching the content"""
        
        candidates = []
        
        for journalist in self.journalist_database:
            # Filter by industry
            if content_analysis.primary_industry not in journalist['industries']:
                continue
            
            # Check beat overlap with topics
            beat_overlap = any(
                topic.lower() in ' '.join(journalist['beat']).lower()
                for topic in content_analysis.topics
            )
            
            if beat_overlap or len(candidates) < 50:  # Ensure minimum candidates
                candidates.append(journalist)
        
        return candidates
    
    async def _score_relevance(
        self,
        candidates: List[Dict],
        content_analysis
    ) -> List[Tuple[Dict, float]]:
        """Score each journalist's relevance"""
        
        scored = []
        
        for journalist in candidates:
            score = 0.5  # Base score
            
            # Industry match
            if content_analysis.primary_industry in journalist['industries']:
                score += 0.2
            
            # Beat/topic overlap
            beat_text = ' '.join(journalist['beat']).lower()
            topic_matches = sum(
                1 for topic in content_analysis.topics
                if topic.lower() in beat_text
            )
            score += min(0.3, topic_matches * 0.1)
            
            # Historical engagement
            score += journalist['engagement_rate'] * 0.2
            
            # Cap at 1.0
            score = min(1.0, score)
            
            scored.append((journalist, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return scored
    
    def _select_targets(
        self,
        scored_candidates: List[Tuple[Dict, float]],
        target_count: int,
        budget: float
    ) -> List[Tuple[Dict, float]]:
        """Select top N journalists within budget"""
        
        # Cost per journalist outreach (email infrastructure, tracking, etc.)
        cost_per_journalist = 6.0  # $6 per personalized outreach
        
        max_affordable = int(budget / cost_per_journalist) if budget > 0 else target_count
        
        # Select min of requested count or affordable count
        actual_count = min(target_count, max_affordable, len(scored_candidates))
        
        return scored_candidates[:actual_count]
    
    async def _generate_pitches(
        self,
        selected: List[Tuple[Dict, float]],
        content_analysis
    ) -> List[JournalistTarget]:
        """Generate personalized pitches for each journalist"""
        
        targets = []
        
        # Prepare content summary for LLM
        content_summary = {
            'industry': content_analysis.primary_industry.value,
            'topics': content_analysis.topics[:5],
            'sentiment': content_analysis.sentiment,
            'newsworthiness': content_analysis.newsworthiness_score,
            'summary': content_analysis.analysis_summary,
        }
        
        # Generate pitches in batch (for efficiency, we'll do 3 at a time)
        batch_size = 3
        for i in range(0, len(selected), batch_size):
            batch = selected[i:i+batch_size]
            
            try:
                batch_targets = await self._generate_pitch_batch(batch, content_summary)
                targets.extend(batch_targets)
            except Exception as e:
                self.logger.warning(f"Batch pitch generation failed: {e}")
                # Fallback to simple pitches
                for journalist, score in batch:
                    targets.append(self._generate_simple_pitch(journalist, score, content_analysis))
        
        return targets
    
    async def _generate_pitch_batch(
        self,
        batch: List[Tuple[Dict, float]],
        content_summary: Dict
    ) -> List[JournalistTarget]:
        """Generate pitches for a batch of journalists using LLM"""
        
        # Build journalist profiles
        journalist_profiles = []
        for journalist, score in batch:
            journalist_profiles.append({
                'name': journalist['name'],
                'outlet': journalist['outlet'],
                'beat': journalist['beat'],
            })
        
        prompt = f"""Generate personalized email pitches for these journalists.

News Content:
- Industry: {content_summary['industry']}
- Topics: {', '.join(content_summary['topics'])}
- Summary: {content_summary['summary']}
- Newsworthiness: {content_summary['newsworthiness']:.2f}

Journalists:
{self._format_journalists_for_llm(journalist_profiles)}

For each journalist, generate:
1. Personalized subject line (8-12 words, compelling)
2. Email pitch (2-3 paragraphs, professional)
3. Why this story is relevant to their beat

Return JSON:
{{
    "pitches": [
        {{
            "journalist_name": "Name",
            "subject": "Subject line",
            "pitch": "Email body",
            "relevance_explanation": "Why relevant"
        }}
    ]
}}"""

        try:
            response = await self.call_llm_json(prompt)
            
            targets = []
            pitches_data = response.get('pitches', [])
            
            for (journalist, score), pitch_data in zip(batch, pitches_data):
                targets.append(JournalistTarget(
                    journalist_id=journalist['id'],
                    name=journalist['name'],
                    email=journalist['email'],
                    outlet=journalist['outlet'],
                    beat=journalist['beat'],
                    relevance_score=score,
                    personalized_subject=pitch_data.get('subject', 'Breaking Industry News'),
                    personalized_pitch=pitch_data.get('pitch', ''),
                    why_relevant=pitch_data.get('relevance_explanation', ''),
                    past_engagement=f"Opened {int(journalist['engagement_rate']*10)}/10 previous emails",
                    response_likelihood=journalist['engagement_rate'],
                ))
            
            return targets
            
        except Exception as e:
            self.logger.warning(f"LLM pitch generation failed: {e}")
            raise
    
    def _format_journalists_for_llm(self, profiles: List[Dict]) -> str:
        """Format journalist profiles for LLM"""
        lines = []
        for prof in profiles:
            lines.append(f"- {prof['name']} at {prof['outlet']}: Covers {', '.join(prof['beat'][:3])}")
        return '\n'.join(lines)
    
    def _generate_simple_pitch(
        self,
        journalist: Dict,
        score: float,
        content_analysis
    ) -> JournalistTarget:
        """Generate simple pitch (fallback)"""
        
        subject = f"Story Opportunity: {content_analysis.primary_industry.value.title()} - {content_analysis.topics[0] if content_analysis.topics else 'Update'}"
        
        pitch = f"""Hi {journalist['name']},

I wanted to share a story that aligns with your coverage of {', '.join(journalist['beat'][:2])}.

{content_analysis.analysis_summary}

I think this would resonate with {journalist['outlet']}'s audience. Would you be interested in learning more?

Best regards"""
        
        why_relevant = f"Matches {journalist['name']}'s beat: {', '.join(journalist['beat'][:2])}"
        
        return JournalistTarget(
            journalist_id=journalist['id'],
            name=journalist['name'],
            email=journalist['email'],
            outlet=journalist['outlet'],
            beat=journalist['beat'],
            relevance_score=score,
            personalized_subject=subject,
            personalized_pitch=pitch,
            why_relevant=why_relevant,
            past_engagement=f"Engagement rate: {journalist['engagement_rate']:.0%}",
            response_likelihood=journalist['engagement_rate'],
        )
    
    def _generate_strategy_notes(
        self,
        targets: List[JournalistTarget],
        content_analysis
    ) -> str:
        """Generate strategy notes for journalist outreach"""
        
        if not targets:
            return "No journalists targeted"
        
        top_outlets = list(set([t.outlet for t in targets[:10]]))
        avg_response = sum(t.response_likelihood or 0 for t in targets) / len(targets)
        
        notes = f"Targeting {len(targets)} journalists across {len(top_outlets)} top outlets including {', '.join(top_outlets[:5])}. "
        notes += f"Average response likelihood: {avg_response:.0%}. "
        notes += f"Strategy: Personalized outreach emphasizing {content_analysis.primary_industry.value} relevance. "
        notes += f"Expected {int(len(targets) * avg_response)} responses based on historical engagement."
        
        return notes
