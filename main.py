import uvicorn
from fastapi import FastAPI, Body, Depends, Form

from internal.controller import FormController
from internal.storage import storage
from fill_db import fill_db

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.con.drop_tables()
    fill_db(storage.con)
    yield


app = FastAPI(title="form_checker", lifespan=lifespan)


@app.post("/get_form")
def get_form(
    req_str: str = Form(...),
    controller: FormController = Depends(FormController),
):
    return controller.validate_filled_form(req_str=req_str)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")
