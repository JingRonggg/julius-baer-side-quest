# Banking Client Solution

## Language
Python 3.13+ (compatible with Python 3.10+)

## Features

#### **1. Language Modernization (🌟 Standard Bonus)** [DONE]
#### **2. HTTP Client Modernization (🌟 Standard Bonus)** [DONE]
#### **3. Error Handling & Logging (🌟 Standard Bonus)** [DONE]
#### **4. Security & Authentication (🏆 Maximum Bonus)**
#### **5. Code Architecture & Design Patterns (🏆 Maximum Bonus)**
#### **6. Modern Development Practices (🏆 Maximum Bonus)**
#### **7. DevOps & Deployment (🏆🏆 Premium Bonus)**
#### **8. User Experience & Interface (🏆🏆 Premium Bonus)**
#### **9. Performance & Scalability (🏆🏆 Premium Bonus)**

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

API ENDPOINTS:
/authToken