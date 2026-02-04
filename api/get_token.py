from fastapi import APIRouter, Form, HTTPException
import requests

token = APIRouter(prefix="/token", tags=["token"])

TOKEN_URL = "https://3.104.109.16:8443/auth/realms/swanstech/protocol/openid-connect/token"

@token.post("/get_token")
def get_token(
    username: str = Form(...),
    password: str = Form(...),
):
    payload = {
        "client_id": "frontend-client",
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    try:
        response = requests.post(
            TOKEN_URL,
            data=payload,  # x-www-form-urlencoded
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            verify=False,  # local / self-signed cert only
            timeout=10,
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return response.json()
