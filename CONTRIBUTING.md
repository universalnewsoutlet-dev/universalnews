# Contributing to Universal News Platform

Thank you for your interest in contributing to the Universal News AI-Powered Distribution Platform!

## 🎯 Project Overview

This is an intelligent, AI-powered news distribution platform with 7 specialized agents that work together to optimize content distribution across multiple channels.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

---

## 📜 Code of Conduct

### Our Standards

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Be professional** in all communications
- **Focus on what's best** for the project and community

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (3.12 recommended)
- **OpenAI API Key** (for LLM functionality)
- **Git** for version control
- **Virtual environment** tool (venv, conda, etc.)

### Initial Setup

1. **Clone the repository**:
```bash
git clone https://github.com/universalnewsoutlet-dev/universalnews.git
cd universalnews
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

5. **Run tests**:
```bash
python test_step2_full_system.py
```

---

## 🔄 Development Workflow

### Branch Strategy

- **main** - Production-ready code (protected)
- **develop** - Integration branch for features
- **feature/*** - Feature development branches
- **bugfix/*** - Bug fix branches
- **hotfix/*** - Emergency production fixes

### Workflow Steps

1. **Create feature branch** from `develop`:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

2. **Make changes** following code style guidelines

3. **Write tests** for new functionality

4. **Run test suite**:
```bash
python test_orchestrator.py
python test_step2_full_system.py
```

5. **Commit changes** with descriptive messages:
```bash
git add .
git commit -m "feat: add new channel integration for LinkedIn"
```

6. **Push to GitHub**:
```bash
git push origin feature/your-feature-name
```

7. **Create Pull Request** to `develop` branch

---

## 💻 Code Style Guidelines

### Python Style

We follow **PEP 8** with some modifications:

#### General Rules

- **Line length**: Max 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes `"` for strings
- **Imports**: Organized (standard → third-party → local)

#### Example

```python
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field

from models import DistributionRequest
from base_agent import BaseAgent


class MyAgent(BaseAgent):
    """Agent for specific functionality.
    
    This agent handles X, Y, and Z operations with
    intelligent decision-making capabilities.
    """
    
    async def execute(self, request: DistributionRequest) -> MyOutput:
        """Execute the agent's main functionality.
        
        Args:
            request: Distribution request with all parameters
            
        Returns:
            MyOutput: Processed results
            
        Raises:
            ValueError: If validation fails
        """
        self.execution_log.reasoning_trail.append("Starting execution")
        
        # Implementation here
        result = await self._process(request)
        
        return result
```

#### Type Hints

- **Always use type hints** for function parameters and returns
- **Use Pydantic models** for complex data structures
- **Document types** in docstrings for complex generics

#### Docstrings

