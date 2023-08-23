from typing import List

from pydantic import BaseModel

from core.novaposhta.util.base_request import MethodProperties


class DocumentInfo(BaseModel):
    DocumentNumber: str
    Phone: str


class TrackingRequestProperties(MethodProperties):
    Documents: List[DocumentInfo]
