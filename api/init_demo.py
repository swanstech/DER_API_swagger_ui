from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["pentest"])


@router.get("/demo")
def pentest_hello():
    return {"message": "Hello World for this demo"}
