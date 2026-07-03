from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class CloudTrailEvent(BaseModel):
    username:str
    age:int


data ={"username":"muhammad", "age":"Thirty"}

user = CloudTrailEvent(**data)

print(user.username,user.age)