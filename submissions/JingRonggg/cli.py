"""Command-line interface for money transfer system."""

import logging

from config import TransferConfig
from transfer import transfer_money
from validators import parse_amount

logger = logging.getLogger(__name__)


def run_interactive_cli(config: TransferConfig, jwt_token=None) -> None:
    """
    Run interactive command-line interface for transfers.
    
    Args:
        config: Transfer configuration object
        jwt_token: Optional JWT token for authenticated requests.
    """
    logger.info("Starting money transfer client...")
    logger.info(f"API URL: {config.api_url}")
    
    # Continuous loop for processing transfers
    while True:
        try:
            print("\n" + "="*50)
            print("Money Transfer System")
            print("="*50)
            
            # Get account and amount details from user
            from_acc = input("Enter source account (or 'quit' to exit): ").strip()
            
            # Allow user to exit the loop
            if from_acc.lower() in ['quit', 'exit', 'q']:
                logger.info("Exiting money transfer client...")
                break
            
            to_acc = input("Enter destination account: ").strip()
            amount_str = input("Enter amount to transfer: ").strip()
            
            # Validate and convert amount
            try:
                amount = parse_amount(amount_str)
            except ValueError as e:
                logger.error(str(e))
                continue
            
            # Attempt the transfer
            result = transfer_money(from_acc, to_acc, amount, config, jwt_token=jwt_token)
            
            if result:
                logger.info(f"Transfer completed successfully: {result}")
                print(f"\n✓ Transfer successful! Transaction ID: {result.get('transactionId', 'N/A')}")
            else:
                logger.error("Transfer failed - check logs above for details")
                print("\n✗ Transfer failed. Please try again.")
                
        except KeyboardInterrupt:
            logger.info("\nReceived keyboard interrupt. Exiting...")
            break
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            print(f"\n✗ Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {type(e).__name__} - {str(e)}")
            print(f"\n✗ Unexpected error: {str(e)}")
    
    print("\nThank you for using the Money Transfer System!")
