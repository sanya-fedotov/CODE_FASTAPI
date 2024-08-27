from typing import List

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class SHotel(BaseModel):
    model_config = SettingsConfigDict(from_attributes=True)
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int



class SHotelInfo(SHotel):
    model_config = SettingsConfigDict(from_attributes=True)
    rooms_left: int

