"""Configuration management for money transfer client."""

import os
from dataclasses import dataclass


@dataclass
class TransferConfig:
    """Configuration for money transfer API client."""
    api_url: str
    timeout: int = 30
    max_retries: int = 3
    backoff_factor: float = 0.3
    
    @classmethod
    def from_environment(cls) -> 'TransferConfig':
        """Create configuration from environment variables with defaults."""
        return cls(
            api_url=os.getenv('TRANSFER_API_URL', 'http://localhost:8123'),
            timeout=int(os.getenv('TRANSFER_TIMEOUT', '30')),
            max_retries=int(os.getenv('TRANSFER_MAX_RETRIES', '3')),
            backoff_factor=float(os.getenv('TRANSFER_BACKOFF_FACTOR', '0.3'))
        )
