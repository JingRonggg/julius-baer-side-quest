"""Configuration management for money transfer client."""

import os
from dataclasses import dataclass


@dataclass
class TransferConfig:
    """
    Configuration for money transfer API client.

    Attributes:
        api_url (str): API endpoint URL.
        timeout (int): Request timeout in seconds.
        max_retries (int): Maximum number of retry attempts.
        backoff_factor (float): Binary exponential backoff factor.
    """
    api_url: str
    timeout: int = 30
    max_retries: int = 3
    backoff_factor: float = 1.0  # Binary exponential backoff (1s, 2s, 4s, 8s...)
    
    @classmethod
    def from_environment(cls) -> 'TransferConfig':
        """
        Create configuration from environment variables with defaults.

        Returns:
            TransferConfig: Configuration object populated from environment variables.
        """
        return cls(
            api_url=os.getenv('TRANSFER_API_URL', 'http://localhost:8123'),
            timeout=int(os.getenv('TRANSFER_TIMEOUT', '30')),
            max_retries=int(os.getenv('TRANSFER_MAX_RETRIES', '3')),
            backoff_factor=float(os.getenv('TRANSFER_BACKOFF_FACTOR', '1.0'))
        )
