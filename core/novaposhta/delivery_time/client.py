import locale
from datetime import datetime

import httpx

import core.config as config
import core.utils.chroma_utils as chroma
from core.novaposhta.delivery_time.request import DocumentDeliveryDateRequestProperties
from core.novaposhta.delivery_time.response import DeliveryDate
from core.novaposhta.util.base_request import Request


async def get_document_delivery_date(city_sender: str, city_recipient: str, service_type='WarehouseWarehouse'):
    city_sender_ref = \
    chroma.query_collection(collection_name=chroma.cities_collection_name, query=city_sender)["ids"][0][0]
    city_recipient_ref = \
    chroma.query_collection(collection_name=chroma.cities_collection_name, query=city_recipient)["ids"][0][0]

    method_properties = DocumentDeliveryDateRequestProperties(
        DateTime=datetime.now().strftime("%d.%m.%Y"),
        ServiceType=service_type,
        CitySender=city_sender_ref,
        CityRecipient=city_recipient_ref
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
            json_obj = response.json()
            if "success" in json_obj:
                locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
                date_str = DeliveryDate(**json_obj['data'][0]['DeliveryDate']).date
                date_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                res = date_object.strftime('%d %B, o %H:%M')
            return res
        else:
            return None
