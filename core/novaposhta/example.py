from core.novaposhta.delivery_time.client import get_document_delivery_date
from core.novaposhta.document_price.client import get_document_price
from core.novaposhta.express_waybill.client import create_express_waybill
from core.novaposhta.tracking.client import get_status_documents

get_document_price(city_sender='22244293-96d3-11ea-a970-b8830365ade4',
                   city_recipient='4aa2b998-1988-11e5-add9-005056887b8d',
                   weight='2',
                   service_type='WarehouseWarehouse',
                   cost='300',
                   cargo_type='Cargo',
                   seats_amount='2'
                   )

get_document_delivery_date(city_sender='22244293-96d3-11ea-a970-b8830365ade4',
                           city_recipient='4aa2b998-1988-11e5-add9-005056887b8d',
                           service_type='WarehouseWarehouse'
                           )

get_status_documents(document_number='59000991136011',
                     phone='380674479448'
                     )

create_express_waybill(payer_type='ThirdPerson',
                       payment_method='380674479448',
                       date_time='25.08.2023',
                       cargo_type='Cargo',
                       weight='0.5',
                       service_type='DoorsWarehouse',
                       seats_amount='2',
                       description='Додатковий опис',
                       cost='15000',
                       city_sender='00000000-0000-0000-0000-000000000000',
                       sender='00000000-0000-0000-0000-000000000000',
                       sender_address='00000000-0000-0000-0000-000000000000',
                       contact_sender='00000000-0000-0000-0000-000000000000',
                       senders_phone='380660000000',
                       city_recipient='00000000-0000-0000-0000-000000000000',
                       recipient='00000000-0000-0000-0000-000000000000',
                       recipient_address='00000000-0000-0000-0000-000000000000',
                       contact_recipient='00000000-0000-0000-0000-000000000000',
                       recipients_phone='380660000000'
                       )
