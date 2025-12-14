"""
Universal News - Market Intelligence Agent
Analyzes news content to identify industries, topics, audiences, and media outlets

This agent uses LLM-powered analysis to:
1. Classify content by industry and topics
2. Extract named entities and keywords
3. Identify target audience segments
4. Match relevant media outlets
5. Assess newsworthiness and viral potential
"""

import json
import re
from typing import List, Dict, Any
from datetime import datetime, timezone

from base_agent import BaseAgent
from models import (
    ContentAnalysisRequest,
    ContentAnalysis,
    IndustryCategory,
    Entity,
    AudienceSegment,
    OutletMatch,
)


class MarketIntelligenceAgent(BaseAgent[ContentAnalysisRequest, ContentAnalysis]):
    """
    Analyzes news content to extract actionable intelligence for distribution
    
    Capabilities:
    - Industry classification (primary + secondary)
    - Topic extraction and categorization
    - Named entity recognition
    - SEO keyword identification
    - Target audience profiling
    - Media outlet matching
    - Sentiment analysis
    - Newsworthiness scoring
    - Viral potential assessment
    """
    
    def __init__(self):
        super().__init__(agent_name="market_intelligence")
        
        # Industry keywords for classification assistance
        self.industry_keywords = {
            IndustryCategory.TECHNOLOGY: [
                "ai", "artificial intelligence", "software", "app", "platform",
                "cloud", "saas", "tech", "digital", "algorithm", "data",
                "machine learning", "automation", "api", "developer"
            ],
            IndustryCategory.FINANCE: [
                "investment", "funding", "revenue", "profit", "bank",
                "financial", "capital", "investor", "stock", "market",
                "fintech", "payment", "loan", "credit", "trading"
            ],
            IndustryCategory.HEALTHCARE: [
                "health", "medical", "patient", "hospital", "clinic",
                "pharmaceutical", "drug", "biotech", "therapy", "diagnosis",
                "healthcare", "medicine", "disease", "treatment"
            ],
            IndustryCategory.ENERGY: [
                "energy", "power", "electricity", "solar", "renewable",
                "oil", "gas", "battery", "grid", "utilities", "fuel"
            ],
            IndustryCategory.RETAIL: [
                "retail", "store", "shopping", "consumer", "ecommerce",
                "merchandise", "brand", "product", "sales", "customer"
            ],
        }
        
        # Common media outlets by category
        self.media_outlets = {
            "technology": [
                "TechCrunch", "The Verge", "Ars Technica", "Wired", "VentureBeat",
                "TechRadar", "Engadget", "ZDNet", "CNET", "Gizmodo"
            ],
            "business": [
                "Wall Street Journal", "Bloomberg", "Forbes", "Fortune", "Reuters",
                "Financial Times", "Business Insider", "CNBC", "MarketWatch"
            ],
            "general": [
                "Associated Press", "Reuters", "CNN", "BBC", "The New York Times",
                "Washington Post", "USA Today", "The Guardian"
            ],
        }
    
    async def process(self, request: ContentAnalysisRequest) -> ContentAnalysis:
        """
        Analyze news content and extract intelligence
        
        Args:
            request: Content analysis request with headline and content
            
        Returns:
            Complete content analysis with classifications and insights
        """
        self.log_reasoning("Starting content analysis", {
            "headline_length": len(request.headline),
            "content_length": len(request.content),
        })
        
        # Step 1: Industry Classification
        industries = await self._classify_industries(
            request.headline,
            request.content,
            request.provided_industries
        )
        self.log_reasoning(f"Industries identified: {industries['primary']}, {industries['secondary']}")
        
        # Step 2: Topic Extraction
        topics = await self._extract_topics(request.headline, request.content)
        self.log_reasoning(f"Topics extracted: {topics}")
        
        # Step 3: Entity Recognition
        entities = await self._extract_entities(request.content)
        self.log_reasoning(f"Entities found: {len(entities)}")
        
        # Step 4: Keyword Extraction
        keywords = await self._extract_keywords(request.headline, request.content, topics)
        self.log_reasoning(f"Keywords: {keywords}")
        
        # Step 5: Audience Identification
        audiences = await self._identify_audiences(
            industries['primary'],
            topics,
            request.content,
            request.provided_audiences
        )
        self.log_reasoning(f"Audiences identified: {len(audiences)}")
        
        # Step 6: Outlet Matching
        outlets = await self._match_outlets(industries['primary'], topics)
        self.log_reasoning(f"Outlets matched: {len(outlets)}")
        
        # Step 7: Sentiment Analysis
        sentiment = await self._analyze_sentiment(request.headline, request.content)
        self.log_reasoning(f"Sentiment: {sentiment}")
        
        # Step 8: Scoring
        scores = await self._calculate_scores(
            request.headline,
            request.content,
            industries['primary'],
            topics,
            entities
        )
        self.log_reasoning(f"Scores - Newsworthiness: {scores['newsworthiness']}, Viral: {scores['viral']}")
        
        # Step 9: Recommended Angles
        angles = await self._generate_angles(industries['primary'], topics, audiences)
        self.log_reasoning(f"Story angles: {len(angles)}")
        
        # Step 10: Analysis Summary
        summary = await self._generate_summary(industries, topics, audiences, scores)
        
        # Compile results
        return ContentAnalysis(
            distribution_id=request.distribution_id,
            primary_industry=industries['primary'],
            secondary_industries=industries['secondary'],
            topics=topics,
            entities=entities,
            keywords=keywords,
            target_audiences=audiences,
            matched_outlets=outlets,
            sentiment=sentiment,
            newsworthiness_score=scores['newsworthiness'],
            viral_potential=scores['viral'],
            analysis_summary=summary,
            recommended_angles=angles,
            processed_at=datetime.now(timezone.utc),
        )
    
    async def _classify_industries(
        self,
        headline: str,
        content: str,
        provided_industries: List[IndustryCategory] = None
    ) -> Dict[str, Any]:
        """Classify content by industry using LLM and keyword analysis"""
        
        # If industries provided, validate and use them
        if provided_industries:
            return {
                'primary': provided_industries[0],
                'secondary': provided_industries[1:] if len(provided_industries) > 1 else [],
            }
        
        # Use LLM for classification
        prompt = f"""Analyze this news content and classify it by industry.

Headline: {headline}

Content excerpt: {content[:1000]}

Available industries:
{', '.join([cat.value for cat in IndustryCategory])}

Respond with JSON:
{{
    "primary_industry": "technology",
    "secondary_industries": ["finance", "retail"],
    "reasoning": "explanation of classification"
}}

Choose the MOST RELEVANT primary industry and up to 2 secondary industries."""

        system_prompt = "You are an expert industry analyst. Classify news content accurately."
        
        try:
            response = await self.call_llm_json(prompt, system_prompt)
            
            primary = IndustryCategory(response.get('primary_industry', 'technology'))
            secondary = [
                IndustryCategory(ind) 
                for ind in response.get('secondary_industries', [])
                if ind in [cat.value for cat in IndustryCategory]
            ]
            
            return {
                'primary': primary,
                'secondary': secondary[:2],  # Max 2 secondary
                'reasoning': response.get('reasoning', '')
            }
            
        except Exception as e:
            self.logger.warning(f"LLM classification failed, using keyword fallback: {e}")
            return self._classify_by_keywords(headline, content)
    
    def _classify_by_keywords(self, headline: str, content: str) -> Dict[str, Any]:
        """Fallback: Classify by keyword matching"""
        text = (headline + " " + content).lower()
        
        scores = {}
        for industry, keywords in self.industry_keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[industry] = score
        
        if not scores:
            return {
                'primary': IndustryCategory.OTHER,
                'secondary': [],
            }
        
        sorted_industries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'primary': sorted_industries[0][0],
            'secondary': [ind for ind, _ in sorted_industries[1:3]],
        }
    
    async def _extract_topics(self, headline: str, content: str) -> List[str]:
        """Extract main topics from content using LLM"""
        
        prompt = f"""Extract 3-5 main topics from this news content.

Headline: {headline}

Content: {content[:1500]}

Return a JSON array of specific topics (not generic categories):
{{"topics": ["artificial intelligence", "product launch", "series b funding"]}}

Focus on concrete subjects, events, and themes."""

        try:
            response = await self.call_llm_json(prompt)
            topics = response.get('topics', [])
            return [t.lower() for t in topics[:5]]  # Max 5 topics
            
        except Exception as e:
            self.logger.warning(f"Topic extraction failed: {e}")
            return self._extract_topics_simple(headline, content)
    
    def _extract_topics_simple(self, headline: str, content: str) -> List[str]:
        """Simple topic extraction fallback"""
        # Extract capitalized phrases as potential topics
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', headline + " " + content)
        topics = list(set([w.lower() for w in words if len(w.split()) <= 3]))
        return topics[:5]
    
    async def _extract_entities(self, content: str) -> List[Entity]:
        """Extract named entities using LLM"""
        
        prompt = f"""Extract named entities from this text.

Content: {content[:2000]}

Return JSON with entities:
{{
    "entities": [
        {{"text": "Apple Inc", "type": "ORG", "relevance": 0.9}},
        {{"text": "Tim Cook", "type": "PERSON", "relevance": 0.8}}
    ]
}}

Types: PERSON, ORG, GPE (location), PRODUCT, EVENT, LAW, MONEY
Only include entities with relevance > 0.5"""

        try:
            response = await self.call_llm_json(prompt)
            entities_data = response.get('entities', [])
            
            entities = []
            for ent in entities_data[:20]:  # Max 20 entities
                try:
                    entities.append(Entity(
                        text=ent['text'],
                        type=ent['type'],
                        relevance_score=float(ent.get('relevance', 0.7))
                    ))
                except Exception:
                    continue
            
            return entities
            
        except Exception as e:
            self.logger.warning(f"Entity extraction failed: {e}")
            return []
    
    async def _extract_keywords(
        self,
        headline: str,
        content: str,
        topics: List[str]
    ) -> List[str]:
        """Extract SEO keywords"""
        
        # Combine topics with key phrases from content
        keywords = set(topics)
        
        # Extract important noun phrases (simple approach)
        words = re.findall(r'\b[a-z]+\b', (headline + " " + content).lower())
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Top frequent words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords.update([word for word, _ in top_words])
        
        return list(keywords)[:15]  # Max 15 keywords
    
    async def _identify_audiences(
        self,
        primary_industry: IndustryCategory,
        topics: List[str],
        content: str,
        provided_audiences: List[str] = None
    ) -> List[AudienceSegment]:
        """Identify target audience segments"""
        
        if provided_audiences:
            # Use provided audiences with relevance scoring
            return [
                AudienceSegment(
                    name=aud,
                    relevance_score=0.9,
                    characteristics=["provided by user"],
                    estimated_size=None
                )
                for aud in provided_audiences
            ]
        
        prompt = f"""Identify target audiences for this news.

Industry: {primary_industry.value}
Topics: {', '.join(topics)}
Content excerpt: {content[:1000]}

Return JSON with 3-5 audience segments:
{{
    "audiences": [
        {{
            "name": "enterprise CTOs",
            "relevance": 0.95,
            "characteristics": ["technical decision-makers", "budget authority"],
            "estimated_size": 50000
        }}
    ]
}}"""

        try:
            response = await self.call_llm_json(prompt)
            audiences_data = response.get('audiences', [])
            
            audiences = []
            for aud in audiences_data[:5]:
                try:
                    audiences.append(AudienceSegment(
                        name=aud['name'],
                        relevance_score=float(aud.get('relevance', 0.8)),
                        characteristics=aud.get('characteristics', []),
                        estimated_size=aud.get('estimated_size')
                    ))
                except Exception:
                    continue
            
            return audiences
            
        except Exception as e:
            self.logger.warning(f"Audience identification failed: {e}")
            return self._identify_audiences_fallback(primary_industry)
    
    def _identify_audiences_fallback(
        self,
        primary_industry: IndustryCategory
    ) -> List[AudienceSegment]:
        """Fallback audience identification"""
        industry_audiences = {
            IndustryCategory.TECHNOLOGY: ["developers", "tech executives", "investors"],
            IndustryCategory.FINANCE: ["investors", "financial analysts", "traders"],
            IndustryCategory.HEALTHCARE: ["healthcare professionals", "patients", "administrators"],
        }
        
        audience_names = industry_audiences.get(primary_industry, ["general public"])
        
        return [
            AudienceSegment(
                name=name,
                relevance_score=0.7,
                characteristics=[],
                estimated_size=None
            )
            for name in audience_names
        ]
    
    async def _match_outlets(
        self,
        primary_industry: IndustryCategory,
        topics: List[str]
    ) -> List[OutletMatch]:
        """Match relevant media outlets"""
        
        # Determine outlet categories based on industry
        if primary_industry == IndustryCategory.TECHNOLOGY:
            relevant_outlets = self.media_outlets['technology'] + self.media_outlets['business']
        elif primary_industry == IndustryCategory.FINANCE:
            relevant_outlets = self.media_outlets['business']
        else:
            relevant_outlets = self.media_outlets['general'] + self.media_outlets['business']
        
        # Create outlet matches with relevance scores
        matches = []
        for outlet in relevant_outlets[:10]:  # Top 10 outlets
            # Simple relevance based on position (more sophisticated in production)
            relevance = 0.9 - (len(matches) * 0.05)
            
            matches.append(OutletMatch(
                outlet_name=outlet,
                outlet_type="publication",
                relevance_score=max(0.6, relevance),
                audience_overlap=0.8,
                typical_response_time="2-4 hours"
            ))
        
        return matches
    
    async def _analyze_sentiment(self, headline: str, content: str) -> str:
        """Analyze sentiment of content"""
        
        prompt = f"""Analyze the sentiment of this news.

Headline: {headline}
Content: {content[:1000]}

Respond with one word: positive, neutral, or negative"""

        try:
            response = await self.call_llm(prompt)
            sentiment = response.strip().lower()
            
            if sentiment in ['positive', 'neutral', 'negative']:
                return sentiment
            else:
                return 'neutral'
                
        except Exception as e:
            self.logger.warning(f"Sentiment analysis failed: {e}")
            return 'neutral'
    
    async def _calculate_scores(
        self,
        headline: str,
        content: str,
        primary_industry: IndustryCategory,
        topics: List[str],
        entities: List[Entity]
    ) -> Dict[str, float]:
        """Calculate newsworthiness and viral potential scores"""
        
        prompt = f"""Rate this news on two metrics (0.0 to 1.0):

Headline: {headline}
Industry: {primary_industry.value}
Topics: {', '.join(topics)}
Content length: {len(content)} characters

1. Newsworthiness: How newsworthy is this story?
   - 0.9-1.0: Major breaking news
   - 0.7-0.9: Significant news
   - 0.5-0.7: Moderate interest
   - 0.3-0.5: Low interest
   - 0.0-0.3: Not newsworthy

2. Viral Potential: Likelihood of social sharing
   - 0.9-1.0: Extremely viral
   - 0.7-0.9: High potential
   - 0.5-0.7: Moderate potential
   - 0.3-0.5: Low potential
   - 0.0-0.3: Unlikely to spread

Return JSON: {{"newsworthiness": 0.75, "viral_potential": 0.6, "reasoning": "..."}}"""

        try:
            response = await self.call_llm_json(prompt)
            
            return {
                'newsworthiness': min(1.0, max(0.0, float(response.get('newsworthiness', 0.7)))),
                'viral': min(1.0, max(0.0, float(response.get('viral_potential', 0.5)))),
            }
            
        except Exception as e:
            self.logger.warning(f"Scoring failed: {e}")
            # Fallback scoring based on heuristics
            return {
                'newsworthiness': 0.7 if len(entities) > 5 else 0.5,
                'viral': 0.6 if primary_industry == IndustryCategory.TECHNOLOGY else 0.4,
            }
    
    async def _generate_angles(
        self,
        primary_industry: IndustryCategory,
        topics: List[str],
        audiences: List[AudienceSegment]
    ) -> List[str]:
        """Generate recommended story angles for pitching"""
        
        prompt = f"""Suggest 3-5 different angles to pitch this story.

Industry: {primary_industry.value}
Topics: {', '.join(topics)}
Audiences: {', '.join([aud.name for aud in audiences])}

Return JSON array of story angles:
{{"angles": ["Innovation angle: How this disrupts the industry", "Business angle: Impact on market competition"]}}"""

        try:
            response = await self.call_llm_json(prompt)
            return response.get('angles', [])[:5]
            
        except Exception as e:
            self.logger.warning(f"Angle generation failed: {e}")
            return [
                "Industry impact angle",
                "Business strategy angle",
                "Consumer benefit angle"
            ]
    
    async def _generate_summary(
        self,
        industries: Dict,
        topics: List[str],
        audiences: List[AudienceSegment],
        scores: Dict[str, float]
    ) -> str:
        """Generate executive summary of analysis"""
        
        summary = f"Content classified as {industries['primary'].value}"
        
        if industries['secondary']:
            summary += f" with relevance to {', '.join([i.value for i in industries['secondary']])}"
        
        summary += f". Key topics include {', '.join(topics[:3])}."
        summary += f" Primary audiences: {', '.join([a.name for a in audiences[:3]])}."
        summary += f" Newsworthiness: {scores['newsworthiness']:.2f}, Viral potential: {scores['viral']:.2f}."
        
        return summary
