from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from models.user import User
from web3 import Web3
from eth_account.messages import defunct_hash_message
from database.db import db
from pymongo import ReturnDocument


router = APIRouter(
    prefix="/user",
    responses={404: {"message": "Not found"}},
)
w3 = Web3()


@router.post("/signin")
async def signin(request: Request):
    try:
        body = await request.json()
        # https://ethereum.stackexchange.com/questions/55003/recover-javascript-signed-message-in-python-web3
        message_hash = defunct_hash_message(
            text=f"Please approve this message \n \nNonce:\n{body['nonce']}"
        )
        address = w3.eth.account._recover_hash(message_hash, signature=body["sign"])

        user = db.user.find_one({"address": address})

        if user is not None:
            user = User(**user)
            user.createToken(address=address, signature=body["sign"])
            db.user.find_one_and_update(
                {"address": user.address},
                {"$set": jsonable_encoder(user)},
                return_document=ReturnDocument.AFTER,
            )
        else:
            user = User(address=address)
            user.createToken(address=address, signature=body["sign"])
            db.user.insert_one(jsonable_encoder(user))
            user = jsonable_encoder(user)
        return user
    except Exception as e:
        return {"message": str(e)}
