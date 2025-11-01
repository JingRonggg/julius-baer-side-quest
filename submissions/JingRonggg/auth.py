import requests

def get_jwt_token(api_url: str, username: str, password: str, claim: str = "enquiry") -> str:
    """
    Authenticate with the API and retrieve a JWT token.

    Args:
        api_url (str): Base URL of the API.
        username (str): Username for authentication.
        password (str): Password for authentication.
        claim (str): Claim/scope for the token (default: "enquiry").

    Returns:
        str: JWT token if authentication is successful.

    Raises:
        Exception: If authentication fails or the request is invalid.
    """
    auth_url = f"{api_url}/authToken?claim={claim}"
    response = requests.post(auth_url, json={"username": username, "password": password})

    if response.status_code == 200:
        return response.json().get("token")
    else:
        raise Exception(f"Authentication failed: {response.json().get('error', 'Unknown error')}")
