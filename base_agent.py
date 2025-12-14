"""
Universal News - Base Agent Framework
Abstract base class defining standard agent interface and common utilities
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel
from openai import OpenAI

from models import AgentExecutionLog
from config import get_llm_config, get_agent_config

# Type variables for input/output contracts
InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel)


class BaseAgent(ABC, Generic[InputType, OutputType]):
    """
    Abstract base class for all Universal News agents
    
    Provides:
    - Standard execution interface
    - LLM integration wrapper
    - Logging and observability
    - Error handling patterns
    - Token usage tracking
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize base agent
        
        Args:
            agent_name: Unique identifier for this agent
        """
        self.agent_name = agent_name
        self.llm_config = get_llm_config()
        self.agent_config = get_agent_config()
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Initialize LLM client
        self.llm_client = OpenAI(api_key=self.llm_config.api_key)
        
        # Execution tracking
        self.execution_log: Optional[AgentExecutionLog] = None
    
    def _setup_logger(self) -> logging.Logger:
        """Configure logger for this agent"""
        logger = logging.getLogger(f"agent.{self.agent_name}")
        logger.setLevel(getattr(logging, self.agent_config.log_level))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.agent_name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    @abstractmethod
    async def process(self, input_data: InputType) -> OutputType:
        """
        Core agent logic - must be implemented by each agent
        
        Args:
            input_data: Validated input matching agent's contract
            
        Returns:
            Validated output matching agent's contract
        """
        pass
    
    async def execute(self, input_data: InputType) -> OutputType:
        """
        Execute agent with full observability and error handling
        
        Args:
            input_data: Agent input
            
        Returns:
            Agent output
            
        Raises:
            Exception: If agent execution fails after retries
        """
        distribution_id = self._extract_distribution_id(input_data)
        
        # Initialize execution log
        self.execution_log = AgentExecutionLog(
            agent_name=self.agent_name,
            distribution_id=distribution_id,
            started_at=datetime.now(timezone.utc),
        )
        
        self.logger.info(f"Starting execution for distribution: {distribution_id}")
        start_time = time.time()
        
        try:
            # Validate input
            self._validate_input(input_data)
            
            # Execute with retry logic
            output = await self._execute_with_retry(input_data)
            
            # Validate output
            self._validate_output(output)
            
            # Mark success
            self.execution_log.success = True
            self.execution_log.completed_at = datetime.now(timezone.utc)
            self.execution_log.duration_seconds = time.time() - start_time
            
            self.logger.info(
                f"Completed successfully in {self.execution_log.duration_seconds:.2f}s"
            )
            
            return output
            
        except Exception as e:
            self.execution_log.success = False
            self.execution_log.error_message = str(e)
            self.execution_log.completed_at = datetime.now(timezone.utc)
            self.execution_log.duration_seconds = time.time() - start_time
            
            self.logger.error(f"Failed after {self.execution_log.duration_seconds:.2f}s: {e}")
            raise
    
    async def _execute_with_retry(self, input_data: InputType) -> OutputType:
        """Execute with retry logic"""
        last_exception = None
        
        for attempt in range(self.agent_config.max_retries):
            try:
                if attempt > 0:
                    self.logger.info(f"Retry attempt {attempt + 1}/{self.agent_config.max_retries}")
                
                return await self.process(input_data)
                
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                # Don't retry on validation errors
                if isinstance(e, ValueError):
                    raise
                
                # Wait before retry (exponential backoff)
                if attempt < self.agent_config.max_retries - 1:
                    wait_time = 2 ** attempt
                    self.logger.info(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
        
        # All retries exhausted
        raise last_exception
    
    def _validate_input(self, input_data: InputType):
        """Validate input data structure"""
        if not isinstance(input_data, BaseModel):
            raise ValueError(f"Input must be a Pydantic BaseModel, got {type(input_data)}")
        
        self.logger.debug(f"Input validation passed: {type(input_data).__name__}")
    
    def _validate_output(self, output_data: OutputType):
        """Validate output data structure"""
        if not isinstance(output_data, BaseModel):
            raise ValueError(f"Output must be a Pydantic BaseModel, got {type(output_data)}")
        
        self.logger.debug(f"Output validation passed: {type(output_data).__name__}")
    
    def _extract_distribution_id(self, input_data: InputType) -> UUID:
        """Extract distribution_id from input"""
        if hasattr(input_data, 'distribution_id'):
            return input_data.distribution_id
        else:
            # Fallback for requests without distribution_id
            from uuid import uuid4
            return uuid4()
    
    async def call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Call LLM with standard parameters and tracking
        
        Args:
            prompt: User prompt
            system_prompt: Optional system instructions
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            LLM response text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        self.logger.debug(f"Calling LLM with {len(messages)} messages")
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_config.model_name,
                messages=messages,
                temperature=temperature or self.llm_config.temperature,
                max_tokens=max_tokens or self.llm_config.max_tokens,
            )
            
            # Track usage
            if self.execution_log and response.usage:
                self.execution_log.llm_calls += 1
                self.execution_log.total_tokens += response.usage.total_tokens
                
                # Calculate cost
                input_cost = (response.usage.prompt_tokens / 1000) * self.llm_config.input_cost_per_1k
                output_cost = (response.usage.completion_tokens / 1000) * self.llm_config.output_cost_per_1k
                self.execution_log.cost_usd += input_cost + output_cost
            
            result = response.choices[0].message.content
            self.logger.debug(f"LLM response: {len(result)} characters")
            
            return result
            
        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            raise
    
    async def call_llm_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[type[BaseModel]] = None,
    ) -> Dict[str, Any]:
        """
        Call LLM expecting JSON response
        
        Args:
            prompt: User prompt
            system_prompt: Optional system instructions
            response_format: Pydantic model for structured output
            
        Returns:
            Parsed JSON response
        """
        if response_format:
            # Use OpenAI's structured output feature
            response = self.llm_client.beta.chat.completions.parse(
                model=self.llm_config.model_name,
                messages=[
                    {"role": "system", "content": system_prompt or "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                response_format=response_format,
            )
            
            # Track usage
            if self.execution_log and response.usage:
                self.execution_log.llm_calls += 1
                self.execution_log.total_tokens += response.usage.total_tokens
            
            return response.choices[0].message.parsed.model_dump()
        else:
            # Fallback to regular JSON parsing
            import json
            response_text = await self.call_llm(
                prompt=f"{prompt}\n\nRespond with valid JSON only.",
                system_prompt=system_prompt,
            )
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                raise ValueError(f"LLM did not return valid JSON: {response_text[:200]}")
    
    def log_reasoning(self, step: str, decision: Any = None):
        """
        Log agent reasoning for observability
        
        Args:
            step: Description of reasoning step
            decision: Optional decision data
        """
        if self.execution_log:
            self.execution_log.reasoning_steps.append(step)
            if decision is not None:
                self.execution_log.decisions_made[step] = decision
        
        self.logger.info(f"Reasoning: {step}")
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of execution metrics"""
        if not self.execution_log:
            return {}
        
        return {
            "agent": self.agent_name,
            "duration_seconds": self.execution_log.duration_seconds,
            "llm_calls": self.execution_log.llm_calls,
            "total_tokens": self.execution_log.total_tokens,
            "cost_usd": round(self.execution_log.cost_usd, 4),
            "success": self.execution_log.success,
        }


class MockAgent(BaseAgent[InputType, OutputType]):
    """
    Mock agent for testing orchestrator
    Returns predefined output without real processing
    """
    
    def __init__(self, agent_name: str, mock_output: OutputType):
        super().__init__(agent_name)
        self.mock_output = mock_output
    
    async def process(self, input_data: InputType) -> OutputType:
        """Return mock output"""
        self.logger.info("Returning mock output")
        await self._simulate_processing()
        return self.mock_output
    
    async def _simulate_processing(self):
        """Simulate processing delay"""
        import asyncio
        await asyncio.sleep(0.1)  # Small delay to simulate work
