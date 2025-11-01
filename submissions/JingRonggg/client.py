"""HTTP client management with retry logic."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import TransferConfig


def create_session_with_retries(config: TransferConfig) -> requests.Session:
    """
    Create a requests session with binary exponential backoff retry strategy.
    
    Binary exponential backoff means retry delays double with each attempt:
    - 1st retry: backoff_factor * (2^0) = 1s
    - 2nd retry: backoff_factor * (2^1) = 2s
    - 3rd retry: backoff_factor * (2^2) = 4s
    - 4th retry: backoff_factor * (2^3) = 8s
    
    Args:
        config: Transfer configuration object
    
    Returns:
        Configured requests.Session with binary exponential backoff retry logic
    """
    session = requests.Session()
    
    retry_strategy = Retry(
        total=config.max_retries,
        backoff_factor=config.backoff_factor,  # Binary exponential: delays = 1s, 2s, 4s, 8s...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
        raise_on_status=False  # Don't raise on retry exhaustion
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session
