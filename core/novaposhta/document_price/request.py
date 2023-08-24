from typing import List

from pydantic import BaseModel

from core.novaposhta.util.base_request import MethodProperties


class RedeliveryCalculate(BaseModel):
    CargoType: str
    Amount: str


class CargoDetail(BaseModel):
    CargoDescription: str
    Amount: str


class DocumentPriceRequestProperties(MethodProperties):
    CitySender: str
    CityRecipient: str
    Weight: str
    ServiceType: str
    Cost: str
    CargoType: str
    SeatsAmount: str
    RedeliveryCalculate: RedeliveryCalculate = None
    PackCount: str = None
    PackRef: str = None
    Amount: str = None
    CargoDetails: List[CargoDetail] = None
    CargoDescription: str = None
