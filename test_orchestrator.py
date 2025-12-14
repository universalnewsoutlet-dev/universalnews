"""
Universal News - Orchestrator Test Harness
Demonstrates the orchestrator executing a full distribution workflow with mock agents
"""

import asyncio
import json
from datetime import datetime, timezone
from uuid import uuid4

from models import (
    DistributionRequest,
    UrgencyLevel,
    IndustryCategory,
    ComplianceRequirement,
)
from orchestrator_agent import OrchestratorAgent


def create_sample_request() -> DistributionRequest:
    """Create a sample distribution request for testing"""
    return DistributionRequest(
        distribution_id=uuid4(),
        organization_id="org_techcorp_123",
        user_id="user_john_doe",
        headline="TechCorp Launches Revolutionary AI-Powered Analytics Platform",
        content="""
        TechCorp, a leading enterprise software company, today announced the launch of 
        InsightAI, a revolutionary artificial intelligence-powered analytics platform 
        that transforms how businesses make data-driven decisions.
        
        The platform leverages advanced machine learning algorithms to analyze vast 
        amounts of data in real-time, providing actionable insights that were previously 
        impossible to obtain. Early adopters report a 300% increase in decision-making 
        speed and a 45% reduction in operational costs.
        
        "InsightAI represents a paradigm shift in business analytics," said Jane Smith, 
        CEO of TechCorp. "We're not just processing data—we're predicting future trends 
        and empowering businesses to stay ahead of the competition."
        
        The platform integrates seamlessly with existing enterprise systems and offers 
        industry-leading security features, making it ideal for Fortune 500 companies 
        and rapidly growing startups alike.
        
        InsightAI is available immediately with pricing starting at $499 per month. 
        TechCorp is offering a 30-day free trial for early adopters.
        """,
        summary="TechCorp launches InsightAI, an AI-powered analytics platform that increases decision-making speed by 300%",
        media_urls=[],
        target_budget=1500.00,
        urgency=UrgencyLevel.STANDARD,
        target_industries=[IndustryCategory.TECHNOLOGY, IndustryCategory.FINANCE],
        target_audiences=["enterprise CTOs", "data scientists", "business analysts"],
        target_channels=None,  # Let AI decide
        compliance_requirements=[ComplianceRequirement.NONE],
        created_at=datetime.now(timezone.utc),
        idempotency_key=f"test_{uuid4()}",
    )


