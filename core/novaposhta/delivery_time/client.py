from datetime import datetime

import httpx

from core.config import config
from core.novaposhta.delivery_time.request import DocumentDeliveryDateRequestProperties
from core.novaposhta.util.base_request import Request


async def get_document_delivery_date(city_sender, city_recipient, service_type='WarehouseWarehouse'):
    method_properties = DocumentDeliveryDateRequestProperties(
        DateTime=datetime.now().strftime("%d.%m.%Y"),
        ServiceType=service_type,
        CitySender=city_sender,
        CityRecipient=city_recipient
    )

    request_data = Request(
        apiKey=config.novaposhta_api_key,
        modelName="InternetDocument",
        calledMethod="getDocumentDeliveryDate",
        methodProperties=method_properties
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(config.novaposhta_api_url, json=request_data.dict())

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
