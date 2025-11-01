# Available API Endpoints

## POST /authToken

Generates a JWT token with specified claims/scopes. Use `?claim=transfer` for transfer operations, default is `enquiry`.

### Parameters

| Name   | Type   | Location | Description                                      |
|--------|--------|----------|--------------------------------------------------|
| `claim` | string | query    | Claim/scope for the token: `'enquiry'` (default) or `'transfer'` |

### Request Body

**Content-Type:** `application/json`

```json
{
  "username": "alice",
  "password": "password123"
}
```

### Responses

#### 200 - Success

JWT token successfully generated.

**Content-Type:** `application/json`

**Example Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "username": "alice",
  "scope": "enquiry",
  "permissions": "enquiry",
  "expiresAt": "2024-01-01T12:00:00Z"
}
```

#### 400 - Bad Request

Invalid request body.

**Example Response:**

```json
{
  "error": "Invalid credentials or malformed request"
}
```

---

## GET /accounts

Returns 100 valid accounts with their balances. JWT token optional but earns bonus points!

### Parameters

| Name          | Type   | Location | Description                                   |
|---------------|--------|----------|-----------------------------------------------|
| Authorization | string | header   | JWT token (optional - bonus points if provided) |

### Example Request

```bash
curl -X 'GET' \
  'http://localhost:8123/accounts' \
  -H 'accept: application/json'
```

### Example Response

```json
{
  "bonusPoints": "💡 Hint: Use JWT token in Authorization header for bonus points!",
  "accounts": [
    {
      "id": "ACC1030",
      "balance": 1000
    },
    {
      "id": "ACC1031",
      "balance": 1000
    }
    // ...remaining accounts...
  ],
  "totalAccounts": 100
}
```

---

## GET /accounts/validate/{accountId}

Checks if the given account ID is valid/active. JWT token optional but earns bonus points!

### Parameters

| Name          | Type   | Location | Description                                   |
|---------------|--------|----------|-----------------------------------------------|
| `accountId`   | string | path     | The account ID to validate.                  |
| Authorization | string | header   | JWT token (optional - bonus points if provided) |

---

## GET /accounts/balance/{accountId}

Returns the current balance of a specific account. JWT token optional but earns bonus points!

### Parameters

| Name          | Type   | Location | Description                                   |
|---------------|--------|----------|-----------------------------------------------|
| `accountId`   | string | path     | The account ID to retrieve the balance for.  |
| Authorization | string | header   | JWT token (optional - bonus points if provided) |

---

## POST /transfer

🏦 **Transfer Funds (Core Challenge Endpoint)**

Transfers funds between accounts.

- ✅ Works without authentication (minimum requirement).
- 🌟 JWT token earns bonus points!

### Challenge Requirements

- Implement HTTP client to call this endpoint.
- Handle success/failure responses.
- Use valid account IDs (`ACC1000-ACC1099`).
- Add JWT authentication for bonus points.

💡 **Bonus Points:**
- Include `Authorization: Bearer <token>` header.
- Use transfer token (`?claim=transfer`) for maximum points.

### Parameters

| Name          | Type   | Location | Description                                   |
|---------------|--------|----------|-----------------------------------------------|
| Authorization | string | header   | JWT token for bonus points. Format: `Bearer <token>` |

### Request Body

**Content-Type:** `application/json`

```json
{
  "fromAccount": "ACC1000",
  "toAccount": "ACC1001",
  "amount": 150
}
```

### Responses

#### 200 - Success

**Example Response:**

```json
{
  "transactionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "SUCCESS",
  "message": "Transfer completed successfully",
  "fromAccount": "ACC1000",
  "toAccount": "ACC1001",
  "amount": 100,
  "bonusPoints": "🌟 JWT Authentication Bonus!"
}
```

#### 400 - Invalid Request

**Example Response:**

```json
{
  "status": "FAILED",
  "message": "Invalid account format",
  "errors": [
    "fromAccount must match pattern ACC[0-9]{4}"
  ]
}
```

---

## GET /transactions/history

Returns recent transaction history. JWT token required for this bonus endpoint!

### Parameters

| Name          | Type    | Location | Description                                   |
|---------------|---------|----------|-----------------------------------------------|
| Authorization | string  | header   | JWT token (required for this endpoint).      |
| `limit`       | integer | query    | Number of transactions to retrieve (default: 10, max: 20). |

### Example Response

```json
{
  "transactions": [
    {
      "transactionId": "tx123",
      "fromAccount": "ACC1000",
      "toAccount": "ACC1001",
      "amount": 150,
      "timestamp": "2025-11-01T11:11:12Z"
    }
    // ...remaining transactions...
  ]
}
```