from typing import Dict, Any

from pydantic import BaseModel


class MethodProperties(BaseModel):
    pass


class Request(BaseModel):
    apiKey: str
    modelName: str
    calledMethod: str
    methodProperties: MethodProperties

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)
