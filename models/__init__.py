import datetime
from typing import Optional, Union
from pydantic import BaseModel, validator



class Person(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime.date] = "DAY-MON-YEAR"
    id_number: Union[None, int, str] = '<ID>'

    @validator("date_of_birth", pre=True)
    def parse_date_of_birth(cls, value):
        return datetime.datetime.strptime(
            value,
            "%d-%m-%Y"
        ).date()