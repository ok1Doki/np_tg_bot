from pydantic import BaseModel


class CreateExpressWaybillRequestProperties(BaseModel):
    SenderWarehouseIndex: str
    RecipientWarehouseIndex: str
    PayerType: str
    PaymentMethod: str
    DateTime: str
    CargoType: str
    VolumeGeneral: str
    Weight: str
    ServiceType: str
    SeatsAmount: str
    Description: str
    Cost: str
    CitySender: str
    Sender: str
    SenderAddress: str
    ContactSender: str
    SendersPhone: str
    CityRecipient: str
    Recipient: str
    RecipientAddress: str
    ContactRecipient: str
    RecipientsPhone: str
