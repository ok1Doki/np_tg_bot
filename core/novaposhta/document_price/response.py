from pydantic import BaseModel

from core.novaposhta.util.base_response import ResponseObject


class TZoneInfo(BaseModel):
    TzoneName: str
    TzoneID: str


class DocumentPriceData(ResponseObject):
    AssessedCost: str
    Cost: str
    CostRedelivery: str
    TZoneInfo: TZoneInfo
    CostPack: str
