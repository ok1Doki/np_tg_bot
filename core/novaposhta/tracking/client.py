import httpx

from core.config import config
from core.novaposhta.tracking.request import DocumentInfo, TrackingRequestProperties
from core.novaposhta.util.base_request import Request
from core.novaposhta.util.base_response import Response


async def get_status_documents(document_number, phone) -> Response:
    document_info = DocumentInfo(
        DocumentNumber=document_number,
        Phone=phone
    )

    method_properties = TrackingRequestProperties(
        Documents=[document_info]
    )

    request_data = Request(
        apiKey=config.novaposhta_api_key,
        modelName="TrackingDocument",
        calledMethod="getStatusDocuments",
        methodProperties=method_properties
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(config.novaposhta_api_url, json=request_data.dict())

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
