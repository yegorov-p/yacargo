# -*- coding: utf-8 -*-
"""
Модуль с объектами
"""
import collections
import logging
from typing import List, Optional

from typeguard import check_type

from yacargo.exceptions import InputParamError

logger = logging.getLogger('yacargo')


def validate_fields(field_name, field, field_type):
    """
    Валидатор полей на соответствие ожидаемому типу

    :param field_name: Название поля, передается для ошибки

    :param field: Поле

    :param field_type: Тип поля

    :return: Объект в виде json
    """
    try:
        check_type(field_name, field, field_type)
    except TypeError as exc:
        raise InputParamError(exc)
    else:
        if isinstance(field, list):
            return [i if isinstance(i, (bool, str, int, float, tuple, list, dict)) else i.json() for i in field]
        elif isinstance(field, (bool, str, int, float, tuple, list, dict)):
            return field
        else:
            return field.json()


class YCBase:
    """
        Базовый класс
    """

    # def __init__(self, data):
    #    self.body = data

    def json(self) -> dict:
        """

        :return: Объект в виде JSON
        :rtype: dict
        """
        return self.body


class CutClaimResponse(YCBase):
    """
        ???
        ???

            :param str id: id заявки, полученный на этапе создания заявки *(Обязательный параметр)* (741cedf82cd464fa6fa16d87155c636)
            :param Optional[str] status: Статус заявки *(Обязательный параметр)* (new)

                * **new** - ???
                * **estimating** - ???
                * **estimating_failed** - ???
                * **ready_for_approval** - ???
                * **accepted** - ???
                * **performer_lookup** - ???
                * **performer_draft** - ???
                * **performer_found** - ???
                * **performer_not_found** - ???
                * **pickup_arrived** - ???
                * **ready_for_pickup_confirmation** - ???
                * **pickuped** - ???
                * **delivery_arrived** - ???
                * **ready_for_delivery_confirmation** - ???
                * **pay_waiting** - ???
                * **delivered** - ???
                * **delivered_finish** - ???
                * **returning** - ???
                * **return_arrived** - ???
                * **ready_for_return_confirmation** - ???
                * **returned** - ???
                * **returned_finish** - ???
                * **failed** - ???
                * **cancelled** - ???
                * **cancelled_with_payment** - ???
                * **cancelled_by_taxi** - ???
                * **cancelled_with_items_on_hands** - ???

            :param int version: Версия заявки из запроса *(Обязательный параметр)* (1)
            :param Optional[str] taxi_order_id: taxi_order_id в такси (uuid) (33f95d1a73b84cbcaa06c9ad306dc459)
    """

    def __init__(self,
                 id: str = None,
                 status: Optional[str] = None,
                 version: int = None,
                 taxi_order_id: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if id is not None:
            self.body["id"] = validate_fields('id', id, str)
            self.body['id'] = validate_fields('id', id, str)
        if id is None:
            raise InputParamError("<id> (=>id) of <CutClaimResponse> is a required parameter")

        if status is not None:
            self.body["status"] = validate_fields('status', status, str)
            self.body['status'] = validate_fields('status', status, Optional[str])
        if status is None:
            raise InputParamError("<status> (=>status) of <CutClaimResponse> is a required parameter")

        if status not in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived',
                          'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning',
                          'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi',
                          'cancelled_with_items_on_hands']:
            raise InputParamError(
                "<status> of <CutClaimResponse> should be in <new, estimating, estimating_failed, ready_for_approval, accepted, performer_lookup, performer_draft, performer_found, performer_not_found, pickup_arrived, ready_for_pickup_confirmation, pickuped, delivery_arrived, ready_for_delivery_confirmation, pay_waiting, delivered, delivered_finish, returning, return_arrived, ready_for_return_confirmation, returned, returned_finish, failed, cancelled, cancelled_with_payment, cancelled_by_taxi, cancelled_with_items_on_hands>")

        if version is not None:
            self.body["version"] = validate_fields('version', version, int)
            self.body['version'] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <CutClaimResponse> is a required parameter")

        if taxi_order_id is not None:
            self.body["taxi_order_id"] = validate_fields('taxi_order_id', taxi_order_id, str)
            self.body['taxi_order_id'] = validate_fields('taxi_order_id', taxi_order_id, Optional[str])

    def __repr__(self):
        return "<CutClaimResponse>"

    @property
    def id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("id")

    @property
    def status(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("status")

    @property
    def version(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("version")

    @property
    def taxi_order_id(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("taxi_order_id")


class ConfirmationCodeResponse(YCBase):
    """
        ???
        ???

            :param str code: Код подтверждения *(Обязательный параметр)* (2000)
            :param int attempts: Число оставшихся попыток ввода кода *(Обязательный параметр)* (1)
    """

    def __init__(self,
                 code: str = None,
                 attempts: int = None,
                 ):
        self.body = collections.defaultdict(dict)

        if code is not None:
            self.body["code"] = validate_fields('code', code, str)
            self.body['code'] = validate_fields('code', code, str)
        if code is None:
            raise InputParamError("<code> (=>code) of <ConfirmationCodeResponse> is a required parameter")

        if attempts is not None:
            self.body["attempts"] = validate_fields('attempts', attempts, int)
            self.body['attempts'] = validate_fields('attempts', attempts, int)
        if attempts is None:
            raise InputParamError("<attempts> (=>attempts) of <ConfirmationCodeResponse> is a required parameter")

    def __repr__(self):
        return "<ConfirmationCodeResponse>"

    @property
    def code(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("code")

    @property
    def attempts(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("attempts")


class ClaimsJournalResponse(YCBase):
    """
        ???
        ???

            :param str cursor: Идентификатор последнего изменения *(Обязательный параметр)*
            :param List['Event'] events: ??? *(Обязательный параметр)*
    """

    def __init__(self,
                 cursor: str = None,
                 events: List['Event'] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if cursor is not None:
            self.body["cursor"] = validate_fields('cursor', cursor, str)
            self.body['cursor'] = validate_fields('cursor', cursor, str)
        if cursor is None:
            raise InputParamError("<cursor> (=>cursor) of <ClaimsJournalResponse> is a required parameter")

        if events is not None:
            self.body["events"] = validate_fields('events', events, List['Event'])
            self.body['events'] = validate_fields('events', events, List['Event'])
        if events is None:
            raise InputParamError("<events> (=>events) of <ClaimsJournalResponse> is a required parameter")

    def __repr__(self):
        return "<ClaimsJournalResponse>"

    @property
    def cursor(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("cursor")

    @property
    def events(self) -> List['Event']:
        """

        :return: ???
        :rtype: List['Event']
        """
        return [Event(operation_id=item.get("operation_id", None),
                      claim_id=item.get("claim_id", None),
                      change_type=item.get("change_type", None),
                      updated_ts=item.get("updated_ts", None),
                      new_status=item.get("new_status", None),
                      new_price=item.get("new_price", None),
                      new_currency=item.get("new_currency", None),
                      resolution=item.get("resolution", None),
                      revision=item.get("revision", None),
                      client_id=item.get("client_id", None),
                      ) for item in self.body.get("events")]


class SearchedClaimMP(YCBase):
    """
        ???
        ???

            :param str id: id заявки, полученный на этапе создания заявки *(Обязательный параметр)* (741cedf82cd464fa6fa16d87155c636)
            :param Optional[str] corp_client_id: id корпоративного клиента (из OAuth токена) (cd8cc018bde34597932855e3cfdce927)
            :param Optional[str] yandex_uid: yandex uid (3a4e06e733a3433880e4900ffeaf7b62)
            :param List['CargoItemMP'] items: Перечисление наименований грузов для отправления *(Обязательный параметр)*
            :param List['ResponseCargoPointMP'] route_points: Информация по точкам маршрута *(Обязательный параметр)*
            :param Optional[int] current_point_id: Целочисленный идентификатор точки (6987)
            :param Optional[str] status: Статус заявки *(Обязательный параметр)* (new)

                * **new** - ???
                * **estimating** - ???
                * **estimating_failed** - ???
                * **ready_for_approval** - ???
                * **accepted** - ???
                * **performer_lookup** - ???
                * **performer_draft** - ???
                * **performer_found** - ???
                * **performer_not_found** - ???
                * **pickup_arrived** - ???
                * **ready_for_pickup_confirmation** - ???
                * **pickuped** - ???
                * **delivery_arrived** - ???
                * **ready_for_delivery_confirmation** - ???
                * **pay_waiting** - ???
                * **delivered** - ???
                * **delivered_finish** - ???
                * **returning** - ???
                * **return_arrived** - ???
                * **ready_for_return_confirmation** - ???
                * **returned** - ???
                * **returned_finish** - ???
                * **failed** - ???
                * **cancelled** - ???
                * **cancelled_with_payment** - ???
                * **cancelled_by_taxi** - ???
                * **cancelled_with_items_on_hands** - ???

            :param int version: ??? *(Обязательный параметр)*
            :param Optional[List['HumanErrorMessage']] error_messages: ???
            :param str emergency_contact_name: Имя контактного лица *(Обязательный параметр)* (Рик)
            :param str emergency_contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999999)
            :param Optional[bool] skip_door_to_door: Отказ от доставки до двери. В случае true — курьер доставит заказ только на улицу, до подъезда
            :param Optional[bool] skip_client_notify: Не отправлять получателю нотификации, когда к нему направится курьер
            :param Optional[bool] skip_emergency_notify: Не отправлять нотификации emergency контакту
            :param Optional[bool] skip_act: Не показывать акт
            :param Optional[bool] optional_return: Не требуется возврат товаров в случае отмены заказа. Курьер оставляет товар себе
            :param Optional[int] eta: Ожидаемое время исполнения заказа в минутах (10)
            :param str created_ts: Дата-время создания *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
            :param str updated_ts: Дата-время последнего обновления *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
            :param str taxi_offer_offer_id: Идентификатор оффера *(Обязательный параметр)* (28ae5f1d72364468be3f5e26cd6a66bf)
            :param int taxi_offer_price_raw: Цена по офферу в валюте, указанной в договоре *(Обязательный параметр)* (12)
            :param Optional[str] taxi_offer_price: Decimal(19, 4) *(Обязательный параметр)* (12.50)
            :param str pricing_offer_offer_id: Идентификатор оффера *(Обязательный параметр)* (28ae5f1d72364468be3f5e26cd6a66bf)
            :param int pricing_offer_price_raw: (deprecated) Цена по офферу в валюте, указанной в договоре *(Обязательный параметр)* (12)
            :param str pricing_offer_price: Decimal(19, 4) *(Обязательный параметр)* (12.50)
            :param Optional[str] pricing_currency: Трехзначный код валюты, в которой ведется расчет (например, RUB) (RUB)
            :param str pricing_currency_rules_code: ??? *(Обязательный параметр)* (RUB)
            :param str pricing_currency_rules_text: ??? *(Обязательный параметр)* (руб.)
            :param str pricing_currency_rules_template: ??? *(Обязательный параметр)* ($VALUE$ $SIGN$$CURRENCY$)
            :param Optional[str] pricing_currency_rules_sign: ??? (₽)
            :param str pricing_final_price: Decimal(19, 4) (12.50)
            :param Optional[str] available_cancel_state: Признак возможности платной/бесплатной отмены (free)

                * **free** - ???
                * **paid** - ???

            :param str client_requirements_taxi_class: Класс такси. Возможные значения express, cargo. *(Обязательный параметр)* (express)
            :param Optional[str] client_requirements_cargo_type: Тип грузовика (lcv_m)
            :param Optional[int] client_requirements_cargo_loaders: Требуемое число грузчиков
            :param Optional[List['str']] client_requirements_cargo_options: Дополнительные опции тарифа
            :param Optional[List['MatchedCar']] matched_cars: Информация об исполнителе (массив, на данный момент всегда 1 элемент)
            :param Optional[List['ClaimWarning']] warnings: Предупреждения по циклу заявки
            :param str performer_info_courier_name: Имя курьера, доставляющего посылку *(Обязательный параметр)* (Личность)
            :param str performer_info_legal_name: Данные о юр. лице, осуществляющем доставку *(Обязательный параметр)* (ИП Птичья личность)
            :param Optional[str] performer_info_car_model: Модель машины (Hyundai Solaris)
            :param Optional[str] performer_info_car_number: Номер машины (А100РА100)
            :param str callback_properties_callback_url: URL, который будет вызываться при смене статусов по заявке.Данный механизм устарел, вместо него следует использовать операцию v1/claims/journal. *(Обязательный параметр)* (https://www.example.com)
            :param Optional[str] due: Создать заказ к определенному времени (например, заказ на завтра). Согласуйте с менеджером использование опции! (2020-01-01T00:00:00+00:00)
            :param Optional[str] shipping_document: Сопроводительные документы
            :param Optional[str] comment: Общий комментарий к заказу (Ресторан)
            :param Optional[str] c2c_data_payment_method_id: ??? (payment_method_id)
            :param str c2c_data_payment_type: ??? *(Обязательный параметр)* (card)
            :param Optional[str] c2c_data_partner_tag: ??? (some_tag)
            :param int revision: ??? *(Обязательный параметр)* (1)
    """

    def __init__(self,
                 id: str = None,
                 corp_client_id: Optional[str] = None,
                 yandex_uid: Optional[str] = None,
                 items: List['CargoItemMP'] = None,
                 route_points: List['ResponseCargoPointMP'] = None,
                 current_point_id: Optional[int] = None,
                 status: Optional[str] = None,
                 version: int = None,
                 error_messages: Optional[List['HumanErrorMessage']] = None,
                 emergency_contact_name: str = None,
                 emergency_contact_phone: str = None,
                 skip_door_to_door: Optional[bool] = None,
                 skip_client_notify: Optional[bool] = None,
                 skip_emergency_notify: Optional[bool] = None,
                 skip_act: Optional[bool] = None,
                 optional_return: Optional[bool] = None,
                 eta: Optional[int] = None,
                 created_ts: str = None,
                 updated_ts: str = None,
                 taxi_offer_offer_id: str = None,
                 taxi_offer_price_raw: int = None,
                 taxi_offer_price: Optional[str] = None,
                 pricing_offer_offer_id: str = None,
                 pricing_offer_price_raw: int = None,
                 pricing_offer_price: str = None,
                 pricing_currency: Optional[str] = None,
                 pricing_currency_rules_code: str = None,
                 pricing_currency_rules_text: str = None,
                 pricing_currency_rules_template: str = None,
                 pricing_currency_rules_sign: Optional[str] = None,
                 pricing_final_price: str = None,
                 available_cancel_state: Optional[str] = None,
                 client_requirements_taxi_class: str = None,
                 client_requirements_cargo_type: Optional[str] = None,
                 client_requirements_cargo_loaders: Optional[int] = None,
                 client_requirements_cargo_options: Optional[List['str']] = None,
                 matched_cars: Optional[List['MatchedCar']] = None,
                 warnings: Optional[List['ClaimWarning']] = None,
                 performer_info_courier_name: str = None,
                 performer_info_legal_name: str = None,
                 performer_info_car_model: Optional[str] = None,
                 performer_info_car_number: Optional[str] = None,
                 callback_properties_callback_url: str = None,
                 due: Optional[str] = None,
                 shipping_document: Optional[str] = None,
                 comment: Optional[str] = None,
                 c2c_data_payment_method_id: Optional[str] = None,
                 c2c_data_payment_type: str = None,
                 c2c_data_partner_tag: Optional[str] = None,
                 revision: int = None,
                 ):
        self.body = collections.defaultdict(dict)

        if id is not None:
            self.body["id"] = validate_fields('id', id, str)
            self.body['id'] = validate_fields('id', id, str)
        if id is None:
            raise InputParamError("<id> (=>id) of <SearchedClaimMP> is a required parameter")

        if corp_client_id is not None:
            self.body["corp_client_id"] = validate_fields('corp_client_id', corp_client_id, str)
            self.body['corp_client_id'] = validate_fields('corp_client_id', corp_client_id, Optional[str])
        if corp_client_id and len(corp_client_id) < 32:
            raise InputParamError("<corp_client_id> of <SearchedClaimMP> should contain at least 32 element")
        if corp_client_id and len(corp_client_id) > 32:
            raise InputParamError("<corp_client_id> of <SearchedClaimMP> should not contain more than 32 element")

        if yandex_uid is not None:
            self.body["yandex_uid"] = validate_fields('yandex_uid', yandex_uid, str)
            self.body['yandex_uid'] = validate_fields('yandex_uid', yandex_uid, Optional[str])

        if items is not None:
            self.body["items"] = validate_fields('items', items, List['CargoItemMP'])
            self.body['items'] = validate_fields('items', items, List['CargoItemMP'])
        if items and len(items) < 1:
            raise InputParamError("<items> of <SearchedClaimMP> should contain at least 1 element")
        if items is None:
            raise InputParamError("<items> (=>items) of <SearchedClaimMP> is a required parameter")

        if route_points is not None:
            self.body["route_points"] = validate_fields('route_points', route_points, List['ResponseCargoPointMP'])
            self.body['route_points'] = validate_fields('route_points', route_points, List['ResponseCargoPointMP'])
        if route_points and len(route_points) < 2:
            raise InputParamError("<route_points> of <SearchedClaimMP> should contain at least 2 element")
        if route_points is None:
            raise InputParamError("<route_points> (=>route_points) of <SearchedClaimMP> is a required parameter")

        if current_point_id is not None:
            self.body["current_point_id"] = validate_fields('current_point_id', current_point_id, int)
            self.body['current_point_id'] = validate_fields('current_point_id', current_point_id, Optional[int])

        if status is not None:
            self.body["status"] = validate_fields('status', status, str)
            self.body['status'] = validate_fields('status', status, Optional[str])
        if status is None:
            raise InputParamError("<status> (=>status) of <SearchedClaimMP> is a required parameter")

        if status not in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived',
                          'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning',
                          'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi',
                          'cancelled_with_items_on_hands']:
            raise InputParamError(
                "<status> of <SearchedClaimMP> should be in <new, estimating, estimating_failed, ready_for_approval, accepted, performer_lookup, performer_draft, performer_found, performer_not_found, pickup_arrived, ready_for_pickup_confirmation, pickuped, delivery_arrived, ready_for_delivery_confirmation, pay_waiting, delivered, delivered_finish, returning, return_arrived, ready_for_return_confirmation, returned, returned_finish, failed, cancelled, cancelled_with_payment, cancelled_by_taxi, cancelled_with_items_on_hands>")

        if version is not None:
            self.body["version"] = validate_fields('version', version, int)
            self.body['version'] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <SearchedClaimMP> is a required parameter")

        if error_messages is not None:
            self.body["error_messages"] = validate_fields('error_messages', error_messages, List['HumanErrorMessage'])
            self.body['error_messages'] = validate_fields('error_messages', error_messages, Optional[List['HumanErrorMessage']])

        if emergency_contact_name is not None:
            self.body["emergency_contact"]["name"] = validate_fields('emergency_contact_name', emergency_contact_name, str)
            self.body['emergency_contact_name'] = validate_fields('emergency_contact_name', emergency_contact_name, str)
        if emergency_contact_name is None:
            raise InputParamError("<emergency_contact_name> (emergency_contact=>name) of <SearchedClaimMP> is a required parameter")

        if emergency_contact_phone is not None:
            self.body["emergency_contact"]["phone"] = validate_fields('emergency_contact_phone', emergency_contact_phone, str)
            self.body['emergency_contact_phone'] = validate_fields('emergency_contact_phone', emergency_contact_phone, str)
        if emergency_contact_phone is None:
            raise InputParamError("<emergency_contact_phone> (emergency_contact=>phone) of <SearchedClaimMP> is a required parameter")

        if skip_door_to_door is not None:
            self.body["skip_door_to_door"] = validate_fields('skip_door_to_door', skip_door_to_door, bool)
            self.body['skip_door_to_door'] = validate_fields('skip_door_to_door', skip_door_to_door, Optional[bool])

        if skip_client_notify is not None:
            self.body["skip_client_notify"] = validate_fields('skip_client_notify', skip_client_notify, bool)
            self.body['skip_client_notify'] = validate_fields('skip_client_notify', skip_client_notify, Optional[bool])

        if skip_emergency_notify is not None:
            self.body["skip_emergency_notify"] = validate_fields('skip_emergency_notify', skip_emergency_notify, bool)
            self.body['skip_emergency_notify'] = validate_fields('skip_emergency_notify', skip_emergency_notify, Optional[bool])

        if skip_act is not None:
            self.body["skip_act"] = validate_fields('skip_act', skip_act, bool)
            self.body['skip_act'] = validate_fields('skip_act', skip_act, Optional[bool])

        if optional_return is not None:
            self.body["optional_return"] = validate_fields('optional_return', optional_return, bool)
            self.body['optional_return'] = validate_fields('optional_return', optional_return, Optional[bool])

        if eta is not None:
            self.body["eta"] = validate_fields('eta', eta, int)
            self.body['eta'] = validate_fields('eta', eta, Optional[int])

        if created_ts is not None:
            self.body["created_ts"] = validate_fields('created_ts', created_ts, str)
            self.body['created_ts'] = validate_fields('created_ts', created_ts, str)
        if created_ts is None:
            raise InputParamError("<created_ts> (=>created_ts) of <SearchedClaimMP> is a required parameter")

        if updated_ts is not None:
            self.body["updated_ts"] = validate_fields('updated_ts', updated_ts, str)
            self.body['updated_ts'] = validate_fields('updated_ts', updated_ts, str)
        if updated_ts is None:
            raise InputParamError("<updated_ts> (=>updated_ts) of <SearchedClaimMP> is a required parameter")

        if taxi_offer_offer_id is not None:
            self.body["taxi_offer"]["offer_id"] = validate_fields('taxi_offer_offer_id', taxi_offer_offer_id, str)
            self.body['taxi_offer_offer_id'] = validate_fields('taxi_offer_offer_id', taxi_offer_offer_id, str)
        if taxi_offer_offer_id is None:
            raise InputParamError("<taxi_offer_offer_id> (taxi_offer=>offer_id) of <SearchedClaimMP> is a required parameter")

        if taxi_offer_price_raw is not None:
            self.body["taxi_offer"]["price_raw"] = validate_fields('taxi_offer_price_raw', taxi_offer_price_raw, int)
            self.body['taxi_offer_price_raw'] = validate_fields('taxi_offer_price_raw', taxi_offer_price_raw, int)
        if taxi_offer_price_raw is None:
            raise InputParamError("<taxi_offer_price_raw> (taxi_offer=>price_raw) of <SearchedClaimMP> is a required parameter")

        if taxi_offer_price is not None:
            self.body["taxi_offer"]["price"] = validate_fields('taxi_offer_price', taxi_offer_price, str)
            self.body['taxi_offer_price'] = validate_fields('taxi_offer_price', taxi_offer_price, Optional[str])
        if taxi_offer_price is None:
            raise InputParamError("<taxi_offer_price> (taxi_offer=>price) of <SearchedClaimMP> is a required parameter")

        if pricing_offer_offer_id is not None:
            self.body["pricing"]["offer"]["offer_id"] = validate_fields('pricing_offer_offer_id', pricing_offer_offer_id, str)
            self.body['pricing_offer_offer_id'] = validate_fields('pricing_offer_offer_id', pricing_offer_offer_id, str)
        if pricing_offer_offer_id is None:
            raise InputParamError("<pricing_offer_offer_id> (pricing=>offer=>offer_id) of <SearchedClaimMP> is a required parameter")

        if pricing_offer_price_raw is not None:
            self.body["pricing"]["offer"]["price_raw"] = validate_fields('pricing_offer_price_raw', pricing_offer_price_raw, int)
            self.body['pricing_offer_price_raw'] = validate_fields('pricing_offer_price_raw', pricing_offer_price_raw, int)
        if pricing_offer_price_raw is None:
            raise InputParamError("<pricing_offer_price_raw> (pricing=>offer=>price_raw) of <SearchedClaimMP> is a required parameter")

        if pricing_offer_price is not None:
            self.body["pricing"]["offer"]["price"] = validate_fields('pricing_offer_price', pricing_offer_price, str)
            self.body['pricing_offer_price'] = validate_fields('pricing_offer_price', pricing_offer_price, str)
        if pricing_offer_price is None:
            raise InputParamError("<pricing_offer_price> (pricing=>offer=>price) of <SearchedClaimMP> is a required parameter")

        if pricing_currency is not None:
            self.body["pricing"]["currency"] = validate_fields('pricing_currency', pricing_currency, str)
            self.body['pricing_currency'] = validate_fields('pricing_currency', pricing_currency, Optional[str])

        if pricing_currency_rules_code is not None:
            self.body["pricing"]["currency_rules"]["code"] = validate_fields('pricing_currency_rules_code', pricing_currency_rules_code, str)
            self.body['pricing_currency_rules_code'] = validate_fields('pricing_currency_rules_code', pricing_currency_rules_code, str)
        if pricing_currency_rules_code is None:
            raise InputParamError("<pricing_currency_rules_code> (pricing=>currency_rules=>code) of <SearchedClaimMP> is a required parameter")

        if pricing_currency_rules_text is not None:
            self.body["pricing"]["currency_rules"]["text"] = validate_fields('pricing_currency_rules_text', pricing_currency_rules_text, str)
            self.body['pricing_currency_rules_text'] = validate_fields('pricing_currency_rules_text', pricing_currency_rules_text, str)
        if pricing_currency_rules_text is None:
            raise InputParamError("<pricing_currency_rules_text> (pricing=>currency_rules=>text) of <SearchedClaimMP> is a required parameter")

        if pricing_currency_rules_template is not None:
            self.body["pricing"]["currency_rules"]["template"] = validate_fields('pricing_currency_rules_template', pricing_currency_rules_template, str)
            self.body['pricing_currency_rules_template'] = validate_fields('pricing_currency_rules_template', pricing_currency_rules_template, str)
        if pricing_currency_rules_template is None:
            raise InputParamError("<pricing_currency_rules_template> (pricing=>currency_rules=>template) of <SearchedClaimMP> is a required parameter")

        if pricing_currency_rules_sign is not None:
            self.body["pricing"]["currency_rules"]["sign"] = validate_fields('pricing_currency_rules_sign', pricing_currency_rules_sign, str)
            self.body['pricing_currency_rules_sign'] = validate_fields('pricing_currency_rules_sign', pricing_currency_rules_sign, Optional[str])

        if pricing_final_price is not None:
            self.body["pricing"]["final_price"] = validate_fields('pricing_final_price', pricing_final_price, str)
            self.body['pricing_final_price'] = validate_fields('pricing_final_price', pricing_final_price, str)

        if available_cancel_state is not None:
            self.body["available_cancel_state"] = validate_fields('available_cancel_state', available_cancel_state, str)
            self.body['available_cancel_state'] = validate_fields('available_cancel_state', available_cancel_state, Optional[str])

        if available_cancel_state not in ['free', 'paid']:
            raise InputParamError("<available_cancel_state> of <SearchedClaimMP> should be in <free, paid>")

        if client_requirements_taxi_class is not None:
            self.body["client_requirements"]["taxi_class"] = validate_fields('client_requirements_taxi_class', client_requirements_taxi_class, str)
            self.body['client_requirements_taxi_class'] = validate_fields('client_requirements_taxi_class', client_requirements_taxi_class, str)
        if client_requirements_taxi_class is None:
            raise InputParamError("<client_requirements_taxi_class> (client_requirements=>taxi_class) of <SearchedClaimMP> is a required parameter")

        if client_requirements_cargo_type is not None:
            self.body["client_requirements"]["cargo_type"] = validate_fields('client_requirements_cargo_type', client_requirements_cargo_type, str)
            self.body['client_requirements_cargo_type'] = validate_fields('client_requirements_cargo_type', client_requirements_cargo_type, Optional[str])

        if client_requirements_cargo_loaders is not None:
            self.body["client_requirements"]["cargo_loaders"] = validate_fields('client_requirements_cargo_loaders', client_requirements_cargo_loaders, int)
            self.body['client_requirements_cargo_loaders'] = validate_fields('client_requirements_cargo_loaders', client_requirements_cargo_loaders, Optional[int])
        if client_requirements_cargo_loaders and client_requirements_cargo_loaders < 0:
            raise InputParamError("<client_requirements_cargo_loaders> of <SearchedClaimMP> should be more than 0")

        if client_requirements_cargo_options is not None:
            self.body["client_requirements"]["cargo_options"] = validate_fields('client_requirements_cargo_options', client_requirements_cargo_options, List['str'])
            self.body['client_requirements_cargo_options'] = validate_fields('client_requirements_cargo_options', client_requirements_cargo_options, Optional[List['str']])

        if matched_cars is not None:
            self.body["matched_cars"] = validate_fields('matched_cars', matched_cars, List['MatchedCar'])
            self.body['matched_cars'] = validate_fields('matched_cars', matched_cars, Optional[List['MatchedCar']])

        if warnings is not None:
            self.body["warnings"] = validate_fields('warnings', warnings, List['ClaimWarning'])
            self.body['warnings'] = validate_fields('warnings', warnings, Optional[List['ClaimWarning']])

        if performer_info_courier_name is not None:
            self.body["performer_info"]["courier_name"] = validate_fields('performer_info_courier_name', performer_info_courier_name, str)
            self.body['performer_info_courier_name'] = validate_fields('performer_info_courier_name', performer_info_courier_name, str)
        if performer_info_courier_name is None:
            raise InputParamError("<performer_info_courier_name> (performer_info=>courier_name) of <SearchedClaimMP> is a required parameter")

        if performer_info_legal_name is not None:
            self.body["performer_info"]["legal_name"] = validate_fields('performer_info_legal_name', performer_info_legal_name, str)
            self.body['performer_info_legal_name'] = validate_fields('performer_info_legal_name', performer_info_legal_name, str)
        if performer_info_legal_name is None:
            raise InputParamError("<performer_info_legal_name> (performer_info=>legal_name) of <SearchedClaimMP> is a required parameter")

        if performer_info_car_model is not None:
            self.body["performer_info"]["car_model"] = validate_fields('performer_info_car_model', performer_info_car_model, str)
            self.body['performer_info_car_model'] = validate_fields('performer_info_car_model', performer_info_car_model, Optional[str])

        if performer_info_car_number is not None:
            self.body["performer_info"]["car_number"] = validate_fields('performer_info_car_number', performer_info_car_number, str)
            self.body['performer_info_car_number'] = validate_fields('performer_info_car_number', performer_info_car_number, Optional[str])

        if callback_properties_callback_url is not None:
            self.body["callback_properties"]["callback_url"] = validate_fields('callback_properties_callback_url', callback_properties_callback_url, str)
            self.body['callback_properties_callback_url'] = validate_fields('callback_properties_callback_url', callback_properties_callback_url, str)
        if callback_properties_callback_url is None:
            raise InputParamError("<callback_properties_callback_url> (callback_properties=>callback_url) of <SearchedClaimMP> is a required parameter")

        if due is not None:
            self.body["due"] = validate_fields('due', due, str)
            self.body['due'] = validate_fields('due', due, Optional[str])

        if shipping_document is not None:
            self.body["shipping_document"] = validate_fields('shipping_document', shipping_document, str)
            self.body['shipping_document'] = validate_fields('shipping_document', shipping_document, Optional[str])

        if comment is not None:
            self.body["comment"] = validate_fields('comment', comment, str)
            self.body['comment'] = validate_fields('comment', comment, Optional[str])

        if c2c_data_payment_method_id is not None:
            self.body["c2c_data"]["payment_method_id"] = validate_fields('c2c_data_payment_method_id', c2c_data_payment_method_id, str)
            self.body['c2c_data_payment_method_id'] = validate_fields('c2c_data_payment_method_id', c2c_data_payment_method_id, Optional[str])

        if c2c_data_payment_type is not None:
            self.body["c2c_data"]["payment_type"] = validate_fields('c2c_data_payment_type', c2c_data_payment_type, str)
            self.body['c2c_data_payment_type'] = validate_fields('c2c_data_payment_type', c2c_data_payment_type, str)
        if c2c_data_payment_type is None:
            raise InputParamError("<c2c_data_payment_type> (c2c_data=>payment_type) of <SearchedClaimMP> is a required parameter")

        if c2c_data_partner_tag is not None:
            self.body["c2c_data"]["partner_tag"] = validate_fields('c2c_data_partner_tag', c2c_data_partner_tag, str)
            self.body['c2c_data_partner_tag'] = validate_fields('c2c_data_partner_tag', c2c_data_partner_tag, Optional[str])

        if revision is not None:
            self.body["revision"] = validate_fields('revision', revision, int)
            self.body['revision'] = validate_fields('revision', revision, int)
        if revision is None:
            raise InputParamError("<revision> (=>revision) of <SearchedClaimMP> is a required parameter")

    def __repr__(self):
        return "<SearchedClaimMP>"

    @property
    def id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("id")

    @property
    def corp_client_id(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("corp_client_id")

    @property
    def yandex_uid(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("yandex_uid")

    @property
    def items(self) -> List['CargoItemMP']:
        """

        :return: ???
        :rtype: List['CargoItemMP']
        """
        return [CargoItemMP(extra_id=item.get("extra_id", None),
                            pickup_point=item.get("pickup_point", None),
                            droppof_point=item.get("droppof_point", None),
                            title=item.get("title", None),
                            size_length=item.get("size", {}).get("length", None),
                            size_width=item.get("size", {}).get("width", None),
                            size_height=item.get("size", {}).get("height", None),
                            weight=item.get("weight", None),
                            cost_value=item.get("cost_value", None),
                            cost_currency=item.get("cost_currency", None),
                            quantity=item.get("quantity", None),
                            fiscalization_vat_code=item.get("fiscalization", {}).get("vat_code", None),
                            fiscalization_payment_subject=item.get("fiscalization", {}).get("payment_subject", None),
                            fiscalization_payment_mode=item.get("fiscalization", {}).get("payment_mode", None),
                            fiscalization_product_code=item.get("fiscalization", {}).get("product_code", None),
                            fiscalization_country_of_origin_code=item.get("fiscalization", {}).get("country_of_origin_code", None),
                            fiscalization_customs_declaration_number=item.get("fiscalization", {}).get("customs_declaration_number", None),
                            fiscalization_excise=item.get("fiscalization", {}).get("excise", None),
                            ) for item in self.body.get("items")]

    @property
    def route_points(self) -> List['ResponseCargoPointMP']:
        """

        :return: ???
        :rtype: List['ResponseCargoPointMP']
        """
        return [ResponseCargoPointMP(id=item.get("id", None),
                                     contact_name=item.get("contact", {}).get("name", None),
                                     contact_phone=item.get("contact", {}).get("phone", None),
                                     contact_email=item.get("contact", {}).get("email", None),
                                     address_fullname=item.get("address", {}).get("fullname", None),
                                     address_shortname=item.get("address", {}).get("shortname", None),
                                     address_coordinates=item.get("address", {}).get("coordinates", None),
                                     address_country=item.get("address", {}).get("country", None),
                                     address_city=item.get("address", {}).get("city", None),
                                     address_street=item.get("address", {}).get("street", None),
                                     address_building=item.get("address", {}).get("building", None),
                                     address_porch=item.get("address", {}).get("porch", None),
                                     address_floor=item.get("address", {}).get("floor", None),
                                     address_flat=item.get("address", {}).get("flat", None),
                                     address_sfloor=item.get("address", {}).get("sfloor", None),
                                     address_sflat=item.get("address", {}).get("sflat", None),
                                     address_door_code=item.get("address", {}).get("door_code", None),
                                     address_comment=item.get("address", {}).get("comment", None),
                                     address_uri=item.get("address", {}).get("uri", None),
                                     type=item.get("type", None),
                                     visit_order=item.get("visit_order", None),
                                     visit_status=item.get("visit_status", None),
                                     skip_confirmation=item.get("skip_confirmation", None),
                                     payment_on_delivery_client_order_id=item.get("payment_on_delivery", {}).get("client_order_id", None),
                                     payment_on_delivery_is_paid=item.get("payment_on_delivery", {}).get("is_paid", None),
                                     payment_on_delivery_cost=item.get("payment_on_delivery", {}).get("cost", None),
                                     payment_on_delivery_customer_full_name=item.get("payment_on_delivery", {}).get("customer", {}).get("full_name", None),
                                     payment_on_delivery_customer_inn=item.get("payment_on_delivery", {}).get("customer", {}).get("inn", None),
                                     payment_on_delivery_customer_email=item.get("payment_on_delivery", {}).get("customer", {}).get("email", None),
                                     payment_on_delivery_customer_phone=item.get("payment_on_delivery", {}).get("customer", {}).get("phone", None),
                                     payment_on_delivery_tax_system_code=item.get("payment_on_delivery", {}).get("tax_system_code", None),
                                     external_order_id=item.get("external_order_id", None),
                                     pickup_code=item.get("pickup_code", None),
                                     ) for item in self.body.get("route_points")]

    @property
    def current_point_id(self) -> Optional[int]:
        """

        :return: ???
        :rtype: Optional[int]
        """
        return self.body.get("current_point_id")

    @property
    def status(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("status")

    @property
    def version(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("version")

    @property
    def error_messages(self) -> Optional[List['HumanErrorMessage']]:
        """

        :return: ???
        :rtype: Optional[List['HumanErrorMessage']]
        """
        return [HumanErrorMessage(code=item.get("code", None),
                                  message=item.get("message", None),
                                  ) for item in self.body.get("error_messages")]

    @property
    def emergency_contact_name(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("emergency_contact_name")

    @property
    def emergency_contact_phone(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("emergency_contact_phone")

    @property
    def skip_door_to_door(self) -> Optional[bool]:
        """

        :return: ???
        :rtype: Optional[bool]
        """
        return self.body.get("skip_door_to_door")

    @property
    def skip_client_notify(self) -> Optional[bool]:
        """

        :return: ???
        :rtype: Optional[bool]
        """
        return self.body.get("skip_client_notify")

    @property
    def skip_emergency_notify(self) -> Optional[bool]:
        """

        :return: ???
        :rtype: Optional[bool]
        """
        return self.body.get("skip_emergency_notify")

    @property
    def skip_act(self) -> Optional[bool]:
        """

        :return: ???
        :rtype: Optional[bool]
        """
        return self.body.get("skip_act")

    @property
    def optional_return(self) -> Optional[bool]:
        """

        :return: ???
        :rtype: Optional[bool]
        """
        return self.body.get("optional_return")

    @property
    def eta(self) -> Optional[int]:
        """

        :return: ???
        :rtype: Optional[int]
        """
        return self.body.get("eta")

    @property
    def created_ts(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("created_ts")

    @property
    def updated_ts(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("updated_ts")

    @property
    def taxi_offer_offer_id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("taxi_offer_offer_id")

    @property
    def taxi_offer_price_raw(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("taxi_offer_price_raw")

    @property
    def taxi_offer_price(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("taxi_offer_price")

    @property
    def pricing_offer_offer_id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("pricing_offer_offer_id")

    @property
    def pricing_offer_price_raw(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("pricing_offer_price_raw")

    @property
    def pricing_offer_price(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("pricing_offer_price")

    @property
    def pricing_currency(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("pricing_currency")

    @property
    def pricing_currency_rules_code(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("pricing_currency_rules_code")

    @property
    def pricing_currency_rules_text(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("pricing_currency_rules_text")

    @property
    def pricing_currency_rules_template(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("pricing_currency_rules_template")

    @property
    def pricing_currency_rules_sign(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("pricing_currency_rules_sign")

    @property
    def pricing_final_price(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("pricing_final_price")

    @property
    def available_cancel_state(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("available_cancel_state")

    @property
    def client_requirements_taxi_class(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("client_requirements_taxi_class")

    @property
    def client_requirements_cargo_type(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("client_requirements_cargo_type")

    @property
    def client_requirements_cargo_loaders(self) -> Optional[int]:
        """

        :return: ???
        :rtype: Optional[int]
        """
        return self.body.get("client_requirements_cargo_loaders")

    @property
    def client_requirements_cargo_options(self) -> Optional[List['str']]:
        """

        :return: ???
        :rtype: Optional[List['str']]
        """
        return [item for item in self.body.get("client_requirements_cargo_options")]

    @property
    def matched_cars(self) -> Optional[List['MatchedCar']]:
        """

        :return: ???
        :rtype: Optional[List['MatchedCar']]
        """
        return [MatchedCar(taxi_class=item.get("taxi_class", None),
                           client_taxi_class=item.get("client_taxi_class", None),
                           cargo_type=item.get("cargo_type", None),
                           cargo_type_int=item.get("cargo_type_int", None),
                           cargo_loaders=item.get("cargo_loaders", None),
                           door_to_door=item.get("door_to_door", None),
                           cargo_points=item.get("cargo_points", None),
                           cargo_points_field=item.get("cargo_points_field", None),
                           ) for item in self.body.get("matched_cars")]

    @property
    def warnings(self) -> Optional[List['ClaimWarning']]:
        """

        :return: ???
        :rtype: Optional[List['ClaimWarning']]
        """
        return [ClaimWarning(source=item.get("source", None),
                             code=item.get("code", None),
                             message=item.get("message", None),
                             ) for item in self.body.get("warnings")]

    @property
    def performer_info_courier_name(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("performer_info_courier_name")

    @property
    def performer_info_legal_name(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("performer_info_legal_name")

    @property
    def performer_info_car_model(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("performer_info_car_model")

    @property
    def performer_info_car_number(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("performer_info_car_number")

    @property
    def callback_properties_callback_url(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("callback_properties_callback_url")

    @property
    def due(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("due")

    @property
    def shipping_document(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("shipping_document")

    @property
    def comment(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("comment")

    @property
    def c2c_data_payment_method_id(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("c2c_data_payment_method_id")

    @property
    def c2c_data_payment_type(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("c2c_data_payment_type")

    @property
    def c2c_data_partner_tag(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("c2c_data_partner_tag")

    @property
    def revision(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("revision")


class SearchClaimsResponseMP(YCBase):
    """
        ???
        Результат поиска

            :param List['SearchedClaimMP'] claims: ??? *(Обязательный параметр)*
    """

    def __init__(self,
                 claims: List['SearchedClaimMP'] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if claims is not None:
            self.body["claims"] = validate_fields('claims', claims, List['SearchedClaimMP'])
            self.body['claims'] = validate_fields('claims', claims, List['SearchedClaimMP'])
        if claims is None:
            raise InputParamError("<claims> (=>claims) of <SearchClaimsResponseMP> is a required parameter")

    def __repr__(self):
        return "<SearchClaimsResponseMP>"

    @property
    def claims(self) -> List['SearchedClaimMP']:
        """

        :return: Результат поиска
        :rtype: List['SearchedClaimMP']
        """
        return [SearchedClaimMP(id=item.get("id", None),
                                corp_client_id=item.get("corp_client_id", None),
                                yandex_uid=item.get("yandex_uid", None),
                                items=item.get("items", None),
                                route_points=item.get("route_points", None),
                                current_point_id=item.get("current_point_id", None),
                                status=item.get("status", None),
                                version=item.get("version", None),
                                error_messages=item.get("error_messages", None),
                                emergency_contact_name=item.get("emergency_contact", {}).get("name", None),
                                emergency_contact_phone=item.get("emergency_contact", {}).get("phone", None),
                                skip_door_to_door=item.get("skip_door_to_door", None),
                                skip_client_notify=item.get("skip_client_notify", None),
                                skip_emergency_notify=item.get("skip_emergency_notify", None),
                                skip_act=item.get("skip_act", None),
                                optional_return=item.get("optional_return", None),
                                eta=item.get("eta", None),
                                created_ts=item.get("created_ts", None),
                                updated_ts=item.get("updated_ts", None),
                                taxi_offer_offer_id=item.get("taxi_offer", {}).get("offer_id", None),
                                taxi_offer_price_raw=item.get("taxi_offer", {}).get("price_raw", None),
                                taxi_offer_price=item.get("taxi_offer", {}).get("price", None),
                                pricing_offer_offer_id=item.get("pricing", {}).get("offer", {}).get("offer_id", None),
                                pricing_offer_price_raw=item.get("pricing", {}).get("offer", {}).get("price_raw", None),
                                pricing_offer_price=item.get("pricing", {}).get("offer", {}).get("price", None),
                                pricing_currency=item.get("pricing", {}).get("currency", None),
                                pricing_currency_rules_code=item.get("pricing", {}).get("currency_rules", {}).get("code", None),
                                pricing_currency_rules_text=item.get("pricing", {}).get("currency_rules", {}).get("text", None),
                                pricing_currency_rules_template=item.get("pricing", {}).get("currency_rules", {}).get("template", None),
                                pricing_currency_rules_sign=item.get("pricing", {}).get("currency_rules", {}).get("sign", None),
                                pricing_final_price=item.get("pricing", {}).get("final_price", None),
                                available_cancel_state=item.get("available_cancel_state", None),
                                client_requirements_taxi_class=item.get("client_requirements", {}).get("taxi_class", None),
                                client_requirements_cargo_type=item.get("client_requirements", {}).get("cargo_type", None),
                                client_requirements_cargo_loaders=item.get("client_requirements", {}).get("cargo_loaders", None),
                                client_requirements_cargo_options=item.get("client_requirements", {}).get("cargo_options", None),
                                matched_cars=item.get("matched_cars", None),
                                warnings=item.get("warnings", None),
                                performer_info_courier_name=item.get("performer_info", {}).get("courier_name", None),
                                performer_info_legal_name=item.get("performer_info", {}).get("legal_name", None),
                                performer_info_car_model=item.get("performer_info", {}).get("car_model", None),
                                performer_info_car_number=item.get("performer_info", {}).get("car_number", None),
                                callback_properties_callback_url=item.get("callback_properties", {}).get("callback_url", None),
                                due=item.get("due", None),
                                shipping_document=item.get("shipping_document", None),
                                comment=item.get("comment", None),
                                c2c_data_payment_method_id=item.get("c2c_data", {}).get("payment_method_id", None),
                                c2c_data_payment_type=item.get("c2c_data", {}).get("payment_type", None),
                                c2c_data_partner_tag=item.get("c2c_data", {}).get("partner_tag", None),
                                revision=item.get("revision", None),
                                ) for item in self.body.get("claims")]


class VoiceforwardingResponse(YCBase):
    """
        ???
        ???

            :param str phone: Номер телефона *(Обязательный параметр)* (+79099999998)
            :param str ext: Добавочный номер *(Обязательный параметр)* (0163)
            :param int ttl_seconds: Время, в течение которого этот номер действителен *(Обязательный параметр)*
    """

    def __init__(self,
                 phone: str = None,
                 ext: str = None,
                 ttl_seconds: int = None,
                 ):
        self.body = collections.defaultdict(dict)

        if phone is not None:
            self.body["phone"] = validate_fields('phone', phone, str)
            self.body['phone'] = validate_fields('phone', phone, str)
        if phone is None:
            raise InputParamError("<phone> (=>phone) of <VoiceforwardingResponse> is a required parameter")

        if ext is not None:
            self.body["ext"] = validate_fields('ext', ext, str)
            self.body['ext'] = validate_fields('ext', ext, str)
        if ext is None:
            raise InputParamError("<ext> (=>ext) of <VoiceforwardingResponse> is a required parameter")

        if ttl_seconds is not None:
            self.body["ttl_seconds"] = validate_fields('ttl_seconds', ttl_seconds, int)
            self.body['ttl_seconds'] = validate_fields('ttl_seconds', ttl_seconds, int)
        if ttl_seconds and ttl_seconds < 2088:
            raise InputParamError("<ttl_seconds> of <VoiceforwardingResponse> should be more than 2088")
        if ttl_seconds is None:
            raise InputParamError("<ttl_seconds> (=>ttl_seconds) of <VoiceforwardingResponse> is a required parameter")

    def __repr__(self):
        return "<VoiceforwardingResponse>"

    @property
    def phone(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("phone")

    @property
    def ext(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("ext")

    @property
    def ttl_seconds(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("ttl_seconds")


class ClaimsReportStatusResponse(YCBase):
    """
        ???
        ???

            :param str task_id: task_id из запроса *(Обязательный параметр)* (f9b4825f45f4914affaeb07fbae9757)
            :param str status: ??? *(Обязательный параметр)* (in_progress)

                * **in_progress** - ???
                * **retry** - ???
                * **complete** - ???
                * **failed** - ???

            :param str author: Yandex Login автора отчета *(Обязательный параметр)* (morty)
            :param str created_at: ??? *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
            :param str request_since_date: ??? *(Обязательный параметр)* (2020-01-01)
            :param str request_till_date: ??? *(Обязательный параметр)* (2020-01-02)
            :param Optional[str] request_lang: Язык, на котором надо генерировать отчет.Если не указан, будет использован Accept-Language (ru)
            :param Optional[str] request_department_id: ID отдела (значение игнорируется). Поле нужно для совместимости с API КК
            :param str request_idempotency_token: Уникальный для данного клиента токен идемпотентности *(Обязательный параметр)* (f9b4825f45f64914affaeb07fbae9757)
            :param Optional[str] url: Временная ссылка для скачивания отчета (https://example.com)
    """

    def __init__(self,
                 task_id: str = None,
                 status: str = None,
                 author: str = None,
                 created_at: str = None,
                 request_since_date: str = None,
                 request_till_date: str = None,
                 request_lang: Optional[str] = None,
                 request_department_id: Optional[str] = None,
                 request_idempotency_token: str = None,
                 url: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if task_id is not None:
            self.body["task_id"] = validate_fields('task_id', task_id, str)
            self.body['task_id'] = validate_fields('task_id', task_id, str)
        if task_id is None:
            raise InputParamError("<task_id> (=>task_id) of <ClaimsReportStatusResponse> is a required parameter")

        if status is not None:
            self.body["status"] = validate_fields('status', status, str)
            self.body['status'] = validate_fields('status', status, str)
        if status is None:
            raise InputParamError("<status> (=>status) of <ClaimsReportStatusResponse> is a required parameter")

        if status not in ['in_progress', 'retry', 'complete', 'failed']:
            raise InputParamError("<status> of <ClaimsReportStatusResponse> should be in <in_progress, retry, complete, failed>")

        if author is not None:
            self.body["author"] = validate_fields('author', author, str)
            self.body['author'] = validate_fields('author', author, str)
        if author is None:
            raise InputParamError("<author> (=>author) of <ClaimsReportStatusResponse> is a required parameter")

        if created_at is not None:
            self.body["created_at"] = validate_fields('created_at', created_at, str)
            self.body['created_at'] = validate_fields('created_at', created_at, str)
        if created_at is None:
            raise InputParamError("<created_at> (=>created_at) of <ClaimsReportStatusResponse> is a required parameter")

        if request_since_date is not None:
            self.body["request"]["since_date"] = validate_fields('request_since_date', request_since_date, str)
            self.body['request_since_date'] = validate_fields('request_since_date', request_since_date, str)
        if request_since_date is None:
            raise InputParamError("<request_since_date> (request=>since_date) of <ClaimsReportStatusResponse> is a required parameter")

        if request_till_date is not None:
            self.body["request"]["till_date"] = validate_fields('request_till_date', request_till_date, str)
            self.body['request_till_date'] = validate_fields('request_till_date', request_till_date, str)
        if request_till_date is None:
            raise InputParamError("<request_till_date> (request=>till_date) of <ClaimsReportStatusResponse> is a required parameter")

        if request_lang is not None:
            self.body["request"]["lang"] = validate_fields('request_lang', request_lang, str)
            self.body['request_lang'] = validate_fields('request_lang', request_lang, Optional[str])

        if request_department_id is not None:
            self.body["request"]["department_id"] = validate_fields('request_department_id', request_department_id, str)
            self.body['request_department_id'] = validate_fields('request_department_id', request_department_id, Optional[str])

        if request_idempotency_token is not None:
            self.body["request"]["idempotency_token"] = validate_fields('request_idempotency_token', request_idempotency_token, str)
            self.body['request_idempotency_token'] = validate_fields('request_idempotency_token', request_idempotency_token, str)
        if request_idempotency_token is None:
            raise InputParamError("<request_idempotency_token> (request=>idempotency_token) of <ClaimsReportStatusResponse> is a required parameter")

        if url is not None:
            self.body["url"] = validate_fields('url', url, str)
            self.body['url'] = validate_fields('url', url, Optional[str])

    def __repr__(self):
        return "<ClaimsReportStatusResponse>"

    @property
    def task_id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("task_id")

    @property
    def status(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("status")

    @property
    def author(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("author")

    @property
    def created_at(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("created_at")

    @property
    def request_since_date(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("request_since_date")

    @property
    def request_till_date(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("request_till_date")

    @property
    def request_lang(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("request_lang")

    @property
    def request_department_id(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("request_department_id")

    @property
    def request_idempotency_token(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("request_idempotency_token")

    @property
    def url(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("url")


class ClaimsReportGenerateResponse(YCBase):
    """
        ???
        ???

            :param str task_id: ID, по которому можно запрашивать статус *(Обязательный параметр)* (f9b4825f45f64914affaeb07fbae9757)
    """

    def __init__(self,
                 task_id: str = None,
                 ):
        self.body = collections.defaultdict(dict)

        if task_id is not None:
            self.body["task_id"] = validate_fields('task_id', task_id, str)
            self.body['task_id'] = validate_fields('task_id', task_id, str)
        if task_id is None:
            raise InputParamError("<task_id> (=>task_id) of <ClaimsReportGenerateResponse> is a required parameter")

    def __repr__(self):
        return "<ClaimsReportGenerateResponse>"

    @property
    def task_id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("task_id")


class PerformerPositionResponse(YCBase):
    """
        ???
        performer position info

            :param int position_lat: Широта *(Обязательный параметр)*
            :param int position_lon: Долгота *(Обязательный параметр)*
            :param int position_timestamp: Время снятия сигнала GPS, unix-time *(Обязательный параметр)*
            :param Optional[int] position_accuracy: Точность GPS. Пока запрещена к передаче т.к. не решилис единицами измерения.
            :param Optional[int] position_speed: Средняя скорость, в м/с
            :param Optional[int] position_direction: Направление. Угол от 0 градусов до 360 градусов от направления на север,по часовой стрелке. 0 - север, 90 - восток, 180 - юг,270 - запад.
    """

    def __init__(self,
                 position_lat: int = None,
                 position_lon: int = None,
                 position_timestamp: int = None,
                 position_accuracy: Optional[int] = None,
                 position_speed: Optional[int] = None,
                 position_direction: Optional[int] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if position_lat is not None:
            self.body["position"]["lat"] = validate_fields('position_lat', position_lat, int)
            self.body['position_lat'] = validate_fields('position_lat', position_lat, int)
        if position_lat and position_lat < -90:
            raise InputParamError("<position_lat> of <PerformerPositionResponse> should be more than -90")
        if position_lat and position_lat > 90:
            raise InputParamError("<position_lat> of <PerformerPositionResponse> should be less than 90")
        if position_lat is None:
            raise InputParamError("<position_lat> (position=>lat) of <PerformerPositionResponse> is a required parameter")

        if position_lon is not None:
            self.body["position"]["lon"] = validate_fields('position_lon', position_lon, int)
            self.body['position_lon'] = validate_fields('position_lon', position_lon, int)
        if position_lon and position_lon < -180:
            raise InputParamError("<position_lon> of <PerformerPositionResponse> should be more than -180")
        if position_lon and position_lon > 180:
            raise InputParamError("<position_lon> of <PerformerPositionResponse> should be less than 180")
        if position_lon is None:
            raise InputParamError("<position_lon> (position=>lon) of <PerformerPositionResponse> is a required parameter")

        if position_timestamp is not None:
            self.body["position"]["timestamp"] = validate_fields('position_timestamp', position_timestamp, int)
            self.body['position_timestamp'] = validate_fields('position_timestamp', position_timestamp, int)
        if position_timestamp is None:
            raise InputParamError("<position_timestamp> (position=>timestamp) of <PerformerPositionResponse> is a required parameter")

        if position_accuracy is not None:
            self.body["position"]["accuracy"] = validate_fields('position_accuracy', position_accuracy, int)
            self.body['position_accuracy'] = validate_fields('position_accuracy', position_accuracy, Optional[int])

        if position_speed is not None:
            self.body["position"]["speed"] = validate_fields('position_speed', position_speed, int)
            self.body['position_speed'] = validate_fields('position_speed', position_speed, Optional[int])

        if position_direction is not None:
            self.body["position"]["direction"] = validate_fields('position_direction', position_direction, int)
            self.body['position_direction'] = validate_fields('position_direction', position_direction, Optional[int])

    def __repr__(self):
        return "<PerformerPositionResponse>"

    @property
    def position_lat(self) -> int:
        """

        :return: performer position info
        :rtype: int
        """
        return self.body.get("position_lat")

    @property
    def position_lon(self) -> int:
        """

        :return: performer position info
        :rtype: int
        """
        return self.body.get("position_lon")

    @property
    def position_timestamp(self) -> int:
        """

        :return: performer position info
        :rtype: int
        """
        return self.body.get("position_timestamp")

    @property
    def position_accuracy(self) -> Optional[int]:
        """

        :return: performer position info
        :rtype: Optional[int]
        """
        return self.body.get("position_accuracy")

    @property
    def position_speed(self) -> Optional[int]:
        """

        :return: performer position info
        :rtype: Optional[int]
        """
        return self.body.get("position_speed")

    @property
    def position_direction(self) -> Optional[int]:
        """

        :return: performer position info
        :rtype: Optional[int]
        """
        return self.body.get("position_direction")


class Event(YCBase):
    """
        ???
        ???

            :param int operation_id: ??? *(Обязательный параметр)* (1)
            :param str claim_id: Идентификатор заявки claim_id *(Обязательный параметр)* (3b8d1af142664fde824626a7c19e2bd9)
            :param str change_type: Тип изменения. Возможные значения status_changed — изменение статуса; price_changed — изменение цены *(Обязательный параметр)* (status_changed)
            :param str updated_ts: Время события в формате ISO 8601 *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
            :param str new_status: Статус заявки (new)

                * **new** - ???
                * **estimating** - ???
                * **estimating_failed** - ???
                * **ready_for_approval** - ???
                * **accepted** - ???
                * **performer_lookup** - ???
                * **performer_draft** - ???
                * **performer_found** - ???
                * **performer_not_found** - ???
                * **pickup_arrived** - ???
                * **ready_for_pickup_confirmation** - ???
                * **pickuped** - ???
                * **delivery_arrived** - ???
                * **ready_for_delivery_confirmation** - ???
                * **pay_waiting** - ???
                * **delivered** - ???
                * **delivered_finish** - ???
                * **returning** - ???
                * **return_arrived** - ???
                * **ready_for_return_confirmation** - ???
                * **returned** - ???
                * **returned_finish** - ???
                * **failed** - ???
                * **cancelled** - ???
                * **cancelled_with_payment** - ???
                * **cancelled_by_taxi** - ???
                * **cancelled_with_items_on_hands** - ???

            :param Optional[str] new_price: ??? (20.00)
            :param Optional[str] new_currency: ??? (RUB)
            :param Optional[str] resolution: Резолюция терминального статуса (success)

                * **success** - ???
                * **failed** - ???

            :param int revision: Версия изменения заявки *(Обязательный параметр)* (1)
            :param Optional[str] client_id: ??? (95d010b2471041499b8cb1bfa282692f)
    """

    def __init__(self,
                 operation_id: int = None,
                 claim_id: str = None,
                 change_type: str = None,
                 updated_ts: str = None,
                 new_status: str = None,
                 new_price: Optional[str] = None,
                 new_currency: Optional[str] = None,
                 resolution: Optional[str] = None,
                 revision: int = None,
                 client_id: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if operation_id is not None:
            self.body["operation_id"] = validate_fields('operation_id', operation_id, int)
            self.body['operation_id'] = validate_fields('operation_id', operation_id, int)
        if operation_id is None:
            raise InputParamError("<operation_id> (=>operation_id) of <Event> is a required parameter")

        if claim_id is not None:
            self.body["claim_id"] = validate_fields('claim_id', claim_id, str)
            self.body['claim_id'] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <Event> is a required parameter")

        if change_type is not None:
            self.body["change_type"] = validate_fields('change_type', change_type, str)
            self.body['change_type'] = validate_fields('change_type', change_type, str)
        if change_type is None:
            raise InputParamError("<change_type> (=>change_type) of <Event> is a required parameter")

        if updated_ts is not None:
            self.body["updated_ts"] = validate_fields('updated_ts', updated_ts, str)
            self.body['updated_ts'] = validate_fields('updated_ts', updated_ts, str)
        if updated_ts is None:
            raise InputParamError("<updated_ts> (=>updated_ts) of <Event> is a required parameter")

        if new_status is not None:
            self.body["new_status"] = validate_fields('new_status', new_status, str)
            self.body['new_status'] = validate_fields('new_status', new_status, str)

        if new_status not in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found',
                              'pickup_arrived', 'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish',
                              'returning', 'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi',
                              'cancelled_with_items_on_hands']:
            raise InputParamError(
                "<new_status> of <Event> should be in <new, estimating, estimating_failed, ready_for_approval, accepted, performer_lookup, performer_draft, performer_found, performer_not_found, pickup_arrived, ready_for_pickup_confirmation, pickuped, delivery_arrived, ready_for_delivery_confirmation, pay_waiting, delivered, delivered_finish, returning, return_arrived, ready_for_return_confirmation, returned, returned_finish, failed, cancelled, cancelled_with_payment, cancelled_by_taxi, cancelled_with_items_on_hands>")

        if new_price is not None:
            self.body["new_price"] = validate_fields('new_price', new_price, str)
            self.body['new_price'] = validate_fields('new_price', new_price, Optional[str])

        if new_currency is not None:
            self.body["new_currency"] = validate_fields('new_currency', new_currency, str)
            self.body['new_currency'] = validate_fields('new_currency', new_currency, Optional[str])

        if resolution is not None:
            self.body["resolution"] = validate_fields('resolution', resolution, str)
            self.body['resolution'] = validate_fields('resolution', resolution, Optional[str])

        if resolution not in ['success', 'failed']:
            raise InputParamError("<resolution> of <Event> should be in <success, failed>")

        if revision is not None:
            self.body["revision"] = validate_fields('revision', revision, int)
            self.body['revision'] = validate_fields('revision', revision, int)
        if revision is None:
            raise InputParamError("<revision> (=>revision) of <Event> is a required parameter")

        if client_id is not None:
            self.body["client_id"] = validate_fields('client_id', client_id, str)
            self.body['client_id'] = validate_fields('client_id', client_id, Optional[str])

    def __repr__(self):
        return "<Event>"

    @property
    def operation_id(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("operation_id")

    @property
    def claim_id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("claim_id")

    @property
    def change_type(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("change_type")

    @property
    def updated_ts(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("updated_ts")

    @property
    def new_status(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("new_status")

    @property
    def new_price(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("new_price")

    @property
    def new_currency(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("new_currency")

    @property
    def resolution(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("resolution")

    @property
    def revision(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("revision")

    @property
    def client_id(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("client_id")


class HumanErrorMessage(YCBase):
    """
        ???
        ???

            :param str code: Машино-понятный код ошибки *(Обязательный параметр)* (some_error)
            :param str message: Человеко-понятный локализованный текст ошибки *(Обязательный параметр)* (Some error)
    """

    def __init__(self,
                 code: str = None,
                 message: str = None,
                 ):
        self.body = collections.defaultdict(dict)

        if code is not None:
            self.body["code"] = validate_fields('code', code, str)
            self.body['code'] = validate_fields('code', code, str)
        if code is None:
            raise InputParamError("<code> (=>code) of <HumanErrorMessage> is a required parameter")

        if message is not None:
            self.body["message"] = validate_fields('message', message, str)
            self.body['message'] = validate_fields('message', message, str)
        if message is None:
            raise InputParamError("<message> (=>message) of <HumanErrorMessage> is a required parameter")

    def __repr__(self):
        return "<HumanErrorMessage>"

    @property
    def code(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("code")

    @property
    def message(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("message")


class ClaimRequirement(YCBase):
    """
        ???
        Дополнительные требования к заявке

    """

    def __init__(self,
                 ):
        self.body = collections.defaultdict(dict)

    def __repr__(self):
        return "<ClaimRequirement>"


class CargoPointMP(YCBase):
    """
        ???
        Описание точки в заявке с мультиточками

            :param Optional[int] point_id: Целочисленный идентификатор точки *(Обязательный параметр)* (6987)
            :param Optional[int] visit_order: Порядок посещения точки *(Обязательный параметр)* (1)
            :param str contact_name: Имя контактного лица *(Обязательный параметр)* (Морти)
            :param str contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999998)
            :param Optional[str] contact_email: Email — обязательный параметр для точек source и return (morty@yandex.ru)
            :param str address_fullname: Полное название с указанием города (Москва, Садовническая набережная, 82с2, БЦ Аврора) *(Обязательный параметр)* (Санкт-Петербург Большая Монетная улица 1к1А)
            :param Optional[str] address_shortname: Адрес в пределах города, как показывается на Таксометре (Садовническая набережная, 82с2, БЦ Аврора) (Большая Монетная улица, 1к1А)
            :param List['int'] address_coordinates: Массив из двух вещественных чисел [долгота, широта]. Порядок важен! *(Обязательный параметр)*
            :param Optional[str] address_country: Страна (Российская Федерация)
            :param Optional[str] address_city: Город (Санкт-Петербург)
            :param Optional[str] address_street: Улица (Большая Монетная улица)
            :param Optional[str] address_building: Строение (23к1А)
            :param Optional[str] address_porch: Подъезд (может быть A) (A)
            :param Optional[int] address_floor: Этаж (DEPRECATED) (1)
            :param Optional[int] address_flat: Квартира (DEPRECATED) (1)
            :param Optional[str] address_sfloor: Этаж (1)
            :param Optional[str] address_sflat: Квартира (1)
            :param Optional[str] address_door_code: Код домофона (169)
            :param Optional[str] address_comment: Комментарий для доставщика (Домофон не работает)
            :param Optional[str] address_uri: Карточный uri геообъекта (ymapsbm1://geo?ll=38.805%2C55.084)
            :param Optional[bool] skip_confirmation: Пропускать подтверждение через SMS в данной точке
            :param str type: Тип точки *(Обязательный параметр)* (source)

                * **source** - ???
                * **destination** - ???
                * **return** - ???

            :param str payment_on_delivery_client_order_id: id заказа *(Обязательный параметр)* (100)
            :param Optional[str] payment_on_delivery_cost: Decimal(19, 4) *(Обязательный параметр)* (12.50)
            :param Optional[str] payment_on_delivery_customer_full_name: Для юридического лица — название организации, для ИП и физического лица — ФИО (Morty)
            :param Optional[str] payment_on_delivery_customer_inn: ИНН пользователя (10 или 12 цифр) (3664069397)
            :param Optional[str] payment_on_delivery_customer_email: Электронная почта пользователя. Если не указано, будет использована почта получателя из точки (morty@yandex.ru)
            :param Optional[str] payment_on_delivery_customer_phone: Телефон пользователя. Если не указано, будет использован телефон получателя из точки (79000000000)
            :param Optional[int] payment_on_delivery_tax_system_code: Система налогообложения магазина (1)
            :param Optional[str] payment_on_delivery_currency: Трехзначный код валюты, в которой ведется расчет (RUB)
            :param Optional[str] external_order_id: Номер заказа клиента (100)
            :param Optional[str] pickup_code: Код выдачи товара (ПВЗ) (8934)
    """

    def __init__(self,
                 point_id: Optional[int] = None,
                 visit_order: Optional[int] = None,
                 contact_name: str = None,
                 contact_phone: str = None,
                 contact_email: Optional[str] = None,
                 address_fullname: str = None,
                 address_shortname: Optional[str] = None,
                 address_coordinates: List['int'] = None,
                 address_country: Optional[str] = None,
                 address_city: Optional[str] = None,
                 address_street: Optional[str] = None,
                 address_building: Optional[str] = None,
                 address_porch: Optional[str] = None,
                 address_floor: Optional[int] = None,
                 address_flat: Optional[int] = None,
                 address_sfloor: Optional[str] = None,
                 address_sflat: Optional[str] = None,
                 address_door_code: Optional[str] = None,
                 address_comment: Optional[str] = None,
                 address_uri: Optional[str] = None,
                 skip_confirmation: Optional[bool] = None,
                 type: str = None,
                 payment_on_delivery_client_order_id: str = None,
                 payment_on_delivery_cost: Optional[str] = None,
                 payment_on_delivery_customer_full_name: Optional[str] = None,
                 payment_on_delivery_customer_inn: Optional[str] = None,
                 payment_on_delivery_customer_email: Optional[str] = None,
                 payment_on_delivery_customer_phone: Optional[str] = None,
                 payment_on_delivery_tax_system_code: Optional[int] = None,
                 payment_on_delivery_currency: Optional[str] = None,
                 external_order_id: Optional[str] = None,
                 pickup_code: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if point_id is not None:
            self.body["point_id"] = validate_fields('point_id', point_id, int)
            self.body['point_id'] = validate_fields('point_id', point_id, Optional[int])
        if point_id is None:
            raise InputParamError("<point_id> (=>point_id) of <CargoPointMP> is a required parameter")

        if visit_order is not None:
            self.body["visit_order"] = validate_fields('visit_order', visit_order, int)
            self.body['visit_order'] = validate_fields('visit_order', visit_order, Optional[int])
        if visit_order is None:
            raise InputParamError("<visit_order> (=>visit_order) of <CargoPointMP> is a required parameter")

        if contact_name is not None:
            self.body["contact"]["name"] = validate_fields('contact_name', contact_name, str)
            self.body['contact_name'] = validate_fields('contact_name', contact_name, str)
        if contact_name is None:
            raise InputParamError("<contact_name> (contact=>name) of <CargoPointMP> is a required parameter")

        if contact_phone is not None:
            self.body["contact"]["phone"] = validate_fields('contact_phone', contact_phone, str)
            self.body['contact_phone'] = validate_fields('contact_phone', contact_phone, str)
        if contact_phone is None:
            raise InputParamError("<contact_phone> (contact=>phone) of <CargoPointMP> is a required parameter")

        if contact_email is not None:
            self.body["contact"]["email"] = validate_fields('contact_email', contact_email, str)
            self.body['contact_email'] = validate_fields('contact_email', contact_email, Optional[str])

        if address_fullname is not None:
            self.body["address"]["fullname"] = validate_fields('address_fullname', address_fullname, str)
            self.body['address_fullname'] = validate_fields('address_fullname', address_fullname, str)
        if address_fullname is None:
            raise InputParamError("<address_fullname> (address=>fullname) of <CargoPointMP> is a required parameter")

        if address_shortname is not None:
            self.body["address"]["shortname"] = validate_fields('address_shortname', address_shortname, str)
            self.body['address_shortname'] = validate_fields('address_shortname', address_shortname, Optional[str])

        if address_coordinates is not None:
            self.body["address"]["coordinates"] = validate_fields('address_coordinates', address_coordinates, List['int'])
            self.body['address_coordinates'] = validate_fields('address_coordinates', address_coordinates, List['int'])
        if address_coordinates and len(address_coordinates) < 2:
            raise InputParamError("<address_coordinates> of <CargoPointMP> should contain at least 2 element")
        if address_coordinates and len(address_coordinates) > 2:
            raise InputParamError("<address_coordinates> of <CargoPointMP> should not contain more than 2 element")
        if address_coordinates is None:
            raise InputParamError("<address_coordinates> (address=>coordinates) of <CargoPointMP> is a required parameter")

        if address_country is not None:
            self.body["address"]["country"] = validate_fields('address_country', address_country, str)
            self.body['address_country'] = validate_fields('address_country', address_country, Optional[str])

        if address_city is not None:
            self.body["address"]["city"] = validate_fields('address_city', address_city, str)
            self.body['address_city'] = validate_fields('address_city', address_city, Optional[str])

        if address_street is not None:
            self.body["address"]["street"] = validate_fields('address_street', address_street, str)
            self.body['address_street'] = validate_fields('address_street', address_street, Optional[str])

        if address_building is not None:
            self.body["address"]["building"] = validate_fields('address_building', address_building, str)
            self.body['address_building'] = validate_fields('address_building', address_building, Optional[str])

        if address_porch is not None:
            self.body["address"]["porch"] = validate_fields('address_porch', address_porch, str)
            self.body['address_porch'] = validate_fields('address_porch', address_porch, Optional[str])

        if address_floor is not None:
            self.body["address"]["floor"] = validate_fields('address_floor', address_floor, int)
            self.body['address_floor'] = validate_fields('address_floor', address_floor, Optional[int])

        if address_flat is not None:
            self.body["address"]["flat"] = validate_fields('address_flat', address_flat, int)
            self.body['address_flat'] = validate_fields('address_flat', address_flat, Optional[int])

        if address_sfloor is not None:
            self.body["address"]["sfloor"] = validate_fields('address_sfloor', address_sfloor, str)
            self.body['address_sfloor'] = validate_fields('address_sfloor', address_sfloor, Optional[str])

        if address_sflat is not None:
            self.body["address"]["sflat"] = validate_fields('address_sflat', address_sflat, str)
            self.body['address_sflat'] = validate_fields('address_sflat', address_sflat, Optional[str])

        if address_door_code is not None:
            self.body["address"]["door_code"] = validate_fields('address_door_code', address_door_code, str)
            self.body['address_door_code'] = validate_fields('address_door_code', address_door_code, Optional[str])

        if address_comment is not None:
            self.body["address"]["comment"] = validate_fields('address_comment', address_comment, str)
            self.body['address_comment'] = validate_fields('address_comment', address_comment, Optional[str])

        if address_uri is not None:
            self.body["address"]["uri"] = validate_fields('address_uri', address_uri, str)
            self.body['address_uri'] = validate_fields('address_uri', address_uri, Optional[str])

        if skip_confirmation is not None:
            self.body["skip_confirmation"] = validate_fields('skip_confirmation', skip_confirmation, bool)
            self.body['skip_confirmation'] = validate_fields('skip_confirmation', skip_confirmation, Optional[bool])

        if type is not None:
            self.body["type"] = validate_fields('type', type, str)
            self.body['type'] = validate_fields('type', type, str)
        if type is None:
            raise InputParamError("<type> (=>type) of <CargoPointMP> is a required parameter")

        if type not in ['source', 'destination', 'return']:
            raise InputParamError("<type> of <CargoPointMP> should be in <source, destination, return>")

        if payment_on_delivery_client_order_id is not None:
            self.body["payment_on_delivery"]["client_order_id"] = validate_fields('payment_on_delivery_client_order_id', payment_on_delivery_client_order_id, str)
            self.body['payment_on_delivery_client_order_id'] = validate_fields('payment_on_delivery_client_order_id', payment_on_delivery_client_order_id, str)
        if payment_on_delivery_client_order_id is None:
            raise InputParamError("<payment_on_delivery_client_order_id> (payment_on_delivery=>client_order_id) of <CargoPointMP> is a required parameter")

        if payment_on_delivery_cost is not None:
            self.body["payment_on_delivery"]["cost"] = validate_fields('payment_on_delivery_cost', payment_on_delivery_cost, str)
            self.body['payment_on_delivery_cost'] = validate_fields('payment_on_delivery_cost', payment_on_delivery_cost, Optional[str])
        if payment_on_delivery_cost is None:
            raise InputParamError("<payment_on_delivery_cost> (payment_on_delivery=>cost) of <CargoPointMP> is a required parameter")

        if payment_on_delivery_customer_full_name is not None:
            self.body["payment_on_delivery"]["customer"]["full_name"] = validate_fields('payment_on_delivery_customer_full_name', payment_on_delivery_customer_full_name, str)
            self.body['payment_on_delivery_customer_full_name'] = validate_fields('payment_on_delivery_customer_full_name', payment_on_delivery_customer_full_name, Optional[str])

        if payment_on_delivery_customer_inn is not None:
            self.body["payment_on_delivery"]["customer"]["inn"] = validate_fields('payment_on_delivery_customer_inn', payment_on_delivery_customer_inn, str)
            self.body['payment_on_delivery_customer_inn'] = validate_fields('payment_on_delivery_customer_inn', payment_on_delivery_customer_inn, Optional[str])

        if payment_on_delivery_customer_email is not None:
            self.body["payment_on_delivery"]["customer"]["email"] = validate_fields('payment_on_delivery_customer_email', payment_on_delivery_customer_email, str)
            self.body['payment_on_delivery_customer_email'] = validate_fields('payment_on_delivery_customer_email', payment_on_delivery_customer_email, Optional[str])

        if payment_on_delivery_customer_phone is not None:
            self.body["payment_on_delivery"]["customer"]["phone"] = validate_fields('payment_on_delivery_customer_phone', payment_on_delivery_customer_phone, str)
            self.body['payment_on_delivery_customer_phone'] = validate_fields('payment_on_delivery_customer_phone', payment_on_delivery_customer_phone, Optional[str])

        if payment_on_delivery_tax_system_code is not None:
            self.body["payment_on_delivery"]["tax_system_code"] = validate_fields('payment_on_delivery_tax_system_code', payment_on_delivery_tax_system_code, int)
            self.body['payment_on_delivery_tax_system_code'] = validate_fields('payment_on_delivery_tax_system_code', payment_on_delivery_tax_system_code, Optional[int])
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code < 1:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <CargoPointMP> should be more than 1")
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code > 6:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <CargoPointMP> should be less than 6")

        if payment_on_delivery_currency is not None:
            self.body["payment_on_delivery"]["currency"] = validate_fields('payment_on_delivery_currency', payment_on_delivery_currency, str)
            self.body['payment_on_delivery_currency'] = validate_fields('payment_on_delivery_currency', payment_on_delivery_currency, Optional[str])
        if payment_on_delivery_currency and len(payment_on_delivery_currency) < 3:
            raise InputParamError("<payment_on_delivery_currency> of <CargoPointMP> should contain at least 3 element")
        if payment_on_delivery_currency and len(payment_on_delivery_currency) > 3:
            raise InputParamError("<payment_on_delivery_currency> of <CargoPointMP> should not contain more than 3 element")

        if external_order_id is not None:
            self.body["external_order_id"] = validate_fields('external_order_id', external_order_id, str)
            self.body['external_order_id'] = validate_fields('external_order_id', external_order_id, Optional[str])

        if pickup_code is not None:
            self.body["pickup_code"] = validate_fields('pickup_code', pickup_code, str)
            self.body['pickup_code'] = validate_fields('pickup_code', pickup_code, Optional[str])

    def __repr__(self):
        return "<CargoPointMP>"

    @property
    def point_id(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("point_id")

    @property
    def visit_order(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("visit_order")

    @property
    def contact_name(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("contact_name")

    @property
    def contact_phone(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("contact_phone")

    @property
    def contact_email(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("contact_email")

    @property
    def address_fullname(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("address_fullname")

    @property
    def address_shortname(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_shortname")

    @property
    def address_coordinates(self) -> List['int']:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: List['int']
        """
        return [item for item in self.body.get("address_coordinates")]

    @property
    def address_country(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_country")

    @property
    def address_city(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_city")

    @property
    def address_street(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_street")

    @property
    def address_building(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_building")

    @property
    def address_porch(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_porch")

    @property
    def address_floor(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("address_floor")

    @property
    def address_flat(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("address_flat")

    @property
    def address_sfloor(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_sfloor")

    @property
    def address_sflat(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_sflat")

    @property
    def address_door_code(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_door_code")

    @property
    def address_comment(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_comment")

    @property
    def address_uri(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_uri")

    @property
    def skip_confirmation(self) -> Optional[bool]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[bool]
        """
        return self.body.get("skip_confirmation")

    @property
    def type(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("type")

    @property
    def payment_on_delivery_client_order_id(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("payment_on_delivery_client_order_id")

    @property
    def payment_on_delivery_cost(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_cost")

    @property
    def payment_on_delivery_customer_full_name(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_full_name")

    @property
    def payment_on_delivery_customer_inn(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_inn")

    @property
    def payment_on_delivery_customer_email(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_email")

    @property
    def payment_on_delivery_customer_phone(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_phone")

    @property
    def payment_on_delivery_tax_system_code(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("payment_on_delivery_tax_system_code")

    @property
    def payment_on_delivery_currency(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_currency")

    @property
    def external_order_id(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("external_order_id")

    @property
    def pickup_code(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("pickup_code")


class ResponseCargoPointMP(YCBase):
    """
        ???
        Описание точки в заявке с мультиточками

            :param int id: Целочисленный идентификатор точки *(Обязательный параметр)* (1)
            :param str contact_name: Имя контактного лица *(Обязательный параметр)* (Морти)
            :param str contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999998)
            :param Optional[str] contact_email: Email — обязательный параметр для точек source и return (morty@yandex.ru)
            :param str address_fullname: Полное название с указанием города (Москва, Садовническая набережная, 82с2, БЦ Аврора) *(Обязательный параметр)* (Санкт-Петербург Большая Монетная улица 1к1А)
            :param Optional[str] address_shortname: Адрес в пределах города, как показывается на Таксометре (Садовническая набережная, 82с2, БЦ Аврора) (Большая Монетная улица, 1к1А)
            :param List['int'] address_coordinates: Массив из двух вещественных чисел [долгота, широта]. Порядок важен! *(Обязательный параметр)*
            :param Optional[str] address_country: Страна (Российская Федерация)
            :param Optional[str] address_city: Город (Санкт-Петербург)
            :param Optional[str] address_street: Улица (Большая Монетная улица)
            :param Optional[str] address_building: Строение (23к1А)
            :param Optional[str] address_porch: Подъезд (может быть A) (A)
            :param Optional[int] address_floor: Этаж (DEPRECATED) (1)
            :param Optional[int] address_flat: Квартира (DEPRECATED) (1)
            :param Optional[str] address_sfloor: Этаж (1)
            :param Optional[str] address_sflat: Квартира (1)
            :param Optional[str] address_door_code: Код домофона (169)
            :param Optional[str] address_comment: Комментарий для доставщика (Домофон не работает)
            :param Optional[str] address_uri: Карточный uri геообъекта (ymapsbm1://geo?ll=38.805%2C55.084)
            :param str type: Тип точки *(Обязательный параметр)* (source)

                * **source** - ???
                * **destination** - ???
                * **return** - ???

            :param int visit_order: Порядок посещения точки *(Обязательный параметр)* (1)
            :param str visit_status: Статус посещения данной точки pending - точка еще не посещена arrived - водитель прибыл на точку visited - водитель передал/забрал груз на точке skipped - точка пропущена (в случае возврата, когда клиент не смог принять груз) *(Обязательный параметр)* (pending)

                * **pending** - ???
                * **arrived** - ???
                * **visited** - ???
                * **skipped** - ???

            :param Optional[bool] skip_confirmation: Пропускать подтверждение через SMS в данной точке
            :param str payment_on_delivery_client_order_id: id заказа *(Обязательный параметр)* (100)
            :param bool payment_on_delivery_is_paid: Оплачен ли заказ *(Обязательный параметр)*
            :param str payment_on_delivery_cost: Decimal(19, 4) *(Обязательный параметр)* (12.50)
            :param Optional[str] payment_on_delivery_customer_full_name: Для юридического лица — название организации, для ИП и физического лица — ФИО (Morty)
            :param Optional[str] payment_on_delivery_customer_inn: ИНН пользователя (10 или 12 цифр) (3664069397)
            :param Optional[str] payment_on_delivery_customer_email: Электронная почта пользователя. Если не указано, будет использована почта получателя из точки (morty@yandex.ru)
            :param Optional[str] payment_on_delivery_customer_phone: Телефон пользователя. Если не указано, будет использован телефон получателя из точки (79000000000)
            :param Optional[int] payment_on_delivery_tax_system_code: Система налогообложения магазина (1)
            :param Optional[str] external_order_id: Номер заказа клиента (100)
            :param Optional[str] pickup_code: Код выдачи товара (ПВЗ) (2397)
    """

    def __init__(self,
                 id: int = None,
                 contact_name: str = None,
                 contact_phone: str = None,
                 contact_email: Optional[str] = None,
                 address_fullname: str = None,
                 address_shortname: Optional[str] = None,
                 address_coordinates: List['int'] = None,
                 address_country: Optional[str] = None,
                 address_city: Optional[str] = None,
                 address_street: Optional[str] = None,
                 address_building: Optional[str] = None,
                 address_porch: Optional[str] = None,
                 address_floor: Optional[int] = None,
                 address_flat: Optional[int] = None,
                 address_sfloor: Optional[str] = None,
                 address_sflat: Optional[str] = None,
                 address_door_code: Optional[str] = None,
                 address_comment: Optional[str] = None,
                 address_uri: Optional[str] = None,
                 type: str = None,
                 visit_order: int = None,
                 visit_status: str = None,
                 skip_confirmation: Optional[bool] = None,
                 payment_on_delivery_client_order_id: str = None,
                 payment_on_delivery_is_paid: bool = None,
                 payment_on_delivery_cost: str = None,
                 payment_on_delivery_customer_full_name: Optional[str] = None,
                 payment_on_delivery_customer_inn: Optional[str] = None,
                 payment_on_delivery_customer_email: Optional[str] = None,
                 payment_on_delivery_customer_phone: Optional[str] = None,
                 payment_on_delivery_tax_system_code: Optional[int] = None,
                 external_order_id: Optional[str] = None,
                 pickup_code: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if id is not None:
            self.body["id"] = validate_fields('id', id, int)
            self.body['id'] = validate_fields('id', id, int)
        if id is None:
            raise InputParamError("<id> (=>id) of <ResponseCargoPointMP> is a required parameter")

        if contact_name is not None:
            self.body["contact"]["name"] = validate_fields('contact_name', contact_name, str)
            self.body['contact_name'] = validate_fields('contact_name', contact_name, str)
        if contact_name is None:
            raise InputParamError("<contact_name> (contact=>name) of <ResponseCargoPointMP> is a required parameter")

        if contact_phone is not None:
            self.body["contact"]["phone"] = validate_fields('contact_phone', contact_phone, str)
            self.body['contact_phone'] = validate_fields('contact_phone', contact_phone, str)
        if contact_phone is None:
            raise InputParamError("<contact_phone> (contact=>phone) of <ResponseCargoPointMP> is a required parameter")

        if contact_email is not None:
            self.body["contact"]["email"] = validate_fields('contact_email', contact_email, str)
            self.body['contact_email'] = validate_fields('contact_email', contact_email, Optional[str])

        if address_fullname is not None:
            self.body["address"]["fullname"] = validate_fields('address_fullname', address_fullname, str)
            self.body['address_fullname'] = validate_fields('address_fullname', address_fullname, str)
        if address_fullname is None:
            raise InputParamError("<address_fullname> (address=>fullname) of <ResponseCargoPointMP> is a required parameter")

        if address_shortname is not None:
            self.body["address"]["shortname"] = validate_fields('address_shortname', address_shortname, str)
            self.body['address_shortname'] = validate_fields('address_shortname', address_shortname, Optional[str])

        if address_coordinates is not None:
            self.body["address"]["coordinates"] = validate_fields('address_coordinates', address_coordinates, List['int'])
            self.body['address_coordinates'] = validate_fields('address_coordinates', address_coordinates, List['int'])
        if address_coordinates and len(address_coordinates) < 2:
            raise InputParamError("<address_coordinates> of <ResponseCargoPointMP> should contain at least 2 element")
        if address_coordinates and len(address_coordinates) > 2:
            raise InputParamError("<address_coordinates> of <ResponseCargoPointMP> should not contain more than 2 element")
        if address_coordinates is None:
            raise InputParamError("<address_coordinates> (address=>coordinates) of <ResponseCargoPointMP> is a required parameter")

        if address_country is not None:
            self.body["address"]["country"] = validate_fields('address_country', address_country, str)
            self.body['address_country'] = validate_fields('address_country', address_country, Optional[str])

        if address_city is not None:
            self.body["address"]["city"] = validate_fields('address_city', address_city, str)
            self.body['address_city'] = validate_fields('address_city', address_city, Optional[str])

        if address_street is not None:
            self.body["address"]["street"] = validate_fields('address_street', address_street, str)
            self.body['address_street'] = validate_fields('address_street', address_street, Optional[str])

        if address_building is not None:
            self.body["address"]["building"] = validate_fields('address_building', address_building, str)
            self.body['address_building'] = validate_fields('address_building', address_building, Optional[str])

        if address_porch is not None:
            self.body["address"]["porch"] = validate_fields('address_porch', address_porch, str)
            self.body['address_porch'] = validate_fields('address_porch', address_porch, Optional[str])

        if address_floor is not None:
            self.body["address"]["floor"] = validate_fields('address_floor', address_floor, int)
            self.body['address_floor'] = validate_fields('address_floor', address_floor, Optional[int])

        if address_flat is not None:
            self.body["address"]["flat"] = validate_fields('address_flat', address_flat, int)
            self.body['address_flat'] = validate_fields('address_flat', address_flat, Optional[int])

        if address_sfloor is not None:
            self.body["address"]["sfloor"] = validate_fields('address_sfloor', address_sfloor, str)
            self.body['address_sfloor'] = validate_fields('address_sfloor', address_sfloor, Optional[str])

        if address_sflat is not None:
            self.body["address"]["sflat"] = validate_fields('address_sflat', address_sflat, str)
            self.body['address_sflat'] = validate_fields('address_sflat', address_sflat, Optional[str])

        if address_door_code is not None:
            self.body["address"]["door_code"] = validate_fields('address_door_code', address_door_code, str)
            self.body['address_door_code'] = validate_fields('address_door_code', address_door_code, Optional[str])

        if address_comment is not None:
            self.body["address"]["comment"] = validate_fields('address_comment', address_comment, str)
            self.body['address_comment'] = validate_fields('address_comment', address_comment, Optional[str])

        if address_uri is not None:
            self.body["address"]["uri"] = validate_fields('address_uri', address_uri, str)
            self.body['address_uri'] = validate_fields('address_uri', address_uri, Optional[str])

        if type is not None:
            self.body["type"] = validate_fields('type', type, str)
            self.body['type'] = validate_fields('type', type, str)
        if type is None:
            raise InputParamError("<type> (=>type) of <ResponseCargoPointMP> is a required parameter")

        if type not in ['source', 'destination', 'return']:
            raise InputParamError("<type> of <ResponseCargoPointMP> should be in <source, destination, return>")

        if visit_order is not None:
            self.body["visit_order"] = validate_fields('visit_order', visit_order, int)
            self.body['visit_order'] = validate_fields('visit_order', visit_order, int)
        if visit_order is None:
            raise InputParamError("<visit_order> (=>visit_order) of <ResponseCargoPointMP> is a required parameter")

        if visit_status is not None:
            self.body["visit_status"] = validate_fields('visit_status', visit_status, str)
            self.body['visit_status'] = validate_fields('visit_status', visit_status, str)
        if visit_status is None:
            raise InputParamError("<visit_status> (=>visit_status) of <ResponseCargoPointMP> is a required parameter")

        if visit_status not in ['pending', 'arrived', 'visited', 'skipped']:
            raise InputParamError("<visit_status> of <ResponseCargoPointMP> should be in <pending, arrived, visited, skipped>")

        if skip_confirmation is not None:
            self.body["skip_confirmation"] = validate_fields('skip_confirmation', skip_confirmation, bool)
            self.body['skip_confirmation'] = validate_fields('skip_confirmation', skip_confirmation, Optional[bool])

        if payment_on_delivery_client_order_id is not None:
            self.body["payment_on_delivery"]["client_order_id"] = validate_fields('payment_on_delivery_client_order_id', payment_on_delivery_client_order_id, str)
            self.body['payment_on_delivery_client_order_id'] = validate_fields('payment_on_delivery_client_order_id', payment_on_delivery_client_order_id, str)
        if payment_on_delivery_client_order_id is None:
            raise InputParamError("<payment_on_delivery_client_order_id> (payment_on_delivery=>client_order_id) of <ResponseCargoPointMP> is a required parameter")

        if payment_on_delivery_is_paid is not None:
            self.body["payment_on_delivery"]["is_paid"] = validate_fields('payment_on_delivery_is_paid', payment_on_delivery_is_paid, bool)
            self.body['payment_on_delivery_is_paid'] = validate_fields('payment_on_delivery_is_paid', payment_on_delivery_is_paid, bool)
        if payment_on_delivery_is_paid is None:
            raise InputParamError("<payment_on_delivery_is_paid> (payment_on_delivery=>is_paid) of <ResponseCargoPointMP> is a required parameter")

        if payment_on_delivery_cost is not None:
            self.body["payment_on_delivery"]["cost"] = validate_fields('payment_on_delivery_cost', payment_on_delivery_cost, str)
            self.body['payment_on_delivery_cost'] = validate_fields('payment_on_delivery_cost', payment_on_delivery_cost, str)
        if payment_on_delivery_cost is None:
            raise InputParamError("<payment_on_delivery_cost> (payment_on_delivery=>cost) of <ResponseCargoPointMP> is a required parameter")

        if payment_on_delivery_customer_full_name is not None:
            self.body["payment_on_delivery"]["customer"]["full_name"] = validate_fields('payment_on_delivery_customer_full_name', payment_on_delivery_customer_full_name, str)
            self.body['payment_on_delivery_customer_full_name'] = validate_fields('payment_on_delivery_customer_full_name', payment_on_delivery_customer_full_name, Optional[str])

        if payment_on_delivery_customer_inn is not None:
            self.body["payment_on_delivery"]["customer"]["inn"] = validate_fields('payment_on_delivery_customer_inn', payment_on_delivery_customer_inn, str)
            self.body['payment_on_delivery_customer_inn'] = validate_fields('payment_on_delivery_customer_inn', payment_on_delivery_customer_inn, Optional[str])

        if payment_on_delivery_customer_email is not None:
            self.body["payment_on_delivery"]["customer"]["email"] = validate_fields('payment_on_delivery_customer_email', payment_on_delivery_customer_email, str)
            self.body['payment_on_delivery_customer_email'] = validate_fields('payment_on_delivery_customer_email', payment_on_delivery_customer_email, Optional[str])

        if payment_on_delivery_customer_phone is not None:
            self.body["payment_on_delivery"]["customer"]["phone"] = validate_fields('payment_on_delivery_customer_phone', payment_on_delivery_customer_phone, str)
            self.body['payment_on_delivery_customer_phone'] = validate_fields('payment_on_delivery_customer_phone', payment_on_delivery_customer_phone, Optional[str])

        if payment_on_delivery_tax_system_code is not None:
            self.body["payment_on_delivery"]["tax_system_code"] = validate_fields('payment_on_delivery_tax_system_code', payment_on_delivery_tax_system_code, int)
            self.body['payment_on_delivery_tax_system_code'] = validate_fields('payment_on_delivery_tax_system_code', payment_on_delivery_tax_system_code, Optional[int])
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code < 1:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <ResponseCargoPointMP> should be more than 1")
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code > 6:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <ResponseCargoPointMP> should be less than 6")

        if external_order_id is not None:
            self.body["external_order_id"] = validate_fields('external_order_id', external_order_id, str)
            self.body['external_order_id'] = validate_fields('external_order_id', external_order_id, Optional[str])

        if pickup_code is not None:
            self.body["pickup_code"] = validate_fields('pickup_code', pickup_code, str)
            self.body['pickup_code'] = validate_fields('pickup_code', pickup_code, Optional[str])

    def __repr__(self):
        return "<ResponseCargoPointMP>"

    @property
    def id(self) -> int:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: int
        """
        return self.body.get("id")

    @property
    def contact_name(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("contact_name")

    @property
    def contact_phone(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("contact_phone")

    @property
    def contact_email(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("contact_email")

    @property
    def address_fullname(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("address_fullname")

    @property
    def address_shortname(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_shortname")

    @property
    def address_coordinates(self) -> List['int']:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: List['int']
        """
        return [item for item in self.body.get("address_coordinates")]

    @property
    def address_country(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_country")

    @property
    def address_city(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_city")

    @property
    def address_street(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_street")

    @property
    def address_building(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_building")

    @property
    def address_porch(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_porch")

    @property
    def address_floor(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("address_floor")

    @property
    def address_flat(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("address_flat")

    @property
    def address_sfloor(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_sfloor")

    @property
    def address_sflat(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_sflat")

    @property
    def address_door_code(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_door_code")

    @property
    def address_comment(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_comment")

    @property
    def address_uri(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("address_uri")

    @property
    def type(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("type")

    @property
    def visit_order(self) -> int:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: int
        """
        return self.body.get("visit_order")

    @property
    def visit_status(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("visit_status")

    @property
    def skip_confirmation(self) -> Optional[bool]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[bool]
        """
        return self.body.get("skip_confirmation")

    @property
    def payment_on_delivery_client_order_id(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("payment_on_delivery_client_order_id")

    @property
    def payment_on_delivery_is_paid(self) -> bool:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: bool
        """
        return self.body.get("payment_on_delivery_is_paid")

    @property
    def payment_on_delivery_cost(self) -> str:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: str
        """
        return self.body.get("payment_on_delivery_cost")

    @property
    def payment_on_delivery_customer_full_name(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_full_name")

    @property
    def payment_on_delivery_customer_inn(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_inn")

    @property
    def payment_on_delivery_customer_email(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_email")

    @property
    def payment_on_delivery_customer_phone(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_phone")

    @property
    def payment_on_delivery_tax_system_code(self) -> Optional[int]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[int]
        """
        return self.body.get("payment_on_delivery_tax_system_code")

    @property
    def external_order_id(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("external_order_id")

    @property
    def pickup_code(self) -> Optional[str]:
        """

        :return: Описание точки в заявке с мультиточками
        :rtype: Optional[str]
        """
        return self.body.get("pickup_code")


class ClaimWarning(YCBase):
    """
        ???
        ???

            :param str source: Источник предупреждения (ex. client_requirements) *(Обязательный параметр)* (client_requirements)

                * **client_requirements** - ???
                * **taxi_requirements** - ???

            :param str code: Тип предупреждения (ex. not_fit_in_car) *(Обязательный параметр)* (not_fit_in_car)

                * **not_fit_in_car** - ???
                * **requirement_unavailable** - ???

            :param Optional[str] message: Локализованная информация с причиной предупреждения (Предупреждение)
    """

    def __init__(self,
                 source: str = None,
                 code: str = None,
                 message: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if source is not None:
            self.body["source"] = validate_fields('source', source, str)
            self.body['source'] = validate_fields('source', source, str)
        if source is None:
            raise InputParamError("<source> (=>source) of <ClaimWarning> is a required parameter")

        if source not in ['client_requirements', 'taxi_requirements']:
            raise InputParamError("<source> of <ClaimWarning> should be in <client_requirements, taxi_requirements>")

        if code is not None:
            self.body["code"] = validate_fields('code', code, str)
            self.body['code'] = validate_fields('code', code, str)
        if code is None:
            raise InputParamError("<code> (=>code) of <ClaimWarning> is a required parameter")

        if code not in ['not_fit_in_car', 'requirement_unavailable']:
            raise InputParamError("<code> of <ClaimWarning> should be in <not_fit_in_car, requirement_unavailable>")

        if message is not None:
            self.body["message"] = validate_fields('message', message, str)
            self.body['message'] = validate_fields('message', message, Optional[str])

    def __repr__(self):
        return "<ClaimWarning>"

    @property
    def source(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("source")

    @property
    def code(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("code")

    @property
    def message(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("message")


class CargoItemMP(YCBase):
    """
        ???
        ???

            :param Optional[str] extra_id: Краткий уникальный идентификатор item'а (в рамках заявки) (БП-208)
            :param int pickup_point: id точки, откуда нужно забрать товар (отличается от id в заявке) *(Обязательный параметр)* (1)
            :param int droppof_point: id точки, куда нужно доставить товар (отличается от id в заявке) *(Обязательный параметр)* (2)
            :param str title: Наименование единицы товара *(Обязательный параметр)* (Плюмбус)
            :param int size_length: Размер в метрах *(Обязательный параметр)* (0.1)
            :param int size_width: Размер в метрах *(Обязательный параметр)* (0.1)
            :param int size_height: Размер в метрах *(Обязательный параметр)* (0.1)
            :param Optional[int] weight: Вес единицы товара в кг. (2.0)
            :param str cost_value: Цена за штуку в валюте cost_currency *(Обязательный параметр)* (2.00)
            :param str cost_currency: Валюта цены за штуку в формате ISO 4217 (используется в оплате при получении товара) *(Обязательный параметр)* (RUB)
            :param int quantity: Количество указанного товара *(Обязательный параметр)* (1)
            :param int fiscalization_vat_code: Ставка НДС *(Обязательный параметр)* (1)
            :param str fiscalization_payment_subject: Признак предмета расчета *(Обязательный параметр)* (commodity)
            :param str fiscalization_payment_mode: Признак способа расчета *(Обязательный параметр)* (full_payment)
            :param Optional[str] fiscalization_product_code: Код товара
            :param Optional[str] fiscalization_country_of_origin_code: Код страны происхождения товара (RU)
            :param Optional[str] fiscalization_customs_declaration_number: Номер таможенной декларации (10702030/260917/0080123)
            :param str fiscalization_excise: Decimal(19, 4) (12.50)
    """

    def __init__(self,
                 extra_id: Optional[str] = None,
                 pickup_point: int = None,
                 droppof_point: int = None,
                 title: str = None,
                 size_length: int = None,
                 size_width: int = None,
                 size_height: int = None,
                 weight: Optional[int] = None,
                 cost_value: str = None,
                 cost_currency: str = None,
                 quantity: int = None,
                 fiscalization_vat_code: int = None,
                 fiscalization_payment_subject: str = None,
                 fiscalization_payment_mode: str = None,
                 fiscalization_product_code: Optional[str] = None,
                 fiscalization_country_of_origin_code: Optional[str] = None,
                 fiscalization_customs_declaration_number: Optional[str] = None,
                 fiscalization_excise: str = None,
                 ):
        self.body = collections.defaultdict(dict)

        if extra_id is not None:
            self.body["extra_id"] = validate_fields('extra_id', extra_id, str)
            self.body['extra_id'] = validate_fields('extra_id', extra_id, Optional[str])

        if pickup_point is not None:
            self.body["pickup_point"] = validate_fields('pickup_point', pickup_point, int)
            self.body['pickup_point'] = validate_fields('pickup_point', pickup_point, int)
        if pickup_point is None:
            raise InputParamError("<pickup_point> (=>pickup_point) of <CargoItemMP> is a required parameter")

        if droppof_point is not None:
            self.body["droppof_point"] = validate_fields('droppof_point', droppof_point, int)
            self.body['droppof_point'] = validate_fields('droppof_point', droppof_point, int)
        if droppof_point is None:
            raise InputParamError("<droppof_point> (=>droppof_point) of <CargoItemMP> is a required parameter")

        if title is not None:
            self.body["title"] = validate_fields('title', title, str)
            self.body['title'] = validate_fields('title', title, str)
        if title is None:
            raise InputParamError("<title> (=>title) of <CargoItemMP> is a required parameter")

        if size_length is not None:
            self.body["size"]["length"] = validate_fields('size_length', size_length, int)
            self.body['size_length'] = validate_fields('size_length', size_length, int)
        if size_length is None:
            raise InputParamError("<size_length> (size=>length) of <CargoItemMP> is a required parameter")

        if size_width is not None:
            self.body["size"]["width"] = validate_fields('size_width', size_width, int)
            self.body['size_width'] = validate_fields('size_width', size_width, int)
        if size_width is None:
            raise InputParamError("<size_width> (size=>width) of <CargoItemMP> is a required parameter")

        if size_height is not None:
            self.body["size"]["height"] = validate_fields('size_height', size_height, int)
            self.body['size_height'] = validate_fields('size_height', size_height, int)
        if size_height is None:
            raise InputParamError("<size_height> (size=>height) of <CargoItemMP> is a required parameter")

        if weight is not None:
            self.body["weight"] = validate_fields('weight', weight, int)
            self.body['weight'] = validate_fields('weight', weight, Optional[int])

        if cost_value is not None:
            self.body["cost_value"] = validate_fields('cost_value', cost_value, str)
            self.body['cost_value'] = validate_fields('cost_value', cost_value, str)
        if cost_value is None:
            raise InputParamError("<cost_value> (=>cost_value) of <CargoItemMP> is a required parameter")

        if cost_currency is not None:
            self.body["cost_currency"] = validate_fields('cost_currency', cost_currency, str)
            self.body['cost_currency'] = validate_fields('cost_currency', cost_currency, str)
        if cost_currency and len(cost_currency) < 3:
            raise InputParamError("<cost_currency> of <CargoItemMP> should contain at least 3 element")
        if cost_currency and len(cost_currency) > 3:
            raise InputParamError("<cost_currency> of <CargoItemMP> should not contain more than 3 element")
        if cost_currency is None:
            raise InputParamError("<cost_currency> (=>cost_currency) of <CargoItemMP> is a required parameter")

        if quantity is not None:
            self.body["quantity"] = validate_fields('quantity', quantity, int)
            self.body['quantity'] = validate_fields('quantity', quantity, int)
        if quantity and quantity < 1:
            raise InputParamError("<quantity> of <CargoItemMP> should be more than 1")
        if quantity is None:
            raise InputParamError("<quantity> (=>quantity) of <CargoItemMP> is a required parameter")

        if fiscalization_vat_code is not None:
            self.body["fiscalization"]["vat_code"] = validate_fields('fiscalization_vat_code', fiscalization_vat_code, int)
            self.body['fiscalization_vat_code'] = validate_fields('fiscalization_vat_code', fiscalization_vat_code, int)
        if fiscalization_vat_code and fiscalization_vat_code < 1:
            raise InputParamError("<fiscalization_vat_code> of <CargoItemMP> should be more than 1")
        if fiscalization_vat_code and fiscalization_vat_code > 6:
            raise InputParamError("<fiscalization_vat_code> of <CargoItemMP> should be less than 6")
        if fiscalization_vat_code is None:
            raise InputParamError("<fiscalization_vat_code> (fiscalization=>vat_code) of <CargoItemMP> is a required parameter")

        if fiscalization_payment_subject is not None:
            self.body["fiscalization"]["payment_subject"] = validate_fields('fiscalization_payment_subject', fiscalization_payment_subject, str)
            self.body['fiscalization_payment_subject'] = validate_fields('fiscalization_payment_subject', fiscalization_payment_subject, str)
        if fiscalization_payment_subject is None:
            raise InputParamError("<fiscalization_payment_subject> (fiscalization=>payment_subject) of <CargoItemMP> is a required parameter")

        if fiscalization_payment_mode is not None:
            self.body["fiscalization"]["payment_mode"] = validate_fields('fiscalization_payment_mode', fiscalization_payment_mode, str)
            self.body['fiscalization_payment_mode'] = validate_fields('fiscalization_payment_mode', fiscalization_payment_mode, str)
        if fiscalization_payment_mode is None:
            raise InputParamError("<fiscalization_payment_mode> (fiscalization=>payment_mode) of <CargoItemMP> is a required parameter")

        if fiscalization_product_code is not None:
            self.body["fiscalization"]["product_code"] = validate_fields('fiscalization_product_code', fiscalization_product_code, str)
            self.body['fiscalization_product_code'] = validate_fields('fiscalization_product_code', fiscalization_product_code, Optional[str])

        if fiscalization_country_of_origin_code is not None:
            self.body["fiscalization"]["country_of_origin_code"] = validate_fields('fiscalization_country_of_origin_code', fiscalization_country_of_origin_code, str)
            self.body['fiscalization_country_of_origin_code'] = validate_fields('fiscalization_country_of_origin_code', fiscalization_country_of_origin_code, Optional[str])

        if fiscalization_customs_declaration_number is not None:
            self.body["fiscalization"]["customs_declaration_number"] = validate_fields('fiscalization_customs_declaration_number', fiscalization_customs_declaration_number, str)
            self.body['fiscalization_customs_declaration_number'] = validate_fields('fiscalization_customs_declaration_number', fiscalization_customs_declaration_number, Optional[str])
        if fiscalization_customs_declaration_number and len(fiscalization_customs_declaration_number) < 1:
            raise InputParamError("<fiscalization_customs_declaration_number> of <CargoItemMP> should contain at least 1 element")
        if fiscalization_customs_declaration_number and len(fiscalization_customs_declaration_number) > 32:
            raise InputParamError("<fiscalization_customs_declaration_number> of <CargoItemMP> should not contain more than 32 element")

        if fiscalization_excise is not None:
            self.body["fiscalization"]["excise"] = validate_fields('fiscalization_excise', fiscalization_excise, str)
            self.body['fiscalization_excise'] = validate_fields('fiscalization_excise', fiscalization_excise, str)

    def __repr__(self):
        return "<CargoItemMP>"

    @property
    def extra_id(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("extra_id")

    @property
    def pickup_point(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("pickup_point")

    @property
    def droppof_point(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("droppof_point")

    @property
    def title(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("title")

    @property
    def size_length(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("size_length")

    @property
    def size_width(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("size_width")

    @property
    def size_height(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("size_height")

    @property
    def weight(self) -> Optional[int]:
        """

        :return: ???
        :rtype: Optional[int]
        """
        return self.body.get("weight")

    @property
    def cost_value(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("cost_value")

    @property
    def cost_currency(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("cost_currency")

    @property
    def quantity(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("quantity")

    @property
    def fiscalization_vat_code(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("fiscalization_vat_code")

    @property
    def fiscalization_payment_subject(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("fiscalization_payment_subject")

    @property
    def fiscalization_payment_mode(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("fiscalization_payment_mode")

    @property
    def fiscalization_product_code(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("fiscalization_product_code")

    @property
    def fiscalization_country_of_origin_code(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("fiscalization_country_of_origin_code")

    @property
    def fiscalization_customs_declaration_number(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("fiscalization_customs_declaration_number")

    @property
    def fiscalization_excise(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("fiscalization_excise")


class MatchedCar(YCBase):
    """
        ???
        Информация о подобранной машине

            :param str taxi_class: Класс такси. Возможные значения express, cargo *(Обязательный параметр)* (express)
            :param Optional[str] client_taxi_class: Подмененный тариф (e.g., cargo, хотя в cars cargocorp) (cargo)
            :param Optional[str] cargo_type: Тип грузовика (lcv_m)
            :param Optional[int] cargo_type_int: Тип грузовика (2 is equal to "lcv_m")
            :param Optional[int] cargo_loaders: Требуемое число грузчиков
            :param Optional[bool] door_to_door: Опция "от двери до двери" для тарифа "доставка"
            :param Optional[List['int']] cargo_points: Значение cargo_points_field, фейковое требование длятарифа
            :param Optional[str] cargo_points_field: Название требования для мультиточек (fake_middle_point_cargo)
    """

    def __init__(self,
                 taxi_class: str = None,
                 client_taxi_class: Optional[str] = None,
                 cargo_type: Optional[str] = None,
                 cargo_type_int: Optional[int] = None,
                 cargo_loaders: Optional[int] = None,
                 door_to_door: Optional[bool] = None,
                 cargo_points: Optional[List['int']] = None,
                 cargo_points_field: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if taxi_class is not None:
            self.body["taxi_class"] = validate_fields('taxi_class', taxi_class, str)
            self.body['taxi_class'] = validate_fields('taxi_class', taxi_class, str)
        if taxi_class is None:
            raise InputParamError("<taxi_class> (=>taxi_class) of <MatchedCar> is a required parameter")

        if client_taxi_class is not None:
            self.body["client_taxi_class"] = validate_fields('client_taxi_class', client_taxi_class, str)
            self.body['client_taxi_class'] = validate_fields('client_taxi_class', client_taxi_class, Optional[str])

        if cargo_type is not None:
            self.body["cargo_type"] = validate_fields('cargo_type', cargo_type, str)
            self.body['cargo_type'] = validate_fields('cargo_type', cargo_type, Optional[str])

        if cargo_type_int is not None:
            self.body["cargo_type_int"] = validate_fields('cargo_type_int', cargo_type_int, int)
            self.body['cargo_type_int'] = validate_fields('cargo_type_int', cargo_type_int, Optional[int])

        if cargo_loaders is not None:
            self.body["cargo_loaders"] = validate_fields('cargo_loaders', cargo_loaders, int)
            self.body['cargo_loaders'] = validate_fields('cargo_loaders', cargo_loaders, Optional[int])
        if cargo_loaders and cargo_loaders < 0:
            raise InputParamError("<cargo_loaders> of <MatchedCar> should be more than 0")

        if door_to_door is not None:
            self.body["door_to_door"] = validate_fields('door_to_door', door_to_door, bool)
            self.body['door_to_door'] = validate_fields('door_to_door', door_to_door, Optional[bool])

        if cargo_points is not None:
            self.body["cargo_points"] = validate_fields('cargo_points', cargo_points, List['int'])
            self.body['cargo_points'] = validate_fields('cargo_points', cargo_points, Optional[List['int']])

        if cargo_points_field is not None:
            self.body["cargo_points_field"] = validate_fields('cargo_points_field', cargo_points_field, str)
            self.body['cargo_points_field'] = validate_fields('cargo_points_field', cargo_points_field, Optional[str])

    def __repr__(self):
        return "<MatchedCar>"

    @property
    def taxi_class(self) -> str:
        """

        :return: Информация о подобранной машине
        :rtype: str
        """
        return self.body.get("taxi_class")

    @property
    def client_taxi_class(self) -> Optional[str]:
        """

        :return: Информация о подобранной машине
        :rtype: Optional[str]
        """
        return self.body.get("client_taxi_class")

    @property
    def cargo_type(self) -> Optional[str]:
        """

        :return: Информация о подобранной машине
        :rtype: Optional[str]
        """
        return self.body.get("cargo_type")

    @property
    def cargo_type_int(self) -> Optional[int]:
        """

        :return: Информация о подобранной машине
        :rtype: Optional[int]
        """
        return self.body.get("cargo_type_int")

    @property
    def cargo_loaders(self) -> Optional[int]:
        """

        :return: Информация о подобранной машине
        :rtype: Optional[int]
        """
        return self.body.get("cargo_loaders")

    @property
    def door_to_door(self) -> Optional[bool]:
        """

        :return: Информация о подобранной машине
        :rtype: Optional[bool]
        """
        return self.body.get("door_to_door")

    @property
    def cargo_points(self) -> Optional[List['int']]:
        """

        :return: Информация о подобранной машине
        :rtype: Optional[List['int']]
        """
        return [item for item in self.body.get("cargo_points")]

    @property
    def cargo_points_field(self) -> Optional[str]:
        """

        :return: Информация о подобранной машине
        :rtype: Optional[str]
        """
        return self.body.get("cargo_points_field")
