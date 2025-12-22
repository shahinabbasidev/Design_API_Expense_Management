from fastapi import FastAPI,HTTPException,status
from fastapi.responses import JSONResponse
import random
from schemas import PersonCreateSchema,PersonResponseSchema,PersonUpdateSchema
from typing import List


app = FastAPI()


expenses_list = []


@app.post("/expenses",response_model=PersonResponseSchema)
def create_expense(person:PersonCreateSchema):
    expense_obj = {"id":random.randint(1,1000),"title":person.title,"mount": person.mount}
    expenses_list.append(expense_obj)
    return JSONResponse(content=expense_obj,status_code=status.HTTP_201_CREATED)

@app.get("/expenses",response_model=list[PersonResponseSchema])
def get_all_expenses():
    return expenses_list


@app.get("/expenses/{id}",response_model=PersonResponseSchema)
def get_expense(id:int):
    for item in expenses_list:
        if item["id"] == id:
            return JSONResponse(content=item,status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

@app.put("/expenses/{id}",response_model=PersonResponseSchema)
def update_list(id:int,person:PersonUpdateSchema):
    for item in expenses_list:
        if item["id"] == id:
            item["title"] = person.title
            return JSONResponse(content={"detail":"object update successfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.delete("/expenses/{id}")
def delete_title(id:int):
    for item in expenses_list:
        if item["id"] == id:
            expenses_list.remove(item)
            return JSONResponse(content={"detail":"object remove successfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



