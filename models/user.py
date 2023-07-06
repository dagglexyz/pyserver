import jwt
from typing import Optional
import constants
from pydantic import BaseModel, Field


class User(BaseModel):
    address: str = Field()
    tokens: list[str] = Field(default=[])

    def createToken(self, address: str, signature: str):
        encoded_jwt = jwt.encode(
            {"address": address, "signature": signature},
            constants.env["JWT_SECRET"],
            algorithm="HS256",
        )
        self.tokens.append(encoded_jwt)
