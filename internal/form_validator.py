from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


class FormValidator(BaseModel):
    email: EmailStr | None = None
    phone: str | None = Field(default=None, description="+7 xxx xxx xx xx")
    date: str | None = Field(default=None, description="YYYY-MM-DD / DD.MM.YYYY")
    text: str | None = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str):
        date_pattern_1 = "%d.%m.%Y"
        date_pattern_2 = "%Y-%m-%d"

        parsed_date = None
        if v:
            try:
                parsed_date = datetime.strptime(v, date_pattern_1)
            except Exception:
                try:
                    parsed_date = datetime.strptime(v, date_pattern_2)
                except Exception:
                    raise Exception("invalid date format")
            return parsed_date
        return v

    @field_validator("phone", mode="after")
    @classmethod
    def validate_phone(cls, v: str):
        split_phone = v.split(" ")
        validators = [
            len(split_phone[0]) == 2,
            len(split_phone[1]) == 3,
            len(split_phone[2]) == 3,
            len(split_phone[3]) == 2,
            len(split_phone[4]) == 2,
        ]
        if len(split_phone) != 5 or not all(validators):
            raise Exception(
                "phone validation error, make sure the format is +7 XXX XXX XX XX"
            )
        if split_phone[0] != "+7":
            raise Exception("ivalid country code (must be +7)")
        return v
