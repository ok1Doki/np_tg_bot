from core.novaposhta.util.base_response import ResponseObject


class DocumentDeliveryDateData(ResponseObject):
    date: str
    timezone_type: str
    timezone: str
