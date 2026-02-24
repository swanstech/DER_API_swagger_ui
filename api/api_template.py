# This file shows a template for creating an api following the coventions.

# below are all necessary packages needs to be included
from fastapi import APIRouter, Form, HTTPException
import requests


# name the template as you wish, the tags will be the new apis group title, and prefix will be the most initial dir for this group of apis
template = APIRouter(prefix="/template", tags=["template"])

# please follow the covention below
# app apis belongs to the same group should be all included in one file
# the template.get means the api template will have a get request with the dir "/get_template"
@template.get("/get_template")
def get_template():

    """
    This is a get API template
    """

    return {"message": "create template"}


# there are two ways to add documentation to an API:
# 1. following the below parameters
# 2. use the doc strings in Python, please back to the previous api for any reference
@template.post(
        "/try_post",
        description="This is a post template",
        response_description="This is a template for doc response"
        )
def get_template():
    return {"message": "try out the post request"}


# then after all of the setup in this file
# if this file is first created, we should go to main.py to register the router
# now move to the main.py in the root dir, there will be the rest of the tutorials