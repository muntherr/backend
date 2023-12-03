from fastapi.encoders import jsonable_encoder
from pydantic import Field
from pydantic.main import BaseModel
from typing import List

class Instructor(BaseModel):
    id: str = Field(None, alias="_id")
    firstName: str  
    lastName: str  
    department: str  
    phoneNumber: int  
    courses: List[str]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.model_dump(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data
    
    
    
