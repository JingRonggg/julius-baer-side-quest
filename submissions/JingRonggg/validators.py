"""Input validation utilities for money transfer operations."""


def validate_transfer_inputs(from_acc: str, to_acc: str, amount: float) -> None:
    """
    Validate transfer input parameters.

    Args:
        from_acc (str): Source account identifier.
        to_acc (str): Destination account identifier.
        amount (float): Transfer amount.

    Raises:
        ValueError: If any validation fails.
    """
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got: {amount}")
    
    if not from_acc or not to_acc:
        raise ValueError("Account identifiers cannot be empty")
    
    if from_acc == to_acc:
        raise ValueError("Cannot transfer to the same account")


def parse_amount(amount_str: str) -> float:
    """
    Parse and validate amount string.

    Args:
        amount_str (str): String representation of amount.

    Returns:
        float: Parsed float amount.

    Raises:
        ValueError: If amount string is invalid.
    """
    try:
        return float(amount_str)
    except ValueError:
        raise ValueError(f"Invalid amount: '{amount_str}'. Please enter a valid number.")
