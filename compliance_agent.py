"""
Universal News - Compliance Agent
Validates regulatory requirements and ensures distribution compliance

This agent ensures news distribution meets:
1. SEC material disclosure requirements
2. GDPR data protection rules
3. FINRA financial industry regulations
4. HIPAA healthcare privacy
5. SOX corporate governance
6. Industry-specific compliance rules
"""

from typing import List, Dict
from datetime import datetime, timezone

from base_agent import BaseAgent
from models import (
    ComplianceCheckRequest,
    ComplianceReport,
    ComplianceIssue,
    ComplianceRequirement,
    ChannelType,
    IndustryCategory,
)


class ComplianceAgent(BaseAgent[ComplianceCheckRequest, ComplianceReport]):
    """
    Validates regulatory compliance for news distribution
    
    Capabilities:
    - SEC material disclosure validation
    - Regulatory requirement checking
    - Channel compliance validation
    - Required disclaimer identification
    - Approval workflow determination
    """
    
    def __init__(self):
        super().__init__(agent_name="compliance")
        
        # Compliance rules database
        self.compliance_rules = self._initialize_compliance_rules()
    
    def _initialize_compliance_rules(self) -> Dict:
        """Initialize compliance rule sets"""
        return {
            ComplianceRequirement.SEC_MATERIAL: {
                'name': 'SEC Material Disclosure',
                'required_channels': [ChannelType.NEWSWIRE],
                'forbidden_channels': [],
                'required_disclaimers': [
                    'Forward-looking statements disclaimer',
                    'SEC filing reference'
                ],
                'approval_required': True,
                'timing_requirements': 'Must be immediate (Regulation FD)',
                'industries': [IndustryCategory.FINANCE],
            },
            ComplianceRequirement.FINRA: {
                'name': 'FINRA Financial Industry',
                'required_channels': [],
                'forbidden_channels': [],
                'required_disclaimers': [
                    'Investment disclaimer',
                    'Risk disclosure',
                    'FINRA member notice'
                ],
                'approval_required': True,
                'timing_requirements': 'Pre-approval required',
                'industries': [IndustryCategory.FINANCE],
            },
            ComplianceRequirement.GDPR: {
                'name': 'GDPR Data Protection',
                'required_channels': [],
                'forbidden_channels': [],
                'required_disclaimers': [
                    'Privacy policy link',
                    'Data processing notice'
                ],
                'approval_required': False,
                'timing_requirements': None,
                'industries': [],  # Applies to all
            },
            ComplianceRequirement.HIPAA: {
                'name': 'HIPAA Healthcare Privacy',
                'required_channels': [],
                'forbidden_channels': [ChannelType.SOCIAL_MEDIA],
                'required_disclaimers': [
                    'Patient privacy notice',
                    'HIPAA compliance statement'
                ],
                'approval_required': True,
                'timing_requirements': 'Legal review required',
                'industries': [IndustryCategory.HEALTHCARE],
            },
            ComplianceRequirement.SOX: {
                'name': 'Sarbanes-Oxley Act',
                'required_channels': [ChannelType.NEWSWIRE],
                'forbidden_channels': [],
                'required_disclaimers': [
                    'Financial accuracy certification',
                    'Management responsibility statement'
                ],
                'approval_required': True,
                'timing_requirements': 'CFO approval required',
                'industries': [IndustryCategory.FINANCE],
            },
        }
    
    async def process(self, request: ComplianceCheckRequest) -> ComplianceReport:
        """
        Validate compliance requirements for distribution
        
        Args:
            request: Compliance check request
            
        Returns:
            Comprehensive compliance report
        """
        self.log_reasoning("Starting compliance check", {
            "requirements": [req.value for req in request.compliance_requirements],
            "industry": request.content_analysis.primary_industry.value,
        })
        
        issues = []
        required_channels = []
        forbidden_channels = []
        required_disclaimers = []
        requires_approval = False
        
        # Skip if no compliance requirements
        if ComplianceRequirement.NONE in request.compliance_requirements:
            self.log_reasoning("No compliance requirements - passing")
            return ComplianceReport(
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
                checked_at=datetime.now(timezone.utc),
            )
        
        # Check each requirement
        for requirement in request.compliance_requirements:
            if requirement == ComplianceRequirement.NONE:
                continue
            
            self.log_reasoning(f"Checking requirement: {requirement.value}")
            
            # Get rule set
            rule = self.compliance_rules.get(requirement)
            if not rule:
                issues.append(ComplianceIssue(
                    severity="warning",
                    requirement=requirement,
                    issue=f"Unknown compliance requirement: {requirement.value}",
                    recommendation="Contact legal team for guidance"
                ))
                continue
            
            # Check industry applicability
            if rule['industries'] and request.content_analysis.primary_industry not in rule['industries']:
                issues.append(ComplianceIssue(
                    severity="warning",
                    requirement=requirement,
                    issue=f"{rule['name']} may not apply to {request.content_analysis.primary_industry.value} industry",
                    recommendation="Verify applicability with legal team"
                ))
            
            # Collect required channels
            required_channels.extend(rule['required_channels'])
            
            # Collect forbidden channels
            forbidden_channels.extend(rule['forbidden_channels'])
            
            # Collect disclaimers
            required_disclaimers.extend(rule['required_disclaimers'])
            
            # Check if approval required
            if rule['approval_required']:
                requires_approval = True
            
            # Validate timing requirements
            if rule['timing_requirements']:
                timing_issue = await self._check_timing(
                    requirement,
                    rule['timing_requirements'],
                    request
                )
                if timing_issue:
                    issues.append(timing_issue)
        
        # Validate channel mix against compliance
        if request.channel_mix:
            channel_issues = self._validate_channels(
                request.channel_mix,
                required_channels,
                forbidden_channels
            )
            issues.extend(channel_issues)
        
        # Run LLM-based content compliance check
        content_issues = await self._check_content_compliance(request)
        issues.extend(content_issues)
        
        # Categorize issues
        critical_issues = [i for i in issues if i.severity == "critical"]
        warnings = [i for i in issues if i.severity == "warning"]
        
        # Determine overall compliance
        compliant = len(critical_issues) == 0
        can_proceed = compliant and not requires_approval  # Block if critical issues OR approval needed
        
        self.log_reasoning("Compliance check complete", {
            "compliant": compliant,
            "can_proceed": can_proceed,
            "critical_issues": len(critical_issues),
            "warnings": len(warnings),
            "requires_approval": requires_approval,
        })
        
        return ComplianceReport(
            distribution_id=request.distribution_id,
            compliant=compliant,
            can_proceed=can_proceed,
            issues=issues,
            critical_issues=critical_issues,
            warnings=warnings,
            required_channels=list(set(required_channels)),
            forbidden_channels=list(set(forbidden_channels)),
            required_disclaimers=list(set(required_disclaimers)),
            requires_human_approval=requires_approval,
            approval_workflow="Legal team review required" if requires_approval else None,
            checked_at=datetime.now(timezone.utc),
        )
    
    async def _check_timing(
        self,
        requirement: ComplianceRequirement,
        timing_rule: str,
        request: ComplianceCheckRequest
    ) -> ComplianceIssue:
        """Check timing compliance"""
        
        # For SEC material disclosure, check if marked as immediate
        if requirement == ComplianceRequirement.SEC_MATERIAL:
            # Would check actual urgency from request in full implementation
            # For now, just create info issue
            return ComplianceIssue(
                severity="info",
                requirement=requirement,
                issue=f"Timing requirement: {timing_rule}",
                recommendation="Ensure distribution is executed immediately per Regulation FD"
            )
        
        return None
    
    def _validate_channels(
        self,
        channel_mix,
        required_channels: List[ChannelType],
        forbidden_channels: List[ChannelType]
    ) -> List[ComplianceIssue]:
        """Validate channel selection against compliance rules"""
        
        issues = []
        selected_channels = [ch.channel for ch in channel_mix.channels]
        
        # Check required channels
        for req_channel in required_channels:
            if req_channel not in selected_channels:
                issues.append(ComplianceIssue(
                    severity="critical",
                    requirement=ComplianceRequirement.SEC_MATERIAL,  # Would track specific requirement
                    issue=f"Required channel missing: {req_channel.value}",
                    recommendation=f"Add {req_channel.value} to distribution channels"
                ))
        
        # Check forbidden channels
        for forb_channel in forbidden_channels:
            if forb_channel in selected_channels:
                issues.append(ComplianceIssue(
                    severity="critical",
                    requirement=ComplianceRequirement.HIPAA,  # Would track specific requirement
                    issue=f"Forbidden channel selected: {forb_channel.value}",
                    recommendation=f"Remove {forb_channel.value} from distribution due to compliance restrictions"
                ))
        
        return issues
    
    async def _check_content_compliance(
        self,
        request: ComplianceCheckRequest
    ) -> List[ComplianceIssue]:
        """Use LLM to check content for compliance issues"""
        
        # Build requirements description
        req_descriptions = []
        for req in request.compliance_requirements:
            if req == ComplianceRequirement.NONE:
                continue
            rule = self.compliance_rules.get(req)
            if rule:
                req_descriptions.append(f"- {rule['name']}: {rule.get('timing_requirements', 'Standard compliance')}")
        
        if not req_descriptions:
            return []
        
        prompt = f"""Review this content for compliance issues.

Content Analysis:
- Industry: {request.content_analysis.primary_industry.value}
- Topics: {', '.join(request.content_analysis.topics[:5])}
- Sentiment: {request.content_analysis.sentiment}

Compliance Requirements:
{chr(10).join(req_descriptions)}

Check for:
1. Missing required disclaimers
2. Potentially misleading statements
3. Unsubstantiated claims
4. Privacy concerns
5. Risk disclosure needs

Return JSON:
{{
    "issues": [
        {{
            "severity": "critical" or "warning" or "info",
            "issue": "Description of issue",
            "recommendation": "How to fix"
        }}
    ],
    "compliant": true or false
}}

If no issues, return {{"issues": [], "compliant": true}}"""

        try:
            response = await self.call_llm_json(prompt)
            
            issues = []
            for issue_data in response.get('issues', []):
                # Map to first requirement (would be more sophisticated in production)
                req = request.compliance_requirements[0] if request.compliance_requirements else ComplianceRequirement.NONE
                
                issues.append(ComplianceIssue(
                    severity=issue_data.get('severity', 'info'),
                    requirement=req,
                    issue=issue_data.get('issue', ''),
                    recommendation=issue_data.get('recommendation', '')
                ))
            
            return issues
            
        except Exception as e:
            self.logger.warning(f"Content compliance check failed: {e}")
            return []
