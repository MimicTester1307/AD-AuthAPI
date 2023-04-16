# handles converting various non-JSON types between JSON types and Python types
from fastapi.encoders import jsonable_encoder

# Pydantic and Python's built-in typing are used to define a schema
# that defines the structure and types of the different objects stored
# in the Staff and Student collections managed by this API
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

from .objectid import PydanticObjectId


class Student(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    # slug: str    # a unique, URL-safe mnemonic used for identifying a document
    student_id: int
    email: str
    password: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data


class Staff(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    # slug: str
    staff_id: int
    email: str
    password: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data
