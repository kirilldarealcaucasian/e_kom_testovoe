from fastapi import HTTPException, status
from typing import Union
from tinydb import Query
from internal.storage import storage
from internal.form_validator import FormValidator
from pydantic import ValidationError


class FormController:
    def __init__(
        self,
    ):
        self.db_con = storage.con

    def validate_filled_form(self, req_str: str) -> Union[str, dict]:
        data = req_str.split("&")
        form_data = {
            v.split("=")[0]: v.split("=")[1] for v in data
        }  # ex. key=value -> {key:value}

        query_fields: list[str] = list(form_data.keys())
        res: Union[list[dict], None] = None

        while len(query_fields) > 0:  # exclude 1 field until appropriate form is found
            res = storage.get_all_by_fields(
                query_fields
            )  # select form template such that all fields in form are contained in form_data
            if not res:
                query_fields.pop()
            else:
                break

        to_validate = dict()

        if res:
            for field_name, field_value in res[
                0
            ].items():  # assemble dict to validate against pydantic model
                if field_name != "name" and field_name in form_data.keys():
                    to_validate[field_value] = form_data[field_name]

            try:
                FormValidator(**to_validate)
            except Exception as e:
                raise HTTPException(
                    detail=str(e), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            return res[0].get("name", "")
        else:
            checked_fields = set()
            email_field_name: str = ""
            phone_number_field_name: str = ""
            date_field_name: str = ""

            for field_name in form_data.keys():
                if "email" in field_name.split("_") or "gmail" in field_name.split("_"):
                    email_field_name = field_name
                    checked_fields.add(field_name)
                elif "phone" in field_name.split("_"):
                    phone_number_field_name = field_name
                    checked_fields.add(field_name)
                elif "date" in field_name.split("_"):
                    date_field_name = field_name
                    checked_fields.add(field_name)

            text_fields = set(form_data.keys()).difference(checked_fields)

            try:
                FormValidator(
                    email=form_data.get(email_field_name, None),
                    phone=form_data.get(phone_number_field_name, None),
                    date=form_data.get(date_field_name, None),
                )
            except Exception as e:
                raise HTTPException(
                    detail=str(e), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            return_dict = {}

            if email_field_name:
                return_dict[email_field_name] = "email"
            if phone_number_field_name:
                return_dict[phone_number_field_name] = "phone"
            if date_field_name:
                return_dict[date_field_name] = "date"

            for text_field in text_fields:
                return_dict[text_field] = "text"

            return return_dict
