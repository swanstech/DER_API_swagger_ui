from fastapi import FastAPI
from api.pentest_results import router as pentest_router

app = FastAPI(title="DER Dashboard APIs Overview")


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(pentest_router)
