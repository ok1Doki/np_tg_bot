import httpx

from core.config import config
from core.novaposhta.document_price.request import DocumentPriceRequestProperties, RedeliveryCalculate, CargoDetail
from core.novaposhta.util.base_request import Request
from core.novaposhta.util.base_response import Response


async def get_document_price(city_sender, city_recipient, weight, service_type, cost, cargo_type,
                             seats_amount) -> Response:
    redelivery_calculate = RedeliveryCalculate(
        CargoType="Money",
        Amount="100"
    )

    cargo_detail = CargoDetail(
        CargoDescription="Some description",
        Amount="2"
    )

    method_properties = DocumentPriceRequestProperties(
        CitySender=city_sender,
        CityRecipient=city_recipient,
        Weight=weight,
        ServiceType=service_type,
        Cost=cost,
        CargoType=cargo_type,
        SeatsAmount=seats_amount,
        # RedeliveryCalculate=redelivery_calculate,
        # PackCount="1",
        # PackRef="00000000-0000-0000-0000-000000000000",
        # Amount="100",
        # CargoDetails=[cargo_detail],
        # CargoDescription="00000000-0000-0000-0000-000000000000"
    )

    request_data = Request(
        apiKey=config.novaposhta_api_key,
        modelName="InternetDocument",
        calledMethod="getDocumentPrice",
        methodProperties=method_properties
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(config.novaposhta_api_url, json=request_data.dict())

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
