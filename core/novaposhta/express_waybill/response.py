from core.novaposhta.util.base_response import ResponseObject


class CreateExpressWaybillResponseData(ResponseObject):
    Ref: str
    CostOnSite: str
    EstimatedDeliveryDate: str
    IntDocNumber: str
    TypeDocument: str
