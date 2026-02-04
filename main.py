from fastapi import FastAPI
from api.pentest_results import pentest as pentest_router
from api.init_demo import demo as demo_router

app = FastAPI(title="DER Dashboard APIs Overview")


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(pentest_router)
app.include_router(demo_router)
