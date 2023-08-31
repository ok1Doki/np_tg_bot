from pydantic import BaseModel


class DeliveryDate(BaseModel):
    date: str
    timezone_type: str
    timezone: str
