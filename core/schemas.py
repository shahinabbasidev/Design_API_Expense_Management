from pydantic import BaseModel, field_validator, Field, field_serializer
import re


class BasePersonSchema(BaseModel):

    title : str = Field(...,description="Enter your expenses name")
    mount : float = Field(..., gt=0, description="Must be a positive number")

    @field_validator("title")
    def validate_title(cls,value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z0-9_]+$",value):
            raise ValueError("Title can contain only letters, numbers, and underscore (_)")
        return value


    @field_serializer("title")
    def serialize_name(self,value):
        return value.title()
    


class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):

    id : int 

class PersonUpdateSchema(BasePersonSchema):
    pass
