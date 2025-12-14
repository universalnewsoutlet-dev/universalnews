# Universal News - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Installation

```bash
# Clone or navigate to the project
cd universal_news/

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# Minimum required:
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Run Tests

```bash
# Validate the installation
python test_orchestrator.py
```

Expected output:
```
✅ DISTRIBUTION COMPLETED SUCCESSFULLY
📊 EXECUTION SUMMARY
   Status: COMPLETED
   Duration: 0.00 seconds
```

### Step 4: Try Examples

```bash
# Run example scenarios
python example_usage.py
```

---

## 📝 Basic Usage

### Simple Distribution

```python
import asyncio
from models import DistributionRequest, UrgencyLevel, ComplianceRequirement
from orchestrator_agent import OrchestratorAgent

async def distribute_news():
    # Create request
    request = DistributionRequest(
        organization_id="your_org",
        user_id="your_user",
        headline="Your News Headline",
        content="Your full news content...",
        target_budget=1500.00,
        urgency=UrgencyLevel.STANDARD,
        compliance_requirements=[ComplianceRequirement.NONE],
    )
    
    # Execute distribution
    orchestrator = OrchestratorAgent()
    result = await orchestrator.execute(request)
    
    print(f"Status: {result.status}")
    print(f"Channels deployed: {result.distribution_results.total_channels_deployed}")

# Run
asyncio.run(distribute_news())
```

---

## 🎯 What's Working (Step 1)

✅ **Agent Contracts**: All input/output models defined  
✅ **Orchestrator**: Master coordinator working  
✅ **Base Framework**: Agent foundation ready  
✅ **Mock Execution**: Full workflow validated  
✅ **Configuration**: Environment management  

⏳ **Coming in Step 2**:
- Real content analysis (NLP)
- Compliance validation
- Channel optimization
- Journalist targeting
- External API integrations
- Performance analytics

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `models.py` | Data models and contracts |
| `config.py` | Configuration management |
| `base_agent.py` | Agent base class |
| `orchestrator_agent.py` | Workflow coordinator |
| `test_orchestrator.py` | Test suite |
| `example_usage.py` | Usage examples |

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install pydantic python-dotenv openai
```

### "OpenAI API key not configured"
Edit `.env` and add:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Tests show warnings about agents
This is expected in Step 1. The orchestrator uses mock agents until Step 2 implements real agents.

---

## 📖 Next Steps

1. **Read the README**: Comprehensive documentation
2. **Check STEP1_CHECKPOINT.md**: Detailed technical report
3. **Explore examples**: See `example_usage.py` for real scenarios
4. **Wait for Step 2**: Real agent intelligence coming soon

---

## 🆘 Support

- **Documentation**: See `README.md`
- **Technical Details**: See `STEP1_CHECKPOINT.md`
- **Code Examples**: See `example_usage.py`

---

**Status**: Step 1 Complete ✅  
**Ready**: For Step 2 (Specialized Agent Implementation)
