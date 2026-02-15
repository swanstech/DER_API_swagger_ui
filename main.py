from fastapi import FastAPI
from api.get_pentest_results import pentest as pentest_router
from api.get_token import token as demo_router

app = FastAPI(title="DER Dashboard APIs Overview", tags=["connect"])


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(pentest_router)
app.include_router(demo_router)
