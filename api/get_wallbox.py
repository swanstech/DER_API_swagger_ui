from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, Field
import base64
import requests

wallbox = APIRouter(prefix="/wallbox", tags=["wallbox"])

# --- Wallbox config ---
BASE_URL = "https://api.wall-box.com"
TOKEN_PATH = "auth/token/user"


class WallboxRequest(BaseModel):
    username: str
    password: str


@wallbox.post("/get_token", tags=["wallbox"])
def wallbox_token(req: WallboxRequest):
    """
    Authenticate with Wallbox API and return JWT token.
    """

    # Build URL
    url = f"{BASE_URL.rstrip('/')}/{TOKEN_PATH.lstrip('/')}"

    # Encode Basic Auth
    auth_string = f"{req.username}:{req.password}"
    auth_b64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=utf-8"
    }

    try:
        response = requests.post(url, headers=headers, timeout=20)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Network error: {str(e)}")

    if not response.ok:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Wallbox error: {response.text}"
        )

    data = response.json()
    token = data.get("jwt")

    if not token:
        raise HTTPException(
            status_code=500,
            detail=f"JWT missing in Wallbox response: {data}"
        )

    return {"jwt": token}



@wallbox.post("/get_chargerslist", tags=["wallbox"])
def wallbox_charger_groups(req: WallboxRequest, token):
    """
    Call Wallbox: GET https://api.wall-box.com/v3/chargers/groups
    using Basic Auth (username:password) and return the JSON response.
    """
    jwt_token = token

    if not jwt_token:
        if not req.username or not req.password:
            raise HTTPException(
                status_code=400,
                detail="Either provide a token OR username and password."
            )

        token_url = "https://api.wall-box.com/auth/token"

        auth_string = f"{req.username}:{req.password}"
        auth_b64 = base64.b64encode(
            auth_string.encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            token_response = requests.post(
                token_url, headers=headers, timeout=20)
        except requests.RequestException as e:
            raise HTTPException(
                status_code=502, detail=f"Token request failed: {str(e)}")

        if not token_response.ok:
            raise HTTPException(
                status_code=token_response.status_code,
                detail=f"Wallbox token error: {token_response.text}"
            )

        token_data = token_response.json()
        jwt_token = token_data.get("jwt")

        if not jwt_token:
            raise HTTPException(
                status_code=500,
                detail=f"JWT missing in token response: {token_data}"
            )

    # Step 2: Call charger groups API
    chargers_url = "https://api.wall-box.com/v3/chargers/groups"

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(chargers_url, headers=headers, timeout=20)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Network error: {str(e)}")

    if not response.ok:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Wallbox error: {response.text}"
        )

    return response.json()
