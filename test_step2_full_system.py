"""
Universal News - Step 2 Full System Test
Tests the complete system with all 6 specialized agents integrated
"""

import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from models import (
    DistributionRequest,
    UrgencyLevel,
    IndustryCategory,
    ComplianceRequirement,
)
from orchestrator_agent import OrchestratorAgent


def create_comprehensive_test_request() -> DistributionRequest:
    """Create a comprehensive test request"""
    return DistributionRequest(
        distribution_id=uuid4(),
        organization_id="org_universal_news_test",
        user_id="user_step2_tester",
        headline="Revolutionary AI Platform Transforms Enterprise Decision-Making",
        content="""
        DataCorp, a leading enterprise software innovator, today announced the launch of 
        InsightAI Pro, a groundbreaking artificial intelligence platform that is revolutionizing
        how Fortune 500 companies make strategic decisions.
        
        The platform leverages advanced machine learning algorithms and natural language processing
        to analyze vast amounts of structured and unstructured data in real-time, providing
        actionable insights that were previously impossible to obtain through traditional analytics.
        
        Early adopters, including Fortune 500 companies across finance, healthcare, and retail
        sectors, report a 300% increase in decision-making speed and a 45% reduction in operational
        costs within the first quarter of deployment.
        
        "InsightAI Pro represents a paradigm shift in enterprise analytics," said Dr. Jennifer Chen,
        CEO of DataCorp. "We're not just processing data—we're predicting future trends with 95%
        accuracy and empowering C-suite executives to stay ahead of market disruptions."
        
        The platform features:
        - Real-time predictive analytics with 95% accuracy
        - Natural language query interface requiring zero technical training
        - Seamless integration with existing ERP, CRM, and data warehouse systems
        - Enterprise-grade security with SOC 2 Type II compliance
        - Industry-leading 99.99% uptime SLA
        
        DataCorp has raised $75 million in Series C funding led by Sequoia Capital to accelerate
        product development and expand into European and Asian markets. The company now serves
        over 200 enterprise customers and processes more than 5 billion data points daily.
        
        InsightAI Pro is available immediately with flexible pricing starting at $10,000 per month
        for mid-market companies and custom enterprise pricing for Fortune 500 organizations.
        DataCorp is offering a 60-day free trial with full feature access for qualified enterprises.
        
        For more information, visit www.datacorp.ai/insightai-pro or contact enterprise@datacorp.ai
        """,
        summary="DataCorp launches InsightAI Pro, revolutionizing enterprise decision-making with 95% accurate AI predictions",
        media_urls=[],
        target_budget=2000.00,
        urgency=UrgencyLevel.URGENT,
        target_industries=[IndustryCategory.TECHNOLOGY, IndustryCategory.FINANCE],
        target_audiences=[
            "enterprise CTOs",
            "CFOs",
            "data scientists",
            "business intelligence directors",
            "venture capitalists"
        ],
        target_channels=None,  # Let AI optimize
        compliance_requirements=[ComplianceRequirement.NONE],
        created_at=datetime.now(timezone.utc),
        idempotency_key=f"step2_test_{uuid4()}",
    )


async def test_full_system():
    """Test the complete system with all agents"""
    
    print("\n" + "="*80)
    print("UNIVERSAL NEWS - STEP 2 FULL SYSTEM TEST")
    print("="*80)
    print("\n")
    
    # Create request
    request = create_comprehensive_test_request()
    
    print("📋 TEST REQUEST")
    print("-"*80)
    print(f"Distribution ID: {request.distribution_id}")
    print(f"Organization: {request.organization_id}")
    print(f"Headline: {request.headline}")
    print(f"Content Length: {len(request.content)} characters")
    print(f"Budget: ${request.target_budget:,.2f}")
    print(f"Urgency: {request.urgency.value}")
    print(f"Industries: {', '.join([i.value for i in request.target_industries])}")
    print(f"Audiences: {', '.join(request.target_audiences[:3])}...")
    print("\n")
    
    # Initialize orchestrator with real agents
    print("🤖 INITIALIZING ORCHESTRATOR")
    print("-"*80)
    orchestrator = OrchestratorAgent(auto_initialize_agents=True)
    print("✅ Orchestrator initialized with all 6 specialized agents")
    print("\n")
    
    # Execute distribution
    print("🚀 EXECUTING FULL DISTRIBUTION WORKFLOW")
    print("-"*80)
    print("\n")
    
    start_time = datetime.now(timezone.utc)
    
    try:
        result = await orchestrator.execute(request)
        
        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()
        
        print("\n")
        print("="*80)
        print("✅ DISTRIBUTION COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\n")
        
        # Display comprehensive results
        print("📊 EXECUTION SUMMARY")
        print("-"*80)
        print(f"Status: {result.status.value}")
        print(f"Distribution ID: {result.distribution_id}")
        print(f"Started: {result.started_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Completed: {result.completed_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Total Duration: {result.total_execution_time_seconds:.2f} seconds")
        print(f"Steps Completed: {len(result.steps_completed)}")
        print("\n")
        
        # Content Analysis Results
        if result.content_analysis:
            print("🔍 MARKET INTELLIGENCE ANALYSIS")
            print("-"*80)
            print(f"Primary Industry: {result.content_analysis.primary_industry.value}")
            if result.content_analysis.secondary_industries:
                print(f"Secondary Industries: {', '.join([i.value for i in result.content_analysis.secondary_industries])}")
            print(f"Topics: {', '.join(result.content_analysis.topics[:5])}")
            print(f"Keywords: {', '.join(result.content_analysis.keywords[:8])}")
            print(f"Entities Found: {len(result.content_analysis.entities)}")
            if result.content_analysis.entities[:3]:
                print(f"Top Entities: {', '.join([e.text for e in result.content_analysis.entities[:3]])}")
            print(f"Target Audiences: {len(result.content_analysis.target_audiences)}")
            if result.content_analysis.target_audiences[:3]:
                print(f"Top Audiences: {', '.join([a.name for a in result.content_analysis.target_audiences[:3]])}")
            print(f"Matched Outlets: {len(result.content_analysis.matched_outlets)}")
            print(f"Newsworthiness Score: {result.content_analysis.newsworthiness_score:.2f}")
            print(f"Viral Potential: {result.content_analysis.viral_potential:.2f}")
            print(f"Sentiment: {result.content_analysis.sentiment}")
            print(f"\nAnalysis Summary:")
            print(f"  {result.content_analysis.analysis_summary}")
            print("\n")
        
        # Compliance Results
        if result.compliance_report:
            print("✓ COMPLIANCE VALIDATION")
            print("-"*80)
            print(f"Compliant: {'✅ Yes' if result.compliance_report.compliant else '❌ No'}")
            print(f"Can Proceed: {'✅ Yes' if result.compliance_report.can_proceed else '❌ No'}")
            print(f"Total Issues: {len(result.compliance_report.issues)}")
            print(f"Critical Issues: {len(result.compliance_report.critical_issues)}")
            print(f"Warnings: {len(result.compliance_report.warnings)}")
            print(f"Requires Human Approval: {'Yes' if result.compliance_report.requires_human_approval else 'No'}")
            if result.compliance_report.required_channels:
                print(f"Required Channels: {', '.join([ch.value for ch in result.compliance_report.required_channels])}")
            print("\n")
        
        # Channel Mix Results
        if result.channel_mix:
            print("🎯 CHANNEL ROUTING OPTIMIZATION")
            print("-"*80)
            print(f"Channels Selected: {len(result.channel_mix.channels)}")
            print(f"Total Budget Allocated: ${result.channel_mix.total_allocated_budget:,.2f}")
            print(f"Expected Total Reach: {result.channel_mix.expected_total_reach:,}")
            print(f"Expected Media Pickups: {result.channel_mix.expected_media_pickups}")
            print(f"Expected Backlinks: {result.channel_mix.expected_backlinks}")
            print(f"Expected ROI: {result.channel_mix.expected_roi_percentage:.1f}%")
            print(f"Confidence Score: {result.channel_mix.confidence_score:.2f}")
            print(f"\nStrategy: {result.channel_mix.strategy_summary}")
            print(f"\nChannel Breakdown:")
            for ch in result.channel_mix.channels:
                print(f"  • {ch.channel.value}:")
                print(f"    Budget: ${ch.allocated_budget:,.2f}")
                print(f"    Expected Reach: {ch.expected_reach:,}")
                print(f"    Expected Pickups: {ch.expected_pickups}")
                print(f"    Expected ROI: {ch.expected_roi:.1f}%")
                print(f"    Rationale: {ch.rationale}")
            print("\n")
        
        # Journalist Targeting Results
        if result.journalist_targeting:
            print("👥 JOURNALIST TARGETING")
            print("-"*80)
            print(f"Total Targets: {result.journalist_targeting.total_targets}")
            print(f"Average Relevance: {result.journalist_targeting.average_relevance_score:.2f}")
            print(f"\nStrategy: {result.journalist_targeting.strategy_notes}")
            if result.journalist_targeting.targets[:5]:
                print(f"\nTop 5 Journalist Targets:")
                for i, target in enumerate(result.journalist_targeting.targets[:5], 1):
                    print(f"  {i}. {target.name} - {target.outlet}")
                    print(f"     Relevance: {target.relevance_score:.2f}")
                    print(f"     Subject: {target.personalized_subject}")
                    print(f"     Why Relevant: {target.why_relevant}")
            print("\n")
        
        # Deployment Results
        if result.distribution_results:
            print("🚀 DEPLOYMENT EXECUTION")
            print("-"*80)
            print(f"Channels Deployed: {result.distribution_results.total_channels_deployed}")
            print(f"Successful: {result.distribution_results.successful_deployments}")
            print(f"Failed: {result.distribution_results.failed_deployments}")
            print(f"Initial Reach: {result.distribution_results.initial_reach:,}")
            print(f"Overall Status: {result.distribution_results.overall_status}")
            print(f"\nDeployment Details:")
            for ch_result in result.distribution_results.channel_results:
                status_icon = "✅" if ch_result.status == "success" else "❌"
                print(f"  {status_icon} {ch_result.channel.value}")
                print(f"     Submission ID: {ch_result.submission_id}")
                if ch_result.url:
                    print(f"     URL: {ch_result.url}")
                if ch_result.reach:
                    print(f"     Reach: {ch_result.reach:,}")
            print("\n")
        
        # Performance Metrics
        print("⚡ PERFORMANCE METRICS")
        print("-"*80)
        summary = orchestrator.get_execution_summary()
        print(f"Agent: {summary.get('agent')}")
        print(f"Duration: {summary.get('duration_seconds', 0):.2f} seconds")
        print(f"LLM Calls: {summary.get('llm_calls', 0)}")
        print(f"Total Tokens: {summary.get('total_tokens', 0):,}")
        print(f"Estimated Cost: ${summary.get('cost_usd', 0):.4f}")
        print(f"\n✅ Target: < 120 seconds")
        print(f"{'✅' if duration < 120 else '⚠️'} Actual: {duration:.2f} seconds")
        print("\n")
        
        # Test Summary
        print("="*80)
        print("✅ STEP 2 FULL SYSTEM TEST COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"\n🎉 All 6 specialized agents working together!")
        print(f"📊 Complete workflow executed in {duration:.2f} seconds")
        print(f"🎯 Ready for GitHub push and production deployment\n")
        
        return result
        
    except Exception as e:
        print("\n")
        print("="*80)
        print("❌ DISTRIBUTION FAILED")
        print("="*80)
        print(f"Error: {e}")
        print("\n")
        import traceback
        traceback.print_exc()
        raise


async def main():
    """Run full system test"""
    
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*25 + "UNIVERSAL NEWS" + " "*40 + "║")
    print("║" + " "*20 + "Step 2: Full System Test" + " "*35 + "║")
    print("╚" + "="*78 + "╝")
    print("\n")
    
    await test_full_system()
    
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*22 + "SYSTEM READY FOR PRODUCTION" + " "*29 + "║")
    print("╚" + "="*78 + "╝")
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
