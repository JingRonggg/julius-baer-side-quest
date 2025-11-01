"""Money transfer API operations."""

import logging
from typing import Optional, Dict, Any

import requests

from config import TransferConfig
from client import create_session_with_retries
from validators import validate_transfer_inputs

logger = logging.getLogger(__name__)


def transfer_money(
    from_acc: str,
    to_acc: str,
    amount: float,
    config: Optional[TransferConfig] = None,
    jwt_token: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Transfer money from one account to another via API.

    Args:
        from_acc (str): Source account identifier.
        to_acc (str): Destination account identifier.
        amount (float): Amount to transfer in the account's currency.
        config (Optional[TransferConfig]): Transfer configuration object.
        jwt_token (Optional[str]): Optional JWT token for authenticated requests.

    Returns:
        Optional[Dict[str, Any]]: JSON response from the API containing transfer confirmation,
        or None if the request failed.

    Raises:
        ValueError: If amount is negative or accounts are invalid

    Example:
        >>> config = TransferConfig.from_environment()
        >>> result = transfer_money("ACC1000", "ACC1001", 100.00, config)
        >>> if result:
        ...     print(f"Transfer successful: {result['transactionId']}")
    """
    # Validate inputs
    validate_transfer_inputs(from_acc, to_acc, amount)

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
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MoneyTransferClient/1.0"
        }
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"

        response = session.post(
            url,
            json=data,
            timeout=config.timeout,
            headers=headers
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
