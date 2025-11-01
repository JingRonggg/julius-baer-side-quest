"""
Money Transfer API Client

This module provides functionality to transfer money between accounts
using a REST API endpoint.

Author: jingronggg
Date: November 2025
"""

import logging
import os
from decimal import Decimal
from typing import Optional, Dict, Any
from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging with more detailed formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


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


def transfer_money(
    from_acc: str,
    to_acc: str,
    amount: float,
    config: Optional[TransferConfig] = None
) -> Optional[Dict[str, Any]]:
    """
    Transfer money from one account to another via API.
    
    Makes a POST request to the transfer endpoint with account and amount
    information. Handles HTTP errors and connection issues gracefully with
    automatic retries and comprehensive error logging.
    
    Args:
        from_acc: Source account identifier (e.g., "ACC1000")
        to_acc: Destination account identifier (e.g., "ACC1001")
        amount: Amount to transfer in the account's currency
        config: Optional TransferConfig object. If None, loads from environment.
    
    Returns:
        JSON response from the API containing transfer confirmation,
        or None if the request failed
    
    Raises:
        ValueError: If amount is negative or accounts are invalid
    
    Example:
        >>> config = TransferConfig.from_environment()
        >>> result = transfer_money("ACC1000", "ACC1001", 100.00, config)
        >>> if result:
        ...     print(f"Transfer successful: {result['transactionId']}")
    """
    # Validate inputs
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got: {amount}")
    
    if not from_acc or not to_acc:
        raise ValueError("Account identifiers cannot be empty")
    
    if from_acc == to_acc:
        raise ValueError("Cannot transfer to the same account")
    
    # Load configuration
    if config is None:
        config = TransferConfig.from_environment()
    
    # API endpoint for money transfers
    url = f"{config.api_url}/transfer"
    
    # Prepare request payload
    data = {
        "fromAccount": from_acc,
        "toAccount": to_acc,
        "amount": amount
    }
    
    logger.info(
        f"Initiating transfer: {from_acc} -> {to_acc}, "
        f"amount: ${amount:.2f}"
    )
    
    try:
        # Create session with retry logic
        session = create_session_with_retries(config)
        
        # Send POST request to transfer endpoint
        response = session.post(
            url,
            json=data,
            timeout=config.timeout,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "MoneyTransferClient/1.0"
            }
        )
        
        # Raise exception for HTTP error status codes (4xx, 5xx)
        response.raise_for_status()
        
        # Parse and return JSON response
        result = response.json()
        logger.info(
            f"Transfer successful - Transaction ID: {result.get('transactionId', 'N/A')}"
        )
        return result
        
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 400 Bad Request, 500 Server Error)
        error_detail = e.response.text if e.response else "No response"
        logger.error(
            f"HTTP error {e.response.status_code if e.response else 'N/A'}: "
            f"{error_detail}"
        )
        return None
        
    except requests.exceptions.Timeout as e:
        # Handle timeout errors
        logger.error(f"Request timed out after {config.timeout}s: {str(e)}")
        return None
        
    except requests.exceptions.ConnectionError as e:
        # Handle connection errors
        logger.error(f"Connection error - unable to reach API at {url}: {str(e)}")
        return None
        
    except requests.exceptions.RequestException as e:
        # Handle other request-related exceptions
        logger.error(f"Request failed with exception: {str(e)}")
        return None
        
    except ValueError as e:
        # Handle JSON parsing errors
        logger.error(f"Failed to parse response JSON: {str(e)}")
        return None
        
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error occurred: {type(e).__name__} - {str(e)}")
        return None
    
    finally:
        # Ensure session is closed
        if 'session' in locals():
            session.close()


def main() -> None:
    """Main execution function with example usage."""
    # Load configuration from environment
    config = TransferConfig.from_environment()
    
    logger.info("Starting money transfer client...")
    logger.info(f"API URL: {config.api_url}")
    
    # Example usage: Transfer $100 from ACC1000 to ACC1001
    result = transfer_money("ACC1000", "ACC1001", 100.00, config)
    
    if result:
        logger.info(f"Transfer completed successfully: {result}")
    else:
        logger.error("Transfer failed - check logs above for details")


# Main execution block
if __name__ == "__main__":
    main()