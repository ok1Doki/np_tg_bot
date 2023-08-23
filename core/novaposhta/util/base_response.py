from pydantic import BaseModel
from typing import List


class ResponseObject(BaseModel):
    pass


class Response(BaseModel):
    success: bool
    data: List[ResponseObject]
    errors: List[str]
    warnings: List[str]
    info: List[str]
    messageCodes: List[str]
    errorCodes: List[str]
    warningCodes: List[str]
    infoCodes: List[str]
