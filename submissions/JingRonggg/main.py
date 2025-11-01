"""Money Transfer Client - Main Entry Point."""

import logging

from config import TransferConfig
from cli import run_interactive_cli

# Configure logging with more detailed formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main() -> None:
    """Main execution function."""
    config = TransferConfig.from_environment()
    run_interactive_cli(config)


if __name__ == "__main__":
    main()