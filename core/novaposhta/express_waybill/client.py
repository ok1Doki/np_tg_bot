from datetime import datetime

import httpx

from core.config import config
from core.novaposhta.express_waybill.request import CreateExpressWaybillRequestProperties
from core.novaposhta.util.base_request import Request
from core.novaposhta.util.base_response import Response


async def create_express_waybill(payer_type,
                                 payment_method,
                                 date_time,
                                 cargo_type,
                                 weight,
                                 seats_amount,
                                 description,
                                 cost,
                                 city_sender,
                                 sender,
                                 sender_address,
                                 contact_sender,
                                 senders_phone,
                                 city_recipient,
                                 recipient,
                                 recipient_address,
                                 contact_recipient,
                                 recipients_phone,
                                 service_type='WarehouseWarehouse'
                                 ) -> Response:
    method_properties = CreateExpressWaybillRequestProperties(
        SenderWarehouseIndex="101/102",  # ?
        RecipientWarehouseIndex="101/102",  # ?
        PayerType=payer_type,
        PaymentMethod=payment_method,
        DateTime=datetime.strptime(date_time, "%d.%m.%Y"),
        CargoType=cargo_type,
        VolumeGeneral="0.45",
        Weight=weight,
        ServiceType=service_type,
        SeatsAmount=seats_amount,
        Description=description,
        Cost=cost,
        CitySender=city_sender,
        Sender=sender,
        SenderAddress=sender_address,
        ContactSender=contact_sender,
        SendersPhone=senders_phone,
        CityRecipient=city_recipient,
        Recipient=recipient,
        RecipientAddress=recipient_address,
        ContactRecipient=contact_recipient,
        RecipientsPhone=recipients_phone
    )

    request_data = Request(
        apiKey=config.novaposhta_api_key,
        modelName="InternetDocument",
        calledMethod="save",
        methodProperties=method_properties
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(config.novaposhta_api_url, json=request_data.dict())

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
