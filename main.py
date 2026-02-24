from fastapi import FastAPI
from api.get_pentest_results import pentest as pentest_router
from api.get_token import token as swanstech_token_router
from api.get_wallbox import wallbox as wallbox_router

# by following the template, please add the router for the template like below
# the template below is the name of the api we just setup
from api.api_template import template as template_router

app = FastAPI(title="DER Dashboard APIs Overview", tags=["connect"])


@app.get(
        "/",
        description="This API is used for initialisation testing",
        response_description="The response demonstrate a successful API buildup"
         )
def root():
    return {"message": "Hello World"}


app.include_router(pentest_router)
app.include_router(swanstech_token_router)
app.include_router(wallbox_router)

# then add the router by following the above naming convention
app.include_router(template_router)
# after this, we will see a new group of apis in template
# anytime after changes, please test at local first, before push

# start the new code below

