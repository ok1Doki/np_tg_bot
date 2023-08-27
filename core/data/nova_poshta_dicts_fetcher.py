import json
import time

import requests

from core.config import config

MAX_RETRIES = 10
RETRY_DELAY = 20


def get_dict(model_name, called_method, fields, method_props=None):
    response = send_request(called_method, method_props, model_name)

    if response.status_code == 200:
        json_objects_list = []
        data = response.json()['data']
        for obj in data:
            for element in list(obj):
                if element not in fields:
                    obj.pop(element)
            json_objects_list.append(obj)

        output_file_path = called_method + '.json'
        save_to_json(json_objects_list, output_file_path)


def send_request(called_method, method_props, model_name):
    request = {
        "apiKey": config.novaposhta_api_key,
        "modelName": model_name,
        "calledMethod": called_method,
        "methodProperties": (method_props if method_props is not None else {})
    }
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(config.novaposhta_api_url, json=request)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Request Exception (Attempt {retries + 1}):", e)
            retries += 1
            time.sleep(RETRY_DELAY)
    return None


def save_to_json(json_objects_list, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(json_objects_list, output_file, ensure_ascii=False, indent=2)
    print("Saved " + output_file_path)


def get_settlements():
    # Довідник населених пунктів України
    get_dict("Address", "getSettlements", fields=("Ref",
                                                  "SettlementType",
                                                  # "Latitude",
                                                  # "Longitude",
                                                  "Description",
                                                  # "DescriptionRu",
                                                  "SettlementTypeDescription",
                                                  # "SettlementTypeDescriptionRu",
                                                  "Region",
                                                  "RegionsDescription",
                                                  # "RegionsDescriptionRu",
                                                  "Area",
                                                  "AreaDescription",
                                                  # "AreaDescriptionRu",
                                                  # "Index1",
                                                  # "Index2",
                                                  # "IndexCOATSU1",
                                                  # "Delivery1",
                                                  # "Delivery2",
                                                  # "Delivery3",
                                                  # "Delivery4",
                                                  # "Delivery5",
                                                  # "Delivery6",
                                                  # "Delivery7",
                                                  # "Warehouse",
                                                  # "DescriptionTranslit",
                                                  # "SettlementTypeDescriptionTranslit",
                                                  # "RegionsDescriptionTranslit",
                                                  # "AreaDescriptionTranslit",
                                                  # "SpecialCashCheck",
                                                  "Conglomerates"
                                                  ))


def get_warehouses():
    # Довідник відділень та поштоматів
    get_dict("Address", "getWarehouses", fields=("SiteKey",
                                                 "Description",
                                                 # "DescriptionRu",
                                                 "ShortAddress",
                                                 # "ShortAddressRu",
                                                 "Phone",
                                                 "TypeOfWarehouse",
                                                 "Ref",
                                                 "Number",
                                                 "CityRef",
                                                 "CityDescription",
                                                 # "CityDescriptionRu",
                                                 "SettlementRef",
                                                 "SettlementDescription",
                                                 "SettlementAreaDescription",
                                                 "SettlementRegionsDescription",
                                                 "SettlementTypeDescription",
                                                 # "SettlementTypeDescriptionRu",
                                                 # "Longitude",
                                                 # "Latitude",
                                                 # "PostFinance",
                                                 # "BicycleParking",
                                                 # "PaymentAccess",
                                                 # "POSTerminal",
                                                 # "InternationalShipping",
                                                 # "SelfServiceWorkplacesCount",
                                                 "TotalMaxWeightAllowed",
                                                 "PlaceMaxWeightAllowed",
                                                 "SendingLimitationsOnDimensions",
                                                 "ReceivingLimitationsOnDimensions",
                                                 # "Reception",
                                                 # "Delivery",
                                                 # "Schedule",
                                                 "DistrictCode",
                                                 # "WarehouseStatus",
                                                 # "WarehouseStatusDate",
                                                 "CategoryOfWarehouse",
                                                 "RegionCity",
                                                 # "WarehouseForAgent",
                                                 "MaxDeclaredCost",
                                                 "DenyToSelect",
                                                 "PostMachineType",
                                                 "PostalCodeUA",
                                                 # "OnlyReceivingParcel",
                                                 "WarehouseIndex",
                                                 # "WarehouseIllusha",
                                                 "Direct",
                                                 # "GeneratorEnabled",
                                                 # "WorkInMobileAwis",
                                                 # "CanGetMoneyTransfer",
                                                 # "HasMirror",
                                                 # "HasFittingRoom",
                                                 # "BeaconCode",
                                                 # "PostomatFor"
                                                 ))


def get_warehouse_types():
    # Довідник типів відділень
    get_dict("Address", "getWarehouseTypes", fields=("Ref",
                                                     # "DescriptionRu,"
                                                     "Description"
                                                     ))


def get_settlements_areas():
    # Довідник областей населених пунктів
    get_dict("Address", "getSettlementAreas", fields=("Description",
                                                      "Ref",
                                                      "AreasCenter",
                                                      "RegionType"
                                                      ))


def get_cargo_types():
    # Види вантажу
    get_dict("Common", "getCargoTypes", fields=("Ref",
                                                "Description"
                                                ))


def get_backward_delivery_cargo_types():
    # Види зворотної доставки вантажу
    get_dict("Common", "getBackwardDeliveryCargoTypes", fields=("Ref",
                                                                "Description"
                                                                ))


def get_palletes_list():
    # Види палет
    get_dict("Common", "getPalletsList", fields=("Ref",
                                                 "Description",
                                                 # "DescriptionRu",
                                                 "Weight"
                                                 ))


def get_types_of_payers_for_redelivery():
    # Види платників зворотної доставки
    get_dict("Common", "getTypesOfPayersForRedelivery", fields=("Ref",
                                                                "Description"
                                                                ))


def get_pack_list():
    # Види упаковки
    get_dict("Common", "getPackList", fields=("Ref",
                                              "Description",
                                              # "DescriptionRu",
                                              "Length",
                                              "Width",
                                              "Height",
                                              "VolumetricWeight",
                                              "TypeOfPacking"
                                              ))


def get_tires_wheels_list():
    # Види шин і дисків
    get_dict("Common", "getTiresWheelsList", fields=("Ref",
                                                     "Description",
                                                     # "DescriptionRu",
                                                     "Weight",
                                                     "DescriptionType"
                                                     ))


def get_cargo_description_list():
    # Описи вантажу
    get_dict("Common", "getCargoDescriptionList", fields=("Ref",
                                                          # "DescriptionRu,"
                                                          "Description"
                                                          ))


def get_message_code_text():
    # Перелік помилок
    get_dict("Common", "getMessageCodeText", fields=("MessageCode",
                                                     "MessageText",
                                                     # "MessageDescriptionRU",
                                                     "MessageDescriptionUA"
                                                     ))


def get_service_types():
    # Технології доставки
    get_dict("Common", "getServiceTypes", fields=("Ref",
                                                  "Description"
                                                  ))


def get_ownership_forms_list():
    # Форми власності
    get_dict("Common", "getOwnershipFormsList", fields=("Ref",
                                                        "Description",
                                                        "FullName"
                                                        ))


def get_cities_with_streets():
    # Довідник міст компанії
    # Довідник вулиць компанії
    cities_fields = ("Description",
                     # "DescriptionRu",
                     "Ref",
                     # "Delivery1",
                     # "Delivery2",
                     # "Delivery3",
                     # "Delivery4",
                     # "Delivery5",
                     # "Delivery6",
                     # "Delivery7",
                     "Area",
                     "AreaDescription",
                     # "AreaDescriptionRu",
                     "SettlementType",
                     # "IsBranch",
                     # "PreventEntryNewStreetsUser",
                     "Conglomerates",
                     "CityID",
                     # "SettlementTypeDescriptionRu",
                     "SettlementTypeDescription"
                     )
    street_fields = ("Ref",
                     "Description",
                     "StreetsTypeRef",
                     "StreetsType"
                     )

    cities_list = []

    cities_response = send_request("getCities", None, "Address")
    if cities_response.status_code == 200:
        city_data = cities_response.json()['data']
        for city in city_data:
            for element in list(city):
                if element not in cities_fields:
                    city.pop(element)
            cities_list.append(city)
        save_to_json(cities_list, 'getCities.json')

    chunk_size = 2000
    for i in range(0, len(cities_list), chunk_size):
        streets_list = []
        for city_ind in range(i, min(len(cities_list), i + chunk_size)):
            city = cities_list[city_ind]
            print(city_ind)
            if city_ind % 10 == 0:
                time.sleep(4)
            street_response = send_request("getStreet", {"CityRef": city['Ref']}, "Address")
            if street_response.status_code == 200:
                street_data = street_response.json()['data']
                for street in street_data:
                    for element in list(street):
                        if element not in street_fields:
                            street.pop(element)
                    street["CityRef"] = city["Ref"]
                    streets_list.append(street)
        save_to_json(streets_list, "getStreets-" + str(i) + ".json")


def get_areas_with_regions():
    # Довідник географічних областей України
    # Довідник районів областей населених пунктів
    areas_fields = ("Ref",
                    "AreasCenter",
                    # "DescriptionRu",
                    "Description"
                    )
    settlements_regions_fields = ("Ref",
                                  "AreasCenter",
                                  "Description",
                                  "RegionType"
                                  )

    areas_response = send_request("getAreas", None, "Address")
    if areas_response.status_code == 200:
        areas_list = []
        regions_list = []

        area_data = areas_response.json()['data']
        for area in area_data:
            for element in list(area):
                if element not in areas_fields:
                    area.pop(element)
            areas_list.append(area)

            print(area["Description"])
            region_response = send_request("getSettlementCountryRegion", {"AreaRef": area["Ref"]}, "Address")
            if region_response.status_code == 200:
                region_data = region_response.json()['data']
                for region in region_data:
                    for element in list(region):
                        if element not in settlements_regions_fields:
                            region.pop(element)
                    regions_list.append(region)

        save_to_json(areas_list, 'getAreas.json')
        save_to_json(regions_list, 'getSettlementCountryRegion.json')


if __name__ == "__main__":
    # get_settlements()
    # get_cities_with_streets()  # HEAVY OPERATION !
    # get_areas_with_regions()
    # get_warehouses()
    # get_warehouse_types()
    # get_settlements_areas()
    # get_cargo_types()
    # get_backward_delivery_cargo_types()
    # get_palletes_list()
    # get_types_of_payers_for_redelivery()
    # get_pack_list()
    # get_tires_wheels_list()
    # get_cargo_description_list()
    # get_message_code_text()
    # get_service_types()
    # get_ownership_forms_list()
    pass
