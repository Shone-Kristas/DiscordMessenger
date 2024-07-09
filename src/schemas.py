from pydantic import BaseModel, validator
from datetime import datetime


class MessageInput(BaseModel):
    message: str
    time: str

    @validator('time')
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Time must be in HH:MM format')
        return v