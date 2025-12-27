from fastapi import FastAPI,HTTPException,status,Depends,Query
from fastapi.responses import JSONResponse
import random
from schemas import PersonCreateSchema,PersonResponseSchema,PersonUpdateSchema
from contextlib import asynccontextmanager
from typing import List,Annotated
from database import Base,engine,get_db,User,Expense
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(engine)
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(lifespan = lifespan)

expenses_list = []


@app.post("/expenses",response_model=PersonResponseSchema)
def create_expense( request:PersonCreateSchema,db:Session = Depends(get_db)):
    # expense_obj = {"id":random.randint(1,1000),"title":person.title,"mount": person.mount}
    # expenses_list.append(expense_obj)
    new_person = User(first_name = request.first_name,last_name = request.last_name,age = request.age)
    new_expense = Expense(expense_name = request.expense_name,mount = request.mount)
    db.add(new_person)
    db.add(new_expense)
    db.close()
    return new_person

@app.get("/expenses",response_model=list[PersonResponseSchema])
def get_all_expenses(q:Annotated[str | None, Query(max_length=30)] = None,db:Session = Depends(get_db)):

    query = db.query(User)
    if q:
        query = query.filter_by(User.first_name == q)
    result = query.all()
    return result


@app.get("/expenses/{id}",response_model=PersonResponseSchema)
def get_expense(id:int,db:Session = Depends(get_db)):
    # for item in expenses_list:
    #     if item["id"] == id:
    #         return JSONResponse(content=item,status_code=status.HTTP_200_OK)
    person = db.query(User).filter_by(id=id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

@app.put("/expenses/{id}",response_model=PersonResponseSchema)
def update_list(id:int,request:PersonUpdateSchema,db:Session = Depends(get_db)):
    # for item in expenses_list:
    #     if item["id"] == id:
    #         item["title"] = person.title
    #         return JSONResponse(content={"detail":"object update successfully"},status_code=status.HTTP_200_OK)
    person = db.query(User).filter_by(id=id).one_or_none()
    if person:
        person.first_name = request.first_name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.delete("/expenses/{id}")
def delete_title(id:int,db:Session = Depends(get_db)):
    person = db.query(User).filter_by(id=id).one_or_none
    if person:
            db.delete(person)
            db.commit()
            return JSONResponse(content={"detail":"object remove successfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



