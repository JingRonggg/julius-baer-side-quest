"""Configuration management for money transfer client."""

import os
from dataclasses import dataclass


@dataclass
class TransferConfig:
    """
    Configuration for money transfer API client.
    
    Binary exponential backoff formula: backoff_factor * (2^retry_number)
    With backoff_factor=1.0:
    - Retry 1: 1s delay
    - Retry 2: 2s delay
    - Retry 3: 4s delay
    - Retry 4: 8s delay
    """
    api_url: str
    timeout: int = 30
    max_retries: int = 3
    backoff_factor: float = 1.0  # Binary exponential backoff (1s, 2s, 4s, 8s...)
    
    @classmethod
    def from_environment(cls) -> 'TransferConfig':
        """Create configuration from environment variables with defaults."""
        return cls(
            api_url=os.getenv('TRANSFER_API_URL', 'http://localhost:8123'),
            timeout=int(os.getenv('TRANSFER_TIMEOUT', '30')),
            max_retries=int(os.getenv('TRANSFER_MAX_RETRIES', '3')),
            backoff_factor=float(os.getenv('TRANSFER_BACKOFF_FACTOR', '1.0'))
        )
