from pydantic import BaseModel


class BasePersonSchema(BaseModel):

    title : str
    mount : int

class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):

    id : int

class PersonUpdateSchema(BasePersonSchema):
    pass
