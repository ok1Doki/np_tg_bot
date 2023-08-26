import _collections_abc
from typing import Dict, List
from enum import Enum
import novaposhta as np


class PropertyType(str, Enum):
    string = 'string'
    integer = 'integer'
    bool = 'boolean'


class property():
    def __init__(self, name: str, type: PropertyType, description: str, required: bool = True, enum: List = [],
                 default: str = None):
        self.name = name
        self.type = type
        self.description = description
        self.required = required  # making this property required or optional for gpt to fill
        self.enum = enum  # it doesn't strictly define options for gpt, only loosely
        self.default = default


class properties(Dict):
    def add(self, item: property):
        if isinstance(item, property):
            super().__setitem__(item.name,
                                {'type': item.type.value, 'description': item.description, 'required': item.required})
        else:
            raise ValueError('Must be type "property."')

        # add enumerators if passed
        if item.enum != None and len(item.enum) > 0:
            super().__getitem__(item.name)['enum'] = item.enum

        # default of property
        if item.default != None:
            super().__getitem__(item.name)['default'] = item.default


class function():
    def __init__(self, fn, trigger_fn, name: str, description: str):
        self.fn = fn  # function to be executed (with params)
        self.trigger_fn = trigger_fn  # insert trigger fn for ui flow here
        self.name = name
        self.description = description
        self.properties = properties()
        self.properties_wo_required = {}

    def to_json(self):
        # create "required" list for chatcompletion
        self.required = [k for k, v in self.properties.items() if v['required'] == True]

        # remove 'required' attribute from properties as it is a list of it's own
        for k, v in self.properties.items():
            self.properties_wo_required[k] = {m: v[m] for m in v.keys() - {'required'}}

        funct = {'name': self.name,
                 'description': self.description,
                 'parameters': {'type': 'object',
                                'properties': self.properties_wo_required},
                 'required': self.required
                }
        return funct
    
    # user for specific function call, like in OPENAI_FUNCTION_CALL_OPTIONS
    def to_json_without_params(self):
        funct = {'name': self.name,
                 'description': self.description,
                 'parameters': {'type': 'object',
                                'properties': {}},
                }
        return funct


class functions(_collections_abc.MutableMapping):
    def __init__(self):
        super().__init__()
        self._dict = dict()

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        self._dict.__setitem__(key, value)
        self._changed = True

    def __delitem__(self, key):
        self._dict.__delitem__(key)
        self._changed = True

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()

    # ChatGPT is expecting an List.
    def to_json_without_params(self):
        l = []
        for item in self._dict:
            l.append(self._dict[item].to_json_without_params())
        return l


# stubs for functions
def my_fn(**kwargs):
    arg1 = kwargs["printText"]
    return arg1

def trigger_fn():
    pass

# name and description can be in any lang (uk) and gotta be descriptive/verbose for gpt.
# PropertyType also got integer and bool, and these can be set:
# enum=['big', 'small']  # it doesn't strictly define options for gpt, only loosely
# default=['small']  # default value
f = function(fn=my_fn, trigger_fn=trigger_fn, name="print", description="print function")
f.properties.add(
    property(
        "printText",
        PropertyType.string,
        "text to print",
        default="default"
    )
)

# the collection of functions to be used with gpt
fns_collection = functions()
fns_collection[f.name] = f

# get_document_delivery_date(city_sender, city_recipient, service_type):
f1 = function(fn=np.delivery_time.get_document_delivery_date, 
              trigger_fn=trigger_fn,  # insert trigger fn for ui flow here
              name="ПрогнозДатиДоставки", 
              description="Прогноз орієнтовної дати доставки вантажу")
f1.properties.add(property("city_sender", PropertyType.string, "Населений пункт відправника"))
f1.properties.add(property("city_recipient", PropertyType.string, "Населений пункт отримувача"))
# i suggest remove service_type and make it a default value WarehouseWarehouse for now.
# f1.properties.add(property("service_type", PropertyType.string, "Тип доставки"))
fns_collection[f1.name] = f1

# get_document_price(city_sender, city_recipient, weight, service_type, cost, cargo_type, seats_amount)
f2 = function(fn=np.get_document_price, 
              trigger_fn=trigger_fn, 
              name="РозрахуватиВартість", 
              description="Розрахунок вартості послуг доставки вантажу, \
              шин та дисків, палет, а також документів.")
f2.properties.add(property("city_sender", PropertyType.string, "Населений пункт відправника"))
f2.properties.add(property("city_recipient", PropertyType.string, "Населений пункт отримувача"))
f2.properties.add(property("weight", PropertyType.integer, "Вага вантажу"))
# f2.properties.add(property("service_type", PropertyType.string, "Тип доставки"))
f2.properties.add(property("cost", PropertyType.integer, "Оціночна вартість вантажу (ціле число)"))
f2.properties.add(property("cargo_type", PropertyType.string, "Тип вантажу"), 
                  enum=['Cargo', 'Documents', 'TiresWheels', 'Pallet'],  # gpt should be smart enough
                  default='Cargo')
fns_collection[f2.name] = f2

# get_status_documents(document_number, phone) -> Response:
f3 = function(fn=np.get_status_documents, 
              trigger_fn=trigger_fn, 
              name="Трекінг", 
              description="цей метод дозволяє переглядати інформацію щодо статусу відправлення")
f3.properties.add(property("document_number", PropertyType.string,
                           "Номер ЕН або ТТН (номер відправлення, номер накладної)"))
f3.properties.add(property("phone", PropertyType.string, "Номер телефону одержувача/відправника"))
fns_collection[f3.name] = f3

# create_express_waybill(  payer_type,
                        #  payment_method,
                        #  date_time,
                        #  cargo_type,
                        #  weight,
                        #  seats_amount,
                        #  description,
                        #  cost,
                        #  city_sender,
                        #  sender,
                        #  sender_address,
                        #  contact_sender,
                        #  senders_phone,
                        #  city_recipient,
                        #  recipient,
                        #  recipient_address,
                        #  contact_recipient,
                        #  recipients_phone) -> Response:
f4 = function(fn=np.express_waybill.create_express_waybill, 
              trigger_fn=trigger_fn, 
              name="СтворитиЕН", 
              description="Створення електронної накладної, яка використовується для доставки вантажу")
f4.properties.add(property("payer_type", PropertyType.string, "Тип платника"), 
                  enum=['Sender', 'Recipient', 'ThirdPerson'],  # gpt should be smart enough
                  default='Recipient')
f4.properties.add(property("payment_method", PropertyType.string, "Спосіб оплати",
                           enum=['Cash', 'NonCash']))
f4.properties.add(property("date_time", PropertyType.string, "Дата відправлення в форматі ДД.ММ.РРРР"))
f4.properties.add(property("cargo_type", PropertyType.string, "Тип вантажу"),
                    enum=['Cargo', 'Documents', 'TiresWheels', 'Pallet'],
                    default='Cargo')
f4.properties.add(property("weight", PropertyType.integer, "Фактична вага, в кг min - 0.1"))
f4.properties.add(property("seats_amount", PropertyType.integer, "Кількість місць відправлення, ціле число"))
f4.properties.add(property("description", PropertyType.string, "Опис вантажу"))
f4.properties.add(property("cost", PropertyType.integer, "Оціночна вартість вантажу (ціле число)"))
f4.properties.add(property("city_sender", PropertyType.string, "Населений пункт відправника"))
f4.properties.add(property("sender", PropertyType.string, "номер телефону відправника"))  # phone number?
f4.properties.add(property("sender_address", PropertyType.string, "Адреса відправника"))
f4.properties.add(property("contact_sender", PropertyType.string, "Контактна особа відправника"))  # ?
f4.properties.add(property("senders_phone", PropertyType.string, "Номер телефону відправника"))
f4.properties.add(property("city_recipient", PropertyType.string, "Населений пункт отримувача"))
f4.properties.add(property("recipient", PropertyType.string, "номер телефону отримувача"))  # phone number?
f4.properties.add(property("recipient_address", PropertyType.string, "Адреса отримувача"))
f4.properties.add(property("contact_recipient", PropertyType.string, "Контактна особа отримувача"))  # ?
f4.properties.add(property("recipients_phone", PropertyType.string, "номер телефону отримувача"))
fns_collection[f4.name] = f4
