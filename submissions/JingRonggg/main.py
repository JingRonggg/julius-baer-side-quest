"""Money Transfer Client - Main Entry Point."""

import logging
import colorlog
from config import TransferConfig
from cli import run_interactive_cli
from auth import get_jwt_token

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))
logging.basicConfig(level=logging.INFO, handlers=[handler])


def main() -> None:
    """
    Main execution function for the money transfer client.

    Prompts the user for authentication details, retrieves a JWT token,
    and starts the interactive CLI.

    Raises:
        Exception: If authentication fails or invalid inputs are provided.
    """
    config = TransferConfig.from_environment()

    # Prompt for username, password, and claim type
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    claim = input("Enter claim type (enquiry/transfer): ").strip().lower()

    if claim not in ["enquiry", "transfer"]:
        logging.error("Invalid claim type. Please enter 'enquiry' or 'transfer'.")
        return

    try:
        jwt_token = get_jwt_token(config.api_url, username, password, claim=claim)
        logging.info("Authentication successful. JWT token retrieved.")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return

    # Pass the JWT token to the CLI or other components as needed
    run_interactive_cli(config, jwt_token=jwt_token)


if __name__ == "__main__":
    main()