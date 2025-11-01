"""HTTP client management with retry logic."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import TransferConfig


def create_session_with_retries(config: TransferConfig) -> requests.Session:
    """
    Create a requests session with retry strategy.
    
    Args:
        config: Transfer configuration object
    
    Returns:
        Configured requests.Session with retry logic
    """
    session = requests.Session()
    
    retry_strategy = Retry(
        total=config.max_retries,
        backoff_factor=config.backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session