- **Use Google style** docstrings
- **Document all public methods**
- **Include examples** for complex functionality

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `MarketIntelligenceAgent`)
- **Functions/Methods**: `snake_case` (e.g., `analyze_content`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private methods**: `_leading_underscore` (e.g., `_internal_method`)

---

## 🧪 Testing Requirements

### Test Coverage

- **All new features** must have tests
- **Minimum coverage**: 80% for new code
- **Critical paths**: 100% coverage required

### Test Types

#### 1. Unit Tests

Test individual components in isolation:

```python
def test_market_intelligence_agent():
    """Test market intelligence analysis."""
    agent = MarketIntelligenceAgent()
    request = ContentAnalysisRequest(
        distribution_id="test-123",
        headline="Test Headline",
        content="Test content..."
    )
    
    result = await agent.execute(request)
    
    assert result.primary_industry is not None
    assert len(result.target_audiences) > 0
```

#### 2. Integration Tests

Test agent coordination:

```python
def test_full_distribution_workflow():
    """Test complete distribution workflow."""
    orchestrator = OrchestratorAgent()
    request = DistributionRequest(...)
    
    result = await orchestrator.execute(request)
    
    assert result.status == DistributionStatus.COMPLETED
    assert len(result.deployed_channels) > 0
```

#### 3. End-to-End Tests

Test complete user scenarios (in `test_step2_full_system.py`)

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python test_orchestrator.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run integration tests
python test_step2_full_system.py
```

---

## 🔍 Pull Request Process

### Before Submitting

1. ✅ **Code follows style guidelines**
2. ✅ **All tests pass**
3. ✅ **New tests added** for new features
4. ✅ **Documentation updated** (if needed)
5. ✅ **No merge conflicts** with target branch
6. ✅ **Commit messages** follow convention

### PR Template

Use this template for your PR description:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- List specific changes
- Be concise but thorough

## Testing
- Describe testing performed
- Include test results

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

### Review Process

1. **Automated checks** run (linting, tests)
2. **Code review** by maintainer (1+ approval required)
3. **Address feedback** (make changes if requested)
4. **Final approval** from maintainer
5. **Merge** to target branch

### Commit Message Convention

We use **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Maintenance tasks

**Examples**:
```bash
feat(channel-router): add LinkedIn channel support
fix(compliance): correct GDPR validation logic
docs(readme): update installation instructions
test(orchestrator): add async coordination tests
```

---

## 📁 Project Structure

```
universalnews/
├── __init__.py                      # Package initialization
├── base_agent.py                    # Base agent framework
├── config.py                        # Configuration management
├── models.py                        # Pydantic data models
│
├── orchestrator_agent.py            # Master coordinator
│
├── market_intelligence_agent.py     # Content analysis
├── compliance_agent.py              # Regulatory checks
├── channel_router_agent.py          # Channel optimization
├── journalist_targeting_agent.py    # Journalist matching
├── deployment_agent.py              # Multi-channel execution
├── analytics_agent.py               # Performance tracking
│
├── test_orchestrator.py             # Unit tests
├── test_step2_full_system.py        # Integration tests
├── example_usage.py                 # Usage examples
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── QUICKSTART.md                    # Quick start guide
├── QUICK_REFERENCE.md               # Developer reference
├── CONTRIBUTING.md                  # This file
│
└── docs/                            # Additional documentation
    ├── INDEX.md
    ├── EXECUTIVE_BRIEFING.md
    └── COMPLETE_TIMEZONE_FIX_REPORT.md
```

### Key Components

- **Agents** - 7 specialized AI agents (each in separate file)
- **Models** - Pydantic schemas for type safety and validation
- **Config** - Centralized configuration management
- **Tests** - Comprehensive test coverage

---

## 🎯 Agent Development Guidelines

When developing new agents or modifying existing ones:

### 1. Inherit from BaseAgent

```python
from base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="my_new_agent")
```

### 2. Define Input/Output Models

```python
class MyAgentInput(BaseModel):
    """Input schema for MyNewAgent."""
    field1: str
    field2: Optional[int] = None

class MyAgentOutput(BaseModel):
    """Output schema for MyNewAgent."""
    result: str
    metadata: Dict[str, Any]
```

### 3. Implement execute() Method

```python
async def execute(self, request: MyAgentInput) -> MyAgentOutput:
    """Main execution method."""
    self.execution_log.started_at = datetime.now(timezone.utc)
    self.execution_log.reasoning_trail.append("Starting processing")
    
    try:
        # Your logic here
        result = await self._process(request)
        
        self.execution_log.success = True
        return result
        
    except Exception as e:
        self.execution_log.success = False
        self.execution_log.error_message = str(e)
        raise
    finally:
        self.execution_log.completed_at = datetime.now(timezone.utc)
```

### 4. Add Logging and Observability

```python
self.execution_log.reasoning_trail.append(f"Analyzed {count} items")
self.logger.info(f"Processing completed in {duration}s")
```

---

## 🐛 Bug Reports

### Before Submitting

1. **Check existing issues** - Bug may already be reported
2. **Reproduce the bug** - Ensure it's consistent
3. **Gather information** - Logs, environment, steps to reproduce

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Initialize orchestrator with '...'
2. Execute distribution with '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g., macOS 14.1]
- Python version: [e.g., 3.11.6]
- Package versions: [from pip freeze]

**Logs**
```
Paste relevant logs here
```

**Additional context**
Any other information about the problem.
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Problem it Solves**
What problem does this feature address?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
What other solutions did you consider?

**Additional Context**
Any other relevant information.
```

---

## 📚 Additional Resources

- **README.md** - Project overview and installation
- **QUICKSTART.md** - Get started in 5 minutes
- **QUICK_REFERENCE.md** - Developer quick reference
- **API Documentation** - (Coming soon)

---

## 🤝 Questions?

- **Open an issue** for questions about contributing
- **Check existing issues** for similar questions
- **Review documentation** in the `docs/` folder

---

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Universal News Platform! 🎉**

---

**Last Updated**: December 14, 2025  
**Version**: 1.0
