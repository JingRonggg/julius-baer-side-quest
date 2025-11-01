# Banking Client Solution

## Language
Python 3.13+ (compatible with Python 3.10+)

## Features

✨ **Modern Python 3.x Implementation**
- Type hints for better code clarity and IDE support
- F-strings for clean string formatting
- Dataclasses for configuration management
- Context managers for resource cleanup

🔒 **Robust Error Handling**
- Comprehensive exception handling for all error types
- Detailed logging with timestamps
- Input validation for transfer parameters
- Graceful degradation on failures

🔄 **Automatic Retry Logic**
- Configurable retry attempts with exponential backoff
- Handles transient failures (500, 502, 503, 504, 429)
- Session management with connection pooling

⚙️ **Configuration Management**
- Environment variable support
- Sensible defaults for all settings
- Easy customization via `.env` file

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure (Optional)
Copy `.env.example` to `.env` and customize if needed:
```bash
cp .env.example .env
```

Available configuration options:
- `TRANSFER_API_URL`: API endpoint (default: http://localhost:8123)
- `TRANSFER_TIMEOUT`: Request timeout in seconds (default: 30)
- `TRANSFER_MAX_RETRIES`: Maximum retry attempts (default: 3)
- `TRANSFER_BACKOFF_FACTOR`: Retry backoff factor (default: 0.3)

## Run

### Basic Usage
```bash
python main.py
```

### Programmatic Usage
```python
from main import transfer_money, TransferConfig

# Use default configuration
result = transfer_money("ACC1000", "ACC1001", 100.00)

# Use custom configuration
config = TransferConfig(
    api_url="http://api.example.com:8080",
    timeout=60,
    max_retries=5
)
result = transfer_money("ACC1000", "ACC1001", 250.50, config)

if result:
    print(f"Success! Transaction ID: {result['transactionId']}")
else:
    print("Transfer failed - check logs")
```

## Code Quality

- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ PEP 8 compliant
- ✅ Defensive programming with input validation
- ✅ Production-ready error handling
- ✅ Structured logging

## Error Handling

The client handles various error scenarios:
- **HTTP Errors**: 4xx/5xx responses with detailed logging
- **Timeouts**: Configurable timeout with retry logic
- **Connection Errors**: Network issues, DNS failures
- **Invalid Input**: Negative amounts, empty accounts, same account transfers
- **JSON Errors**: Malformed API responses

All errors are logged with contextual information for debugging.
