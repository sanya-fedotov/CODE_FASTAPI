from datetime import date
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class SBooking(BaseModel):
    model_config = SettingsConfigDict(from_attributes=True)
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

        
