from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from typing import List
from core.services import twitter_janitor
from db.storage import *
from models.message import *
import time

router = APIRouter()


@router.get("/profile/{id}", response_description="Clean profile tweets")
async def clean_by_profile(id:str):
    data = await get_dirty_twitter(id)
    if len(data)>0:
        cleared_data = twitter_janitor.clean(data)
        clean_data = await save_cleared_twitter(cleared_data)
        return ResponseModel(clean_data, "Profile mined successfully.")
    else:
        return ResponseModel([], "No new data")

@router.get("/inspection/", response_description="Check db for not prepared data")
async def inspect():
    json_responce=miner.get_profile_data(username=id)
    return ResponseModel(added_profile, "Profile mined successfully.")


