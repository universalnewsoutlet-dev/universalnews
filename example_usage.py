"""
Universal News - Example Usage
Demonstrates how to use the orchestrator agent system
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


async def example_basic_distribution():
    """
    Example 1: Basic news distribution
    Minimal configuration - let AI decide everything
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Distribution")
    print("="*80 + "\n")
    
    # Create a simple request
    request = DistributionRequest(
        organization_id="org_example",
        user_id="user_demo",
        headline="Company Launches New Product",
        content="We are excited to announce the launch of our revolutionary new product...",
        target_budget=1000.00,
        urgency=UrgencyLevel.STANDARD,
        compliance_requirements=[ComplianceRequirement.NONE],
    )
    
    # Execute distribution
    orchestrator = OrchestratorAgent()
    result = await orchestrator.execute(request)
    
    print(f"✅ Distribution completed: {result.status}")
    print(f"⏱  Execution time: {result.total_execution_time_seconds:.2f}s")
    print(f"🎯 Channels deployed: {result.distribution_results.total_channels_deployed if result.distribution_results else 0}")
    

async def example_targeted_distribution():
    """
    Example 2: Targeted distribution with specific requirements
    Specify industries, audiences, and urgency
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Targeted Distribution")
    print("="*80 + "\n")
    
    request = DistributionRequest(
        organization_id="org_techstartup",
        user_id="user_marketing_director",
        headline="TechStartup Raises $50M Series B Led by Top VC Firm",
        content="""
        TechStartup, an enterprise AI company, announced today it has raised $50 million
        in Series B funding led by Sequoia Capital with participation from existing
        investors including Andreessen Horowitz and Y Combinator.
        
        The funding will be used to expand the engineering team, accelerate product
        development, and increase go-to-market activities in the enterprise segment.
        
        "This investment validates our vision of making AI accessible to every business,"
        said CEO John Smith. "We're seeing unprecedented demand from Fortune 500 companies."
        
        TechStartup has grown 400% year-over-year and now serves over 500 enterprise
        customers including Microsoft, Google, and Amazon.
        """,
        summary="TechStartup raises $50M Series B to accelerate enterprise AI adoption",
        target_budget=2500.00,
        urgency=UrgencyLevel.URGENT,  # News is time-sensitive
        
        # Specify target markets
        target_industries=[
            IndustryCategory.TECHNOLOGY,
            IndustryCategory.FINANCE,  # VCs and investors
        ],
        
        # Define audiences
        target_audiences=[
            "venture capitalists",
            "enterprise CIOs",
            "tech journalists",
            "startup founders",
        ],
        
        # Let AI select optimal channels
        target_channels=None,
        
        compliance_requirements=[ComplianceRequirement.NONE],
    )
    
    orchestrator = OrchestratorAgent()
    result = await orchestrator.execute(request)
    
    print(f"✅ Status: {result.status}")
    print(f"⏱  Time: {result.total_execution_time_seconds:.2f}s")
    
    if result.content_analysis:
        print(f"📊 Newsworthiness: {result.content_analysis.newsworthiness_score:.2f}")
        print(f"📈 Viral potential: {result.content_analysis.viral_potential:.2f}")
    
    if result.channel_mix:
        print(f"💰 Budget allocated: ${result.channel_mix.total_allocated_budget:,.2f}")
        print(f"📢 Expected reach: {result.channel_mix.expected_total_reach:,}")
        print(f"📰 Expected pickups: {result.channel_mix.expected_media_pickups}")


async def example_compliance_distribution():
    """
    Example 3: SEC material disclosure distribution
    High compliance requirements with specific regulations
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Compliance-Driven Distribution (SEC)")
    print("="*80 + "\n")
    
    request = DistributionRequest(
        organization_id="org_publiccorp",
        user_id="user_ir_director",
        headline="PublicCorp Reports Q4 2024 Earnings Beat Expectations",
        content="""
        PublicCorp (NASDAQ: PBLC) today announced financial results for the fourth
        quarter and full year ended December 31, 2024.
        
        Q4 2024 Financial Highlights:
        - Revenue: $1.2 billion, up 25% year-over-year
        - Adjusted EBITDA: $240 million, representing 20% margin
        - Diluted EPS: $0.85, beating analyst consensus of $0.78
        
        Full Year 2024 Results:
        - Revenue: $4.5 billion, up 30% from 2023
        - Adjusted EBITDA: $900 million
        - Operating cash flow: $650 million
        
        "We delivered strong results across all segments," said CFO Jane Doe.
        "Our financial position remains robust with $500M in cash and no debt."
        
        The company will host a conference call today at 5:00 PM ET.
        """,
        target_budget=5000.00,
        urgency=UrgencyLevel.IMMEDIATE,  # Material disclosure must be immediate
        
        target_industries=[IndustryCategory.FINANCE],
        target_audiences=["institutional investors", "retail investors", "financial analysts"],
        
        # Compliance is critical
        compliance_requirements=[
            ComplianceRequirement.SEC_MATERIAL,
            ComplianceRequirement.SOX,
        ],
    )
    
    orchestrator = OrchestratorAgent()
    result = await orchestrator.execute(request)
    
    print(f"✅ Status: {result.status}")
    
    if result.compliance_report:
        print(f"⚖️  Compliant: {'Yes' if result.compliance_report.compliant else 'No'}")
        print(f"🔒 Can proceed: {'Yes' if result.compliance_report.can_proceed else 'No'}")
        print(f"⚠️  Issues: {len(result.compliance_report.issues)}")
        
        if result.compliance_report.required_channels:
            print(f"📋 Required channels: {[ch.value for ch in result.compliance_report.required_channels]}")


async def example_status_tracking():
    """
    Example 4: Status tracking and monitoring
    Shows how to track distribution progress in real-time
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Status Tracking")
    print("="*80 + "\n")
    
    request = DistributionRequest(
        organization_id="org_demo",
        user_id="user_demo",
        headline="Demo News for Status Tracking",
        content="This is a demonstration of status tracking capabilities.",
        target_budget=500.00,
        urgency=UrgencyLevel.STANDARD,
        compliance_requirements=[ComplianceRequirement.NONE],
    )
    
    orchestrator = OrchestratorAgent()
    
    # In a real async environment, you could poll status while processing
    print("🚀 Starting distribution...")
    print(f"📋 Distribution ID: {request.distribution_id}")
    
    result = await orchestrator.execute(request)
    
    # Retrieve status after completion
    status = orchestrator.get_status(request.distribution_id)
    
    if status:
        print(f"\n📊 Final Status: {status.status}")
        print(f"📝 Steps completed: {len(status.steps_completed)}")
        print(f"⏱  Duration: {status.total_execution_time_seconds:.2f}s")
        print(f"\nExecution trail:")
        for i, step in enumerate(status.steps_completed, 1):
            print(f"  {i}. ✅ {step}")


async def example_batch_distribution():
    """
    Example 5: Batch processing multiple distributions
    Demonstrates parallel execution capabilities
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Batch Distribution")
    print("="*80 + "\n")
    
    # Create multiple requests
    requests = [
        DistributionRequest(
            organization_id="org_batch",
            user_id="user_batch",
            headline=f"News Item {i+1}",
            content=f"Content for news item {i+1}",
            target_budget=500.00,
            urgency=UrgencyLevel.STANDARD,
            compliance_requirements=[ComplianceRequirement.NONE],
        )
        for i in range(3)
    ]
    
    orchestrator = OrchestratorAgent()
    
    # Execute in parallel
    print(f"🚀 Processing {len(requests)} distributions in parallel...")
    start_time = datetime.now(timezone.utc)
    
    results = await asyncio.gather(
        *[orchestrator.execute(req) for req in requests]
    )
    
    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n✅ All distributions completed in {duration:.2f}s")
    print(f"📊 Success rate: {sum(1 for r in results if r.status == 'completed')}/{len(results)}")
    print(f"⚡ Average time per distribution: {duration/len(results):.2f}s")


async def main():
    """Run all examples"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*25 + "UNIVERSAL NEWS" + " "*40 + "║")
    print("║" + " "*22 + "Example Usage Scenarios" + " "*33 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run examples
    await example_basic_distribution()
    await example_targeted_distribution()
    await example_compliance_distribution()
    await example_status_tracking()
    await example_batch_distribution()
    
    print("\n" + "="*80)
    print("✅ All examples completed successfully!")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
