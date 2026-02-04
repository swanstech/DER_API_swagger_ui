from fastapi import APIRouter

demo = APIRouter(prefix="/demo", tags=["demo"])


@demo.get("/hello")
def demo_hello():
    return {"message": "Hello World for this demo"}
