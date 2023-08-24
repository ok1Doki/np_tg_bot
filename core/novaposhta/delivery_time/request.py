from core.novaposhta.util.base_request import MethodProperties


class DocumentDeliveryDateRequestProperties(MethodProperties):
    CitySender: str
    CityRecipient: str
    ServiceType: str
    DateTime: str