async def test_orchestrator_execution():
    """
    Test the orchestrator with a sample request
    Demonstrates the full workflow with mock agents
    """
    print("=" * 80)
    print("UNIVERSAL NEWS - ORCHESTRATOR TEST HARNESS")
    print("=" * 80)
    print()
    
    # Create sample request
    request = create_sample_request()
    
    print("📋 DISTRIBUTION REQUEST")
    print("-" * 80)
    print(f"Distribution ID: {request.distribution_id}")
    print(f"Organization: {request.organization_id}")
    print(f"Headline: {request.headline}")
    print(f"Budget: ${request.target_budget:,.2f}")
    print(f"Urgency: {request.urgency}")
    print(f"Industries: {', '.join([i.value for i in request.target_industries])}")
    print(f"Audiences: {', '.join(request.target_audiences)}")
    print()
    
    # Create orchestrator
    orchestrator = OrchestratorAgent()
    
    # Note: In Step 1, agents are not registered, so orchestrator uses mock outputs
    print("🤖 ORCHESTRATOR INITIALIZATION")
    print("-" * 80)
    print("✅ Orchestrator initialized")
    print("⚠️  Specialized agents not registered - using mock outputs")
    print()
    
    # Execute distribution
    print("🚀 STARTING DISTRIBUTION WORKFLOW")
    print("-" * 80)
    print()
    
    start_time = datetime.now(timezone.utc)
    
    try:
        result = await orchestrator.execute(request)
        
        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()
        
        print()
        print("=" * 80)
        print("✅ DISTRIBUTION COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print()
        
        # Display results
        print("📊 EXECUTION SUMMARY")
        print("-" * 80)
        print(f"Status: {result.status}")
        print(f"Distribution ID: {result.distribution_id}")
        print(f"Started: {result.started_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Completed: {result.completed_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Duration: {result.total_execution_time_seconds:.2f} seconds")
        print()
        
        print("📝 STEPS COMPLETED")
        print("-" * 80)
        for i, step in enumerate(result.steps_completed, 1):
            print(f"{i}. {step}")
        print()
        
        # Content Analysis Results
        if result.content_analysis:
            print("🔍 CONTENT ANALYSIS")
            print("-" * 80)
            print(f"Primary Industry: {result.content_analysis.primary_industry}")
            print(f"Topics: {', '.join(result.content_analysis.topics)}")
            print(f"Keywords: {', '.join(result.content_analysis.keywords)}")
            print(f"Newsworthiness Score: {result.content_analysis.newsworthiness_score:.2f}")
            print(f"Viral Potential: {result.content_analysis.viral_potential:.2f}")
            print(f"Sentiment: {result.content_analysis.sentiment}")
            print()
        
        # Compliance Results
        if result.compliance_report:
            print("✓ COMPLIANCE CHECK")
            print("-" * 80)
            print(f"Compliant: {'✅ Yes' if result.compliance_report.compliant else '❌ No'}")
            print(f"Can Proceed: {'✅ Yes' if result.compliance_report.can_proceed else '❌ No'}")
            print(f"Issues: {len(result.compliance_report.issues)}")
            print(f"Requires Approval: {'Yes' if result.compliance_report.requires_human_approval else 'No'}")
            print()
        
        # Channel Mix Results
        if result.channel_mix:
            print("🎯 CHANNEL ROUTING")
            print("-" * 80)
            print(f"Channels Selected: {len(result.channel_mix.channels)}")
            print(f"Total Budget Allocated: ${result.channel_mix.total_allocated_budget:,.2f}")
            print(f"Expected Reach: {result.channel_mix.expected_total_reach:,}")
            print(f"Expected Pickups: {result.channel_mix.expected_media_pickups}")
            print(f"Expected ROI: {result.channel_mix.expected_roi_percentage:.1f}%")
            print(f"Confidence: {result.channel_mix.confidence_score:.2f}")
            print()
            
            print("Channel Breakdown:")
            for ch in result.channel_mix.channels:
                print(f"  • {ch.channel.value}: ${ch.allocated_budget:,.2f}")
                print(f"    - Expected Reach: {ch.expected_reach:,}")
                print(f"    - Expected Pickups: {ch.expected_pickups}")
                print(f"    - Rationale: {ch.rationale}")
            print()
        
        # Deployment Results
        if result.distribution_results:
            print("🚀 DEPLOYMENT")
            print("-" * 80)
            print(f"Channels Deployed: {result.distribution_results.total_channels_deployed}")
            print(f"Successful: {result.distribution_results.successful_deployments}")
            print(f"Failed: {result.distribution_results.failed_deployments}")
            print(f"Initial Reach: {result.distribution_results.initial_reach:,}")
            print(f"Overall Status: {result.distribution_results.overall_status}")
            print()
            
            print("Deployment Details:")
            for ch_result in result.distribution_results.channel_results:
                status_icon = "✅" if ch_result.status == "success" else "❌"
                print(f"  {status_icon} {ch_result.channel.value}")
                print(f"     Submission ID: {ch_result.submission_id}")
                if ch_result.reach:
                    print(f"     Reach: {ch_result.reach:,}")
            print()
        
        # Errors and Warnings
        if result.errors:
            print("❌ ERRORS")
            print("-" * 80)
            for error in result.errors:
                print(f"  • {error}")
            print()
        
        if result.warnings:
            print("⚠️  WARNINGS")
            print("-" * 80)
            for warning in result.warnings:
                print(f"  • {warning}")
            print()
        
        # Agent Execution Summary
        print("🤖 AGENT PERFORMANCE")
        print("-" * 80)
        summary = orchestrator.get_execution_summary()
        print(f"Agent: {summary.get('agent')}")
        print(f"Duration: {summary.get('duration_seconds', 0):.2f}s")
        print(f"LLM Calls: {summary.get('llm_calls', 0)}")
        print(f"Total Tokens: {summary.get('total_tokens', 0):,}")
        print(f"Cost: ${summary.get('cost_usd', 0):.4f}")
        print()
        
        print("=" * 80)
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
        return result
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ DISTRIBUTION FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        print()
        raise


async def test_status_retrieval():
    """Test retrieving distribution status"""
    print("\n")
    print("=" * 80)
    print("TESTING STATUS RETRIEVAL")
    print("=" * 80)
    print()
    
    request = create_sample_request()
    orchestrator = OrchestratorAgent()
    
    # Execute distribution
    result = await orchestrator.execute(request)
    
    # Retrieve status
    status = orchestrator.get_status(request.distribution_id)
    
    print(f"Status retrieved: {status.status if status else 'Not found'}")
    print(f"Current step: {status.current_step if status else 'N/A'}")
    print(f"Steps completed: {len(status.steps_completed) if status else 0}")
    print()


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "UNIVERSAL NEWS TEST SUITE" + " " * 33 + "║")
    print("║" + " " * 25 + "Step 1: Orchestrator" + " " * 34 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    # Run tests
    asyncio.run(test_orchestrator_execution())
    asyncio.run(test_status_retrieval())
    
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "ALL TESTS PASSED" + " " * 32 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")


if __name__ == "__main__":
    main()
