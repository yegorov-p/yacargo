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

    def json(self) -> dict:
        """

        :return: Объект в виде JSON
        :rtype: dict
        """
        return self.body


class CargoItemMP(YCBase):
    """

    Груз для отправления

    :param Optional[str] extra_id: Краткий уникальный идентификатор item'а (в рамках заявки) (БП-208)
    :param int pickup_point: Идентификатор точки, откуда нужно забрать товар (отличается от идентификатора в заявке) *(Обязательный параметр)* (1)
    :param int droppof_point: Идентификатор точки, куда нужно доставить товар (отличается от идентификатора в заявке) *(Обязательный параметр)* (2)
    :param str title: Наименование единицы товара *(Обязательный параметр)* (Плюмбус)
    :param float size_length: Размер в метрах *(Обязательный параметр)* (0.1)
    :param float size_width: Размер в метрах *(Обязательный параметр)* (0.1)
    :param float size_height: Размер в метрах *(Обязательный параметр)* (0.1)
    :param Optional[float] weight: Вес единицы товара в кг. В поле следует передавать актуальные значения. Если вес не был передан, считается, что заказ оформлен на максимально допустимые габариты для тарифа. Если фактические характеристики отправления превысят допустимые, курьер вправе отказаться от выполнения такого заказа на месте. В этом случае будет удержана стоимость подачи. Габариты тарифа: Пеший курьер (courier без опции автокурьер): до 10 кг  Курьер на авто (courier с опции автокурьер): до 20 кг  Доставка (express): до 20 кг  Грузовой (cargo): Маленький кузов: до 300 кг Средний кузов: до 700 кг Большой кузов: до 1400 кг  (2.0)
    :param str cost_value: Цена за штуку в валюте cost_currency *(Обязательный параметр)* (2.00)
    :param str cost_currency: Валюта цены за штуку в формате ISO 4217 (используется в оплате при получении товара) *(Обязательный параметр)* (RUB)
    :param int quantity: Количество указанного товара *(Обязательный параметр)* (1)
    :param int fiscalization_vat_code: Ставка НДС *(Обязательный параметр)* (1)

        * **1** - Без НДС
        * **2** - НДС по ставке 0%
        * **3** - НДС по ставке 10%
        * **4** - НДС чека по ставке 20%
        * **5**	- НДС чека по расчетной ставке 10/110
        * **6** - НДС чека по расчетной ставке 20/120

    :param str fiscalization_payment_subject: Признак предмета расчета *(Обязательный параметр)* (commodity)

        * **commodity** - Товар
        * **excise** - Подакцизный товар
        * **job** - Работа
        * **service** - Услуга
        * **gambling_bet** - Ставка в азартной игре
        * **gambling_prize** - Выигрыш в азартной игре
        * **lottery** - Лотерейный билет
        * **lottery_prize** - Выигрыш в лотерею
        * **intellectual_activity** - Результаты интеллектуальной деятельности
        * **payment** - Платеж
        * **agent_commission** - Агентское вознаграждение
        * **property_right** - Имущественные права
        * **non_operating_gain** - Внереализационный доход
        * **insurance_premium** - Страховой сбор
        * **sales_tax** - Торговый сбор
        * **resort_fee** - Курортный сбор
        * **composite** - Несколько вариантов
        * **another** - Другое

    :param str fiscalization_payment_mode: Признак способа расчета *(Обязательный параметр)* (full_payment)

        * **full_prepayment** - Полная предоплата
        * **partial_prepayment** - Частичная предоплата
        * **advance** - Аванс
        * **full_payment** - Полный расчет
        * **partial_payment** - Частичный расчет и кредит
        * **credit** - Кредит
        * **credit_payment** - Выплата по кредиту

    :param Optional[str] fiscalization_product_code: Код товара
    :param Optional[str] fiscalization_country_of_origin_code: Код страны происхождения товара (RU)
    :param Optional[str] fiscalization_customs_declaration_number: Номер таможенной декларации (10702030/260917/0080123)
    :param str fiscalization_excise: Цена Decimal(19, 4) *(Обязательный параметр)* (12.50)
    """

    def __init__(self,
                 extra_id: Optional[str] = None,
                 pickup_point: int = None,
                 droppof_point: int = None,
                 title: str = None,
                 size_length: float = None,
                 size_width: float = None,
                 size_height: float = None,
                 weight: Optional[float] = None,
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

        if pickup_point is not None:
            self.body["pickup_point"] = validate_fields('pickup_point', pickup_point, int)
        if pickup_point is None:
            raise InputParamError("<pickup_point> (=>pickup_point) of <CargoItemMP> is a required parameter")

        if droppof_point is not None:
            self.body["droppof_point"] = validate_fields('droppof_point', droppof_point, int)
        if droppof_point is None:
            raise InputParamError("<droppof_point> (=>droppof_point) of <CargoItemMP> is a required parameter")

        if title is not None:
            self.body["title"] = validate_fields('title', title, str)
        if title is None:
            raise InputParamError("<title> (=>title) of <CargoItemMP> is a required parameter")

        if size_length is not None:
            self.body["size"]["length"] = validate_fields('size_length', size_length, float)
        if size_length is None:
            raise InputParamError("<size_length> (size=>length) of <CargoItemMP> is a required parameter")

        if size_width is not None:
            self.body["size"]["width"] = validate_fields('size_width', size_width, float)
        if size_width is None:
            raise InputParamError("<size_width> (size=>width) of <CargoItemMP> is a required parameter")

        if size_height is not None:
            self.body["size"]["height"] = validate_fields('size_height', size_height, float)
        if size_height is None:
            raise InputParamError("<size_height> (size=>height) of <CargoItemMP> is a required parameter")

        if weight is not None:
            self.body["weight"] = validate_fields('weight', weight, float)

        if cost_value is not None:
            self.body["cost_value"] = validate_fields('cost_value', cost_value, str)
        if cost_value is None:
            raise InputParamError("<cost_value> (=>cost_value) of <CargoItemMP> is a required parameter")

        if cost_currency is not None:
            self.body["cost_currency"] = validate_fields('cost_currency', cost_currency, str)
        if cost_currency and len(cost_currency) < 3:
            raise InputParamError("<cost_currency> of <CargoItemMP> should contain at least 3 element")
        if cost_currency and len(cost_currency) > 3:
            raise InputParamError("<cost_currency> of <CargoItemMP> should not contain more than 3 element")
        if cost_currency is None:
            raise InputParamError("<cost_currency> (=>cost_currency) of <CargoItemMP> is a required parameter")

        if quantity is not None:
            self.body["quantity"] = validate_fields('quantity', quantity, int)
        if quantity and quantity < 1:
            raise InputParamError("<quantity> of <CargoItemMP> should be more than 1")
        if quantity is None:
            raise InputParamError("<quantity> (=>quantity) of <CargoItemMP> is a required parameter")

        if fiscalization_vat_code is not None:
            self.body["fiscalization"]["vat_code"] = validate_fields('fiscalization_vat_code', fiscalization_vat_code, int)
        if fiscalization_vat_code and fiscalization_vat_code < 1:
            raise InputParamError("<fiscalization_vat_code> of <CargoItemMP> should be more than 1")
        if fiscalization_vat_code and fiscalization_vat_code > 6:
            raise InputParamError("<fiscalization_vat_code> of <CargoItemMP> should be less than 6")
        if fiscalization_vat_code is None:
            raise InputParamError("<fiscalization_vat_code> (fiscalization=>vat_code) of <CargoItemMP> is a required parameter")

        if fiscalization_payment_subject is not None:
            self.body["fiscalization"]["payment_subject"] = validate_fields('fiscalization_payment_subject', fiscalization_payment_subject, str)
        if fiscalization_payment_subject is None:
            raise InputParamError("<fiscalization_payment_subject> (fiscalization=>payment_subject) of <CargoItemMP> is a required parameter")

        if fiscalization_payment_mode is not None:
            self.body["fiscalization"]["payment_mode"] = validate_fields('fiscalization_payment_mode', fiscalization_payment_mode, str)
        if fiscalization_payment_mode is None:
            raise InputParamError("<fiscalization_payment_mode> (fiscalization=>payment_mode) of <CargoItemMP> is a required parameter")

        if fiscalization_product_code is not None:
            self.body["fiscalization"]["product_code"] = validate_fields('fiscalization_product_code', fiscalization_product_code, str)

        if fiscalization_country_of_origin_code is not None:
            self.body["fiscalization"]["country_of_origin_code"] = validate_fields('fiscalization_country_of_origin_code', fiscalization_country_of_origin_code, str)

        if fiscalization_customs_declaration_number is not None:
            self.body["fiscalization"]["customs_declaration_number"] = validate_fields('fiscalization_customs_declaration_number', fiscalization_customs_declaration_number, str)
        if fiscalization_customs_declaration_number and len(fiscalization_customs_declaration_number) < 1:
            raise InputParamError("<fiscalization_customs_declaration_number> of <CargoItemMP> should contain at least 1 element")
        if fiscalization_customs_declaration_number and len(fiscalization_customs_declaration_number) > 32:
            raise InputParamError("<fiscalization_customs_declaration_number> of <CargoItemMP> should not contain more than 32 element")

        if fiscalization_excise is not None:
            self.body["fiscalization"]["excise"] = validate_fields('fiscalization_excise', fiscalization_excise, str)
        if fiscalization_excise is None:
            raise InputParamError("<fiscalization_excise> (fiscalization=>excise) of <CargoItemMP> is a required parameter")

    def __repr__(self):
        return "<CargoItemMP>"

    @property
    def extra_id(self) -> Optional[str]:
        """

        :return: Краткий уникальный идентификатор item'а (в рамках заявки)
        :rtype: Optional[str]
        """
        return self.body.get("extra_id")

    @property
    def pickup_point(self) -> int:
        """

        :return: Идентификатор точки, откуда нужно забрать товар (отличается от идентификатора в заявке)
        :rtype: int
        """
        return self.body.get("pickup_point")

    @property
    def droppof_point(self) -> int:
        """

        :return: Идентификатор точки, куда нужно доставить товар (отличается от идентификатора в заявке)
        :rtype: int
        """
        return self.body.get("droppof_point")

    @property
    def title(self) -> str:
        """

        :return: Наименование единицы товара
        :rtype: str
        """
        return self.body.get("title")

    @property
    def size_length(self) -> float:
        """

        :return: Размер в метрах
        :rtype: float
        """
        return self.body.get("size_length")

    @property
    def size_width(self) -> float:
        """

        :return: Размер в метрах
        :rtype: float
        """
        return self.body.get("size_width")

    @property
    def size_height(self) -> float:
        """

        :return: Размер в метрах
        :rtype: float
        """
        return self.body.get("size_height")

    @property
    def weight(self) -> Optional[float]:
        """

        :return: Вес единицы товара в кг. В поле следует передавать актуальные значения. Если вес не был передан, считается, что заказ оформлен на максимально допустимые габариты для тарифа. Если фактические характеристики отправления превысят допустимые, курьер вправе отказаться от выполнения такого заказа на месте. В этом случае будет удержана стоимость подачи. Габариты тарифа: Пеший курьер (courier без опции автокурьер): до 10 кг  Курьер на авто (courier с опции автокурьер): до 20 кг  Доставка (express): до 20 кг  Грузовой (cargo): Маленький кузов: до 300 кг Средний кузов: до 700 кг Большой кузов: до 1400 кг
        :rtype: Optional[float]
        """
        return self.body.get("weight")

    @property
    def cost_value(self) -> str:
        """

        :return: Цена за штуку в валюте cost_currency
        :rtype: str
        """
        return self.body.get("cost_value")

    @property
    def cost_currency(self) -> str:
        """

        :return: Валюта цены за штуку в формате ISO 4217 (используется в оплате при получении товара)
        :rtype: str
        """
        return self.body.get("cost_currency")

    @property
    def quantity(self) -> int:
        """

        :return: Количество указанного товара
        :rtype: int
        """
        return self.body.get("quantity")

    @property
    def fiscalization_vat_code(self) -> int:
        """

        :return: Ставка НДС

            * **1** - Без НДС
            * **2** - НДС по ставке 0%
            * **3** - НДС по ставке 10%
            * **4** - НДС чека по ставке 20%
            * **5**	- НДС чека по расчетной ставке 10/110
            * **6** - НДС чека по расчетной ставке 20/120

        :rtype: int
        """
        return self.body.get("fiscalization_vat_code")

    @property
    def fiscalization_payment_subject(self) -> str:
        """

        :return: Признак предмета расчета

            * **commodity** - Товар
            * **excise** - Подакцизный товар
            * **job** - Работа
            * **service** - Услуга
            * **gambling_bet** - Ставка в азартной игре
            * **gambling_prize** - Выигрыш в азартной игре
            * **lottery** - Лотерейный билет
            * **lottery_prize** - Выигрыш в лотерею
            * **intellectual_activity** - Результаты интеллектуальной деятельности
            * **payment** - Платеж
            * **agent_commission** - Агентское вознаграждение
            * **property_right** - Имущественные права
            * **non_operating_gain** - Внереализационный доход
            * **insurance_premium** - Страховой сбор
            * **sales_tax** - Торговый сбор
            * **resort_fee** - Курортный сбор
            * **composite** - Несколько вариантов
            * **another** - Другое

        :rtype: str
        """
        return self.body.get("fiscalization_payment_subject")

    @property
    def fiscalization_payment_mode(self) -> str:
        """

        :return: Признак способа расчета

            * **full_prepayment** - Полная предоплата
            * **partial_prepayment** - Частичная предоплата
            * **advance** - Аванс
            * **full_payment** - Полный расчет
            * **partial_payment** - Частичный расчет и кредит
            * **credit** - Кредит
            * **credit_payment** - Выплата по кредиту

        :rtype: str
        """
        return self.body.get("fiscalization_payment_mode")

    @property
    def fiscalization_product_code(self) -> Optional[str]:
        """

        :return: Код товара
        :rtype: Optional[str]
        """
        return self.body.get("fiscalization_product_code")

    @property
    def fiscalization_country_of_origin_code(self) -> Optional[str]:
        """

        :return: Код страны происхождения товара
        :rtype: Optional[str]
        """
        return self.body.get("fiscalization_country_of_origin_code")

    @property
    def fiscalization_customs_declaration_number(self) -> Optional[str]:
        """

        :return: Номер таможенной декларации
        :rtype: Optional[str]
        """
        return self.body.get("fiscalization_customs_declaration_number")

    @property
    def fiscalization_excise(self) -> str:
        """

        :return: Цена Decimal(19, 4)
        :rtype: str
        """
        return self.body.get("fiscalization_excise")


class CargoPointMP(YCBase):
    """

    Описание точки в заявке с мультиточками

    :param int point_id: Целочисленный идентификатор точки *(Обязательный параметр)* (6987)
    :param int visit_order: Порядок посещения точки *(Обязательный параметр)* (1)
    :param str contact_name: Имя контактного лица *(Обязательный параметр)* (Морти)
    :param str contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999998)
    :param Optional[str] contact_email: Email — обязательный параметр для точек source и return (morty@yandex.ru)
    :param str address_fullname: Полное название с указанием города (Москва, Садовническая набережная, 82с2, БЦ Аврора) *(Обязательный параметр)* (Санкт-Петербург, Большая Монетная улица, 1к1А)
    :param Optional[str] address_shortname: Адрес в пределах города, как показывается на Таксометре (Садовническая набережная, 82с2, БЦ Аврора) (Большая Монетная улица, 1к1А)
    :param List['float'] address_coordinates: Массив из двух вещественных чисел [долгота, широта]. Порядок важен! *(Обязательный параметр)*
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
    :param Optional[str] address_comment: Комментарий для курьера Для точки А (откуда забрать отправление) используйте шаблон: "Доставка из магазина <>. Сообщите менеджеру, что заказ по доставке Яндекс.Такси. Назовите номер заказа <> и заберите посылку. Заказ оплачен безналично, при передаче заказа нельзя требовать с получателя деньги за доставку." Для точек Б (куда доставить) в комментарий передавайте пожелания получателя. Например "домофон не работает" / "шлагбаум закрыт, позвонить за 10 минут" / "не звонить, спит ребенок".  (Домофон не работает)
    :param Optional[str] address_uri: Карточный uri геообъекта (ymapsbm1://geo?ll=38.805%2C55.084)
    :param Optional[bool] skip_confirmation: Пропускать подтверждение через SMS в данной точке
    :param str type: Тип точки *(Обязательный параметр)* (source)

        * **source** — точка получения отправления (ровно одна)
        * **destination** — точка доставки отправления
        * **return** — точка возврата части товаров, опциональная (не более одной)

    :param str payment_on_delivery_client_order_id: Идентификатор заказа *(Обязательный параметр)* (100)
    :param str payment_on_delivery_cost: Цена Decimal(19, 4) *(Обязательный параметр)* (12.50)
    :param Optional[str] payment_on_delivery_customer_full_name: Для юридического лица — название организации, для ИП и физического лица — ФИО (Morty)
    :param Optional[str] payment_on_delivery_customer_inn: ИНН пользователя (10 или 12 цифр) (3664069397)
    :param Optional[str] payment_on_delivery_customer_email: Электронная почта пользователя. Если не указано, будет использована почта получателя из точки (morty@yandex.ru)
    :param Optional[str] payment_on_delivery_customer_phone: Телефон пользователя. Если не указано, будет использован телефон получателя из точки (79000000000)
    :param Optional[int] payment_on_delivery_tax_system_code: Система налогообложения магазина (1)

        * **1** - Общая система налогообложения
        * **2** - Упрощенная (УСН, доходы)
        * **3** - Упрощенная (УСН, доходы минус расходы)
        * **4** - Единый налог на вмененный доход (ЕНВД)
        * **5** - Единый сельскохозяйственный налог (ЕСН)
        * **6** - Патентная система налогообложения

    :param Optional[str] payment_on_delivery_currency: Трехзначный код валюты, в которой ведется расчет (RUB)
    :param Optional[str] external_order_id: Номер заказа клиента (100)
    :param Optional[str] pickup_code: Код выдачи товара (ПВЗ) (8934)
    :param Optional[List['TimeInterval']] time_intervals: Интервалы, навешанные на точку
    """

    def __init__(self,
                 point_id: int = None,
                 visit_order: int = None,
                 contact_name: str = None,
                 contact_phone: str = None,
                 contact_email: Optional[str] = None,
                 address_fullname: str = None,
                 address_shortname: Optional[str] = None,
                 address_coordinates: List['float'] = None,
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
                 payment_on_delivery_cost: str = None,
                 payment_on_delivery_customer_full_name: Optional[str] = None,
                 payment_on_delivery_customer_inn: Optional[str] = None,
                 payment_on_delivery_customer_email: Optional[str] = None,
                 payment_on_delivery_customer_phone: Optional[str] = None,
                 payment_on_delivery_tax_system_code: Optional[int] = None,
                 payment_on_delivery_currency: Optional[str] = None,
                 external_order_id: Optional[str] = None,
                 pickup_code: Optional[str] = None,
                 time_intervals: Optional[List['TimeInterval']] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if point_id is not None:
            self.body["point_id"] = validate_fields('point_id', point_id, int)
        if point_id is None:
            raise InputParamError("<point_id> (=>point_id) of <CargoPointMP> is a required parameter")

        if visit_order is not None:
            self.body["visit_order"] = validate_fields('visit_order', visit_order, int)
        if visit_order is None:
            raise InputParamError("<visit_order> (=>visit_order) of <CargoPointMP> is a required parameter")

        if contact_name is not None:
            self.body["contact"]["name"] = validate_fields('contact_name', contact_name, str)
        if contact_name is None:
            raise InputParamError("<contact_name> (contact=>name) of <CargoPointMP> is a required parameter")

        if contact_phone is not None:
            self.body["contact"]["phone"] = validate_fields('contact_phone', contact_phone, str)
        if contact_phone is None:
            raise InputParamError("<contact_phone> (contact=>phone) of <CargoPointMP> is a required parameter")

        if contact_email is not None:
            self.body["contact"]["email"] = validate_fields('contact_email', contact_email, str)

        if address_fullname is not None:
            self.body["address"]["fullname"] = validate_fields('address_fullname', address_fullname, str)
        if address_fullname is None:
            raise InputParamError("<address_fullname> (address=>fullname) of <CargoPointMP> is a required parameter")

        if address_shortname is not None:
            self.body["address"]["shortname"] = validate_fields('address_shortname', address_shortname, str)

        if address_coordinates is not None:
            self.body["address"]["coordinates"] = validate_fields('address_coordinates', address_coordinates, List['float'])
        if address_coordinates and len(address_coordinates) < 2:
            raise InputParamError("<address_coordinates> of <CargoPointMP> should contain at least 2 element")
        if address_coordinates and len(address_coordinates) > 2:
            raise InputParamError("<address_coordinates> of <CargoPointMP> should not contain more than 2 element")
        if address_coordinates is None:
            raise InputParamError("<address_coordinates> (address=>coordinates) of <CargoPointMP> is a required parameter")

        if address_country is not None:
            self.body["address"]["country"] = validate_fields('address_country', address_country, str)

        if address_city is not None:
            self.body["address"]["city"] = validate_fields('address_city', address_city, str)

        if address_street is not None:
            self.body["address"]["street"] = validate_fields('address_street', address_street, str)

        if address_building is not None:
            self.body["address"]["building"] = validate_fields('address_building', address_building, str)

        if address_porch is not None:
            self.body["address"]["porch"] = validate_fields('address_porch', address_porch, str)

        if address_floor is not None:
            self.body["address"]["floor"] = validate_fields('address_floor', address_floor, int)

        if address_flat is not None:
            self.body["address"]["flat"] = validate_fields('address_flat', address_flat, int)

        if address_sfloor is not None:
            self.body["address"]["sfloor"] = validate_fields('address_sfloor', address_sfloor, str)

        if address_sflat is not None:
            self.body["address"]["sflat"] = validate_fields('address_sflat', address_sflat, str)

        if address_door_code is not None:
            self.body["address"]["door_code"] = validate_fields('address_door_code', address_door_code, str)

        if address_comment is not None:
            self.body["address"]["comment"] = validate_fields('address_comment', address_comment, str)

        if address_uri is not None:
            self.body["address"]["uri"] = validate_fields('address_uri', address_uri, str)

        if skip_confirmation is not None:
            self.body["skip_confirmation"] = validate_fields('skip_confirmation', skip_confirmation, bool)

        if type is not None:
            self.body["type"] = validate_fields('type', type, str)
        if type is None:
            raise InputParamError("<type> (=>type) of <CargoPointMP> is a required parameter")

        if type not in ['source', 'destination', 'return']:
            raise InputParamError("<type> of <CargoPointMP> should be in ['source', 'destination', 'return']")

        if payment_on_delivery_client_order_id is not None:
            self.body["payment_on_delivery"]["client_order_id"] = validate_fields('payment_on_delivery_client_order_id', payment_on_delivery_client_order_id, str)
        if payment_on_delivery_client_order_id is None:
            raise InputParamError("<payment_on_delivery_client_order_id> (payment_on_delivery=>client_order_id) of <CargoPointMP> is a required parameter")

        if payment_on_delivery_cost is not None:
            self.body["payment_on_delivery"]["cost"] = validate_fields('payment_on_delivery_cost', payment_on_delivery_cost, str)
        if payment_on_delivery_cost is None:
            raise InputParamError("<payment_on_delivery_cost> (payment_on_delivery=>cost) of <CargoPointMP> is a required parameter")

        if payment_on_delivery_customer_full_name is not None:
            self.body["payment_on_delivery"]["customer"]["full_name"] = validate_fields('payment_on_delivery_customer_full_name', payment_on_delivery_customer_full_name, str)

        if payment_on_delivery_customer_inn is not None:
            self.body["payment_on_delivery"]["customer"]["inn"] = validate_fields('payment_on_delivery_customer_inn', payment_on_delivery_customer_inn, str)

        if payment_on_delivery_customer_email is not None:
            self.body["payment_on_delivery"]["customer"]["email"] = validate_fields('payment_on_delivery_customer_email', payment_on_delivery_customer_email, str)

        if payment_on_delivery_customer_phone is not None:
            self.body["payment_on_delivery"]["customer"]["phone"] = validate_fields('payment_on_delivery_customer_phone', payment_on_delivery_customer_phone, str)

        if payment_on_delivery_tax_system_code is not None:
            self.body["payment_on_delivery"]["tax_system_code"] = validate_fields('payment_on_delivery_tax_system_code', payment_on_delivery_tax_system_code, int)
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code < 1:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <CargoPointMP> should be more than 1")
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code > 6:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <CargoPointMP> should be less than 6")

        if payment_on_delivery_currency is not None:
            self.body["payment_on_delivery"]["currency"] = validate_fields('payment_on_delivery_currency', payment_on_delivery_currency, str)
        if payment_on_delivery_currency and len(payment_on_delivery_currency) < 3:
            raise InputParamError("<payment_on_delivery_currency> of <CargoPointMP> should contain at least 3 element")
        if payment_on_delivery_currency and len(payment_on_delivery_currency) > 3:
            raise InputParamError("<payment_on_delivery_currency> of <CargoPointMP> should not contain more than 3 element")

        if external_order_id is not None:
            self.body["external_order_id"] = validate_fields('external_order_id', external_order_id, str)

        if pickup_code is not None:
            self.body["pickup_code"] = validate_fields('pickup_code', pickup_code, str)

        if time_intervals is not None:
            self.body["time_intervals"] = validate_fields('time_intervals', time_intervals, List['TimeInterval'])

    def __repr__(self):
        return "<CargoPointMP>"

    @property
    def point_id(self) -> int:
        """

        :return: Целочисленный идентификатор точки
        :rtype: int
        """
        return self.body.get("point_id")

    @property
    def visit_order(self) -> int:
        """

        :return: Порядок посещения точки
        :rtype: int
        """
        return self.body.get("visit_order")

    @property
    def contact_name(self) -> str:
        """

        :return: Имя контактного лица
        :rtype: str
        """
        return self.body.get("contact_name")

    @property
    def contact_phone(self) -> str:
        """

        :return: Телефон контактного лица
        :rtype: str
        """
        return self.body.get("contact_phone")

    @property
    def contact_email(self) -> Optional[str]:
        """

        :return: Email — обязательный параметр для точек source и return
        :rtype: Optional[str]
        """
        return self.body.get("contact_email")

    @property
    def address_fullname(self) -> str:
        """

        :return: Полное название с указанием города (Москва, Садовническая набережная, 82с2, БЦ Аврора)
        :rtype: str
        """
        return self.body.get("address_fullname")

    @property
    def address_shortname(self) -> Optional[str]:
        """

        :return: Адрес в пределах города, как показывается на Таксометре (Садовническая набережная, 82с2, БЦ Аврора)
        :rtype: Optional[str]
        """
        return self.body.get("address_shortname")

    @property
    def address_coordinates(self) -> List['float']:
        """

        :return: Массив из двух вещественных чисел [долгота, широта]. Порядок важен!
        :rtype: List['float']
        """
        return [item for item in self.body.get("address_coordinates")]

    @property
    def address_country(self) -> Optional[str]:
        """

        :return: Страна
        :rtype: Optional[str]
        """
        return self.body.get("address_country")

    @property
    def address_city(self) -> Optional[str]:
        """

        :return: Город
        :rtype: Optional[str]
        """
        return self.body.get("address_city")

    @property
    def address_street(self) -> Optional[str]:
        """

        :return: Улица
        :rtype: Optional[str]
        """
        return self.body.get("address_street")

    @property
    def address_building(self) -> Optional[str]:
        """

        :return: Строение
        :rtype: Optional[str]
        """
        return self.body.get("address_building")

    @property
    def address_porch(self) -> Optional[str]:
        """

        :return: Подъезд (может быть A)
        :rtype: Optional[str]
        """
        return self.body.get("address_porch")

    @property
    def address_floor(self) -> Optional[int]:
        """

        :return: Этаж (DEPRECATED)
        :rtype: Optional[int]
        """
        return self.body.get("address_floor")

    @property
    def address_flat(self) -> Optional[int]:
        """

        :return: Квартира (DEPRECATED)
        :rtype: Optional[int]
        """
        return self.body.get("address_flat")

    @property
    def address_sfloor(self) -> Optional[str]:
        """

        :return: Этаж
        :rtype: Optional[str]
        """
        return self.body.get("address_sfloor")

    @property
    def address_sflat(self) -> Optional[str]:
        """

        :return: Квартира
        :rtype: Optional[str]
        """
        return self.body.get("address_sflat")

    @property
    def address_door_code(self) -> Optional[str]:
        """

        :return: Код домофона
        :rtype: Optional[str]
        """
        return self.body.get("address_door_code")

    @property
    def address_comment(self) -> Optional[str]:
        """

        :return: Комментарий для курьера Для точки А (откуда забрать отправление) используйте шаблон: "Доставка из магазина <>. Сообщите менеджеру, что заказ по доставке Яндекс.Такси. Назовите номер заказа <> и заберите посылку. Заказ оплачен безналично, при передаче заказа нельзя требовать с получателя деньги за доставку." Для точек Б (куда доставить) в комментарий передавайте пожелания получателя. Например "домофон не работает" / "шлагбаум закрыт, позвонить за 10 минут" / "не звонить, спит ребенок".
        :rtype: Optional[str]
        """
        return self.body.get("address_comment")

    @property
    def address_uri(self) -> Optional[str]:
        """

        :return: Карточный uri геообъекта
        :rtype: Optional[str]
        """
        return self.body.get("address_uri")

    @property
    def skip_confirmation(self) -> Optional[bool]:
        """

        :return: Пропускать подтверждение через SMS в данной точке
        :rtype: Optional[bool]
        """
        return self.body.get("skip_confirmation")

    @property
    def type(self) -> str:
        """

        :return: Тип точки

            * **source** — точка получения отправления (ровно одна)
            * **destination** — точка доставки отправления
            * **return** — точка возврата части товаров, опциональная (не более одной)

        :rtype: str
        """
        return self.body.get("type")

    @property
    def payment_on_delivery_client_order_id(self) -> str:
        """

        :return: Идентификатор заказа
        :rtype: str
        """
        return self.body.get("payment_on_delivery_client_order_id")

    @property
    def payment_on_delivery_cost(self) -> str:
        """

        :return: Цена Decimal(19, 4)
        :rtype: str
        """
        return self.body.get("payment_on_delivery_cost")

    @property
    def payment_on_delivery_customer_full_name(self) -> Optional[str]:
        """

        :return: Для юридического лица — название организации, для ИП и физического лица — ФИО
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_full_name")

    @property
    def payment_on_delivery_customer_inn(self) -> Optional[str]:
        """

        :return: ИНН пользователя (10 или 12 цифр)
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_inn")

    @property
    def payment_on_delivery_customer_email(self) -> Optional[str]:
        """

        :return: Электронная почта пользователя. Если не указано, будет использована почта получателя из точки
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_email")

    @property
    def payment_on_delivery_customer_phone(self) -> Optional[str]:
        """

        :return: Телефон пользователя. Если не указано, будет использован телефон получателя из точки
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_phone")

    @property
    def payment_on_delivery_tax_system_code(self) -> Optional[int]:
        """

        :return: Система налогообложения магазина

            * **1** - Общая система налогообложения
            * **2** - Упрощенная (УСН, доходы)
            * **3** - Упрощенная (УСН, доходы минус расходы)
            * **4** - Единый налог на вмененный доход (ЕНВД)
            * **5** - Единый сельскохозяйственный налог (ЕСН)
            * **6** - Патентная система налогообложения

        :rtype: Optional[int]
        """
        return self.body.get("payment_on_delivery_tax_system_code")

    @property
    def payment_on_delivery_currency(self) -> Optional[str]:
        """

        :return: Трехзначный код валюты, в которой ведется расчет
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_currency")

    @property
    def external_order_id(self) -> Optional[str]:
        """

        :return: Номер заказа клиента
        :rtype: Optional[str]
        """
        return self.body.get("external_order_id")

    @property
    def pickup_code(self) -> Optional[str]:
        """

        :return: Код выдачи товара (ПВЗ)
        :rtype: Optional[str]
        """
        return self.body.get("pickup_code")

    @property
    def time_intervals(self) -> Optional[List['TimeInterval']]:
        """

        :return: Интервалы, навешанные на точку
        :rtype: Optional[List['TimeInterval']]
        """
        return [TimeInterval(type=item.get("type", None),
                             _from=item.get("from", None),
                             to=item.get("to", None),
                             ) for item in self.body.get("time_intervals")]


class ClaimRequirement(YCBase):
    """

    Информация о дополнительных требованиях к заявке

    :param str type: ??? *(Обязательный параметр)* (performer_group)
    :param str logistic_group: ??? *(Обязательный параметр)* (ya_eats_group)
    :param Optional[str] meta_group: ??? (lavka)
    """

    def __init__(self,
                 type: str = None,
                 logistic_group: str = None,
                 meta_group: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if type is not None:
            self.body["type"] = validate_fields('type', type, str)
        if type is None:
            raise InputParamError("<type> (=>type) of <ClaimRequirement> is a required parameter")

        if logistic_group is not None:
            self.body["logistic_group"] = validate_fields('logistic_group', logistic_group, str)
        if logistic_group is None:
            raise InputParamError("<logistic_group> (=>logistic_group) of <ClaimRequirement> is a required parameter")

        if meta_group is not None:
            self.body["meta_group"] = validate_fields('meta_group', meta_group, str)

    def __repr__(self):
        return "<ClaimRequirement>"

    @property
    def type(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("type")

    @property
    def logistic_group(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get("logistic_group")

    @property
    def meta_group(self) -> Optional[str]:
        """

        :return: ???
        :rtype: Optional[str]
        """
        return self.body.get("meta_group")


class ClaimWarning(YCBase):
    """

    Информация о предупреждении

    :param str source: Источник предупреждения *(Обязательный параметр)* (client_requirements)

        * **client_requirements** - Требования клиента
        * **taxi_requirements** - Требования такси

    :param str code: Тип предупреждения *(Обязательный параметр)* (not_fit_in_car)

        * **not_fit_in_car** - Товар не помещается в заявленное транспортное средство
        * **requirement_unavailable** - Некоторые из пожеланий недоступны на выбранном тарифе

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
        if source is None:
            raise InputParamError("<source> (=>source) of <ClaimWarning> is a required parameter")

        if source not in ['client_requirements', 'taxi_requirements']:
            raise InputParamError("<source> of <ClaimWarning> should be in ['client_requirements', 'taxi_requirements']")

        if code is not None:
            self.body["code"] = validate_fields('code', code, str)
        if code is None:
            raise InputParamError("<code> (=>code) of <ClaimWarning> is a required parameter")

        if code not in ['not_fit_in_car', 'requirement_unavailable']:
            raise InputParamError("<code> of <ClaimWarning> should be in ['not_fit_in_car', 'requirement_unavailable']")

        if message is not None:
            self.body["message"] = validate_fields('message', message, str)

    def __repr__(self):
        return "<ClaimWarning>"

    @property
    def source(self) -> str:
        """

        :return: Источник предупреждения

            * **client_requirements** - Требования клиента
            * **taxi_requirements** - Требования такси

        :rtype: str
        """
        return self.body.get("source")

    @property
    def code(self) -> str:
        """

        :return: Тип предупреждения

            * **not_fit_in_car** - Товар не помещается в заявленное транспортное средство
            * **requirement_unavailable** - Некоторые из пожеланий недоступны на выбранном тарифе

        :rtype: str
        """
        return self.body.get("code")

    @property
    def message(self) -> Optional[str]:
        """

        :return: Локализованная информация с причиной предупреждения
        :rtype: Optional[str]
        """
        return self.body.get("message")


class ClaimsJournalResponse(YCBase):
    """

    Информация об событиях в журнале изменений заказа

    :param str cursor: Идентификатор последнего изменения *(Обязательный параметр)*
    :param List['Event'] events: Список изменений заказа *(Обязательный параметр)*
    """

    def __init__(self,
                 cursor: str = None,
                 events: List['Event'] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if cursor is not None:
            self.body["cursor"] = validate_fields('cursor', cursor, str)
        if cursor is None:
            raise InputParamError("<cursor> (=>cursor) of <ClaimsJournalResponse> is a required parameter")

        if events is not None:
            self.body["events"] = validate_fields('events', events, List['Event'])
        if events is None:
            raise InputParamError("<events> (=>events) of <ClaimsJournalResponse> is a required parameter")

    def __repr__(self):
        return "<ClaimsJournalResponse>"

    @property
    def cursor(self) -> str:
        """

        :return: Идентификатор последнего изменения
        :rtype: str
        """
        return self.body.get("cursor")

    @property
    def events(self) -> List['Event']:
        """

        :return: Список изменений заказа
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


class ClaimsReportGenerateResponse(YCBase):
    """

    Информация о статусе генерации отчета

    :param str task_id: ID, по которому можно запрашивать статус *(Обязательный параметр)* (f9b4825f45f64914affaeb07fbae9757)
    """

    def __init__(self,
                 task_id: str = None,
                 ):
        self.body = collections.defaultdict(dict)

        if task_id is not None:
            self.body["task_id"] = validate_fields('task_id', task_id, str)
        if task_id is None:
            raise InputParamError("<task_id> (=>task_id) of <ClaimsReportGenerateResponse> is a required parameter")

    def __repr__(self):
        return "<ClaimsReportGenerateResponse>"

    @property
    def task_id(self) -> str:
        """

        :return: ID, по которому можно запрашивать статус
        :rtype: str
        """
        return self.body.get("task_id")


class ClaimsReportStatusResponse(YCBase):
    """

    Информация о статусе отчета

    :param str task_id: task_id из запроса *(Обязательный параметр)* (f9b4825f45f4914affaeb07fbae9757)
    :param str status: Информация о статусе отчета *(Обязательный параметр)* (in_progress)

        * **in_progress** - в процессе формирования
        * **retry** - повторная попытка формирования
        * **complete** - сформирован
        * **failed** - ошибка при формировании

    :param str author: Yandex Login автора отчета *(Обязательный параметр)* (morty)
    :param str created_at: Дата формирования отчета *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
    :param str request_since_date: Дата начала отчетного периода *(Обязательный параметр)* (2020-01-01)
    :param str request_till_date: Дата конца отчетного периода *(Обязательный параметр)* (2020-01-02)
    :param Optional[str] request_lang: Язык, на котором надо генерировать отчет. Если не указан, будет использован Accept-Language  (ru)
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
        if task_id is None:
            raise InputParamError("<task_id> (=>task_id) of <ClaimsReportStatusResponse> is a required parameter")

        if status is not None:
            self.body["status"] = validate_fields('status', status, str)
        if status is None:
            raise InputParamError("<status> (=>status) of <ClaimsReportStatusResponse> is a required parameter")

        if status not in ['in_progress', 'retry', 'complete', 'failed']:
            raise InputParamError("<status> of <ClaimsReportStatusResponse> should be in ['in_progress', 'retry', 'complete', 'failed']")

        if author is not None:
            self.body["author"] = validate_fields('author', author, str)
        if author is None:
            raise InputParamError("<author> (=>author) of <ClaimsReportStatusResponse> is a required parameter")

        if created_at is not None:
            self.body["created_at"] = validate_fields('created_at', created_at, str)
        if created_at is None:
            raise InputParamError("<created_at> (=>created_at) of <ClaimsReportStatusResponse> is a required parameter")

        if request_since_date is not None:
            self.body["request"]["since_date"] = validate_fields('request_since_date', request_since_date, str)
        if request_since_date is None:
            raise InputParamError("<request_since_date> (request=>since_date) of <ClaimsReportStatusResponse> is a required parameter")

        if request_till_date is not None:
            self.body["request"]["till_date"] = validate_fields('request_till_date', request_till_date, str)
        if request_till_date is None:
            raise InputParamError("<request_till_date> (request=>till_date) of <ClaimsReportStatusResponse> is a required parameter")

        if request_lang is not None:
            self.body["request"]["lang"] = validate_fields('request_lang', request_lang, str)

        if request_department_id is not None:
            self.body["request"]["department_id"] = validate_fields('request_department_id', request_department_id, str)

        if request_idempotency_token is not None:
            self.body["request"]["idempotency_token"] = validate_fields('request_idempotency_token', request_idempotency_token, str)
        if request_idempotency_token is None:
            raise InputParamError("<request_idempotency_token> (request=>idempotency_token) of <ClaimsReportStatusResponse> is a required parameter")

        if url is not None:
            self.body["url"] = validate_fields('url', url, str)

    def __repr__(self):
        return "<ClaimsReportStatusResponse>"

    @property
    def task_id(self) -> str:
        """

        :return: task_id из запроса
        :rtype: str
        """
        return self.body.get("task_id")

    @property
    def status(self) -> str:
        """

        :return: Информация о статусе отчета

            * **in_progress** - в процессе формирования
            * **retry** - повторная попытка формирования
            * **complete** - сформирован
            * **failed** - ошибка при формировании

        :rtype: str
        """
        return self.body.get("status")

    @property
    def author(self) -> str:
        """

        :return: Yandex Login автора отчета
        :rtype: str
        """
        return self.body.get("author")

    @property
    def created_at(self) -> str:
        """

        :return: Дата формирования отчета
        :rtype: str
        """
        return self.body.get("created_at")

    @property
    def request_since_date(self) -> str:
        """

        :return: Дата начала отчетного периода
        :rtype: str
        """
        return self.body.get("request_since_date")

    @property
    def request_till_date(self) -> str:
        """

        :return: Дата конца отчетного периода
        :rtype: str
        """
        return self.body.get("request_till_date")

    @property
    def request_lang(self) -> Optional[str]:
        """

        :return: Язык, на котором надо генерировать отчет. Если не указан, будет использован Accept-Language
        :rtype: Optional[str]
        """
        return self.body.get("request_lang")

    @property
    def request_department_id(self) -> Optional[str]:
        """

        :return: ID отдела (значение игнорируется). Поле нужно для совместимости с API КК
        :rtype: Optional[str]
        """
        return self.body.get("request_department_id")

    @property
    def request_idempotency_token(self) -> str:
        """

        :return: Уникальный для данного клиента токен идемпотентности
        :rtype: str
        """
        return self.body.get("request_idempotency_token")

    @property
    def url(self) -> Optional[str]:
        """

        :return: Временная ссылка для скачивания отчета
        :rtype: Optional[str]
        """
        return self.body.get("url")


class ConfirmationCodeResponse(YCBase):
    """

    Информация о коде подтверждения

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
        if code is None:
            raise InputParamError("<code> (=>code) of <ConfirmationCodeResponse> is a required parameter")

        if attempts is not None:
            self.body["attempts"] = validate_fields('attempts', attempts, int)
        if attempts is None:
            raise InputParamError("<attempts> (=>attempts) of <ConfirmationCodeResponse> is a required parameter")

    def __repr__(self):
        return "<ConfirmationCodeResponse>"

    @property
    def code(self) -> str:
        """

        :return: Код подтверждения
        :rtype: str
        """
        return self.body.get("code")

    @property
    def attempts(self) -> int:
        """

        :return: Число оставшихся попыток ввода кода
        :rtype: int
        """
        return self.body.get("attempts")


class CutClaimResponse(YCBase):
    """

    Информация об измененной заявке

    :param str id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)* (741cedf82cd464fa6fa16d87155c636)
    :param str status: Статус заявки *(Обязательный параметр)* (new)

        * **new** - новая заявка
        * **estimating** - идет процесс оценки заявки (подбор типа автомобиля по параметрам груза и расчет стоимости)
        * **estimating_failed** - не удалось оценить заявку. Причину можно увидеть в error_messages в ответе ручки /info
        * **ready_for_approval** - заявка успешно оценена и ожидает подтверждения от клиента
        * **accepted** - заявка подтверждена клиентом
        * **performer_lookup** - заявка взята в обработку. Промежуточный статус перед созданием заказа
        * **performer_draft** - идет поиск водителя
        * **performer_found** - водитель найден и едет в точку А
        * **performer_not_found** - не удалось найти водителя. Можно попробовать снова через некоторое время
        * **pickup_arrived** - водитель приехал на точку А
        * **ready_for_pickup_confirmation** - водитель ждет, когда отправитель назовет ему код подтверждения
        * **pickuped** - водитель успешно забрал груз
        * **delivery_arrived** - водитель приехал на точку Б
        * **ready_for_delivery_confirmation** - водитель ждет, когда получатель назовет ему код подтверждения
        * **pay_waiting** - заказ ожидает оплаты (актуально для оплаты при получении)
        * **delivered** - водитель успешно доставил груз (ввел смс код). Код приходит после оплаты, если была оплата при получении.
        * **delivered_finish** - заказ завершен
        * **returning** -  водителю пришлось вернуть груз и он едет в точку возврата
        * **return_arrived** - водитель приехал на точку возврата
        * **ready_for_return_confirmation** - водитель в точке возврата ожидает, когда ему назовут код подтверждения
        * **returned** - водитель успешно вернул груз (ввел смс код)
        * **returned_finish** - заказ завершен
        * **failed** - терминальный статус, не удалось начать выполнение заказа
        * **cancelled** - заказ был отменен клиентом бесплатно
        * **cancelled_with_payment** - заказ был отменен клиентом платно (водитель уже приехал)
        * **cancelled_by_taxi** - водитель отменил заказ (до получения груза)
        * **cancelled_with_items_on_hands** - клиент платно отменил заявку без необходимости возврата груза (заявка была создана с флагом optional_return)

    :param int version: Версия заявки из запроса *(Обязательный параметр)* (1)
    :param Optional[str] taxi_order_id: taxi_order_id в такси (uuid) (33f95d1a73b84cbcaa06c9ad306dc459)
    """

    def __init__(self,
                 id: str = None,
                 status: str = None,
                 version: int = None,
                 taxi_order_id: Optional[str] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if id is not None:
            self.body["id"] = validate_fields('id', id, str)
        if id is None:
            raise InputParamError("<id> (=>id) of <CutClaimResponse> is a required parameter")

        if status is not None:
            self.body["status"] = validate_fields('status', status, str)
        if status is None:
            raise InputParamError("<status> (=>status) of <CutClaimResponse> is a required parameter")

        if status not in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived',
                          'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning',
                          'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi',
                          'cancelled_with_items_on_hands']:
            raise InputParamError(
                "<status> of <CutClaimResponse> should be in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived', 'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning', 'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi', 'cancelled_with_items_on_hands']")

        if version is not None:
            self.body["version"] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <CutClaimResponse> is a required parameter")

        if taxi_order_id is not None:
            self.body["taxi_order_id"] = validate_fields('taxi_order_id', taxi_order_id, str)

    def __repr__(self):
        return "<CutClaimResponse>"

    @property
    def id(self) -> str:
        """

        :return: Идентификатор заявки, полученный на этапе создания заявки
        :rtype: str
        """
        return self.body.get("id")

    @property
    def status(self) -> str:
        """

        :return: Статус заявки

            * **new** - новая заявка
            * **estimating** - идет процесс оценки заявки (подбор типа автомобиля по параметрам груза и расчет стоимости)
            * **estimating_failed** - не удалось оценить заявку. Причину можно увидеть в error_messages в ответе ручки /info
            * **ready_for_approval** - заявка успешно оценена и ожидает подтверждения от клиента
            * **accepted** - заявка подтверждена клиентом
            * **performer_lookup** - заявка взята в обработку. Промежуточный статус перед созданием заказа
            * **performer_draft** - идет поиск водителя
            * **performer_found** - водитель найден и едет в точку А
            * **performer_not_found** - не удалось найти водителя. Можно попробовать снова через некоторое время
            * **pickup_arrived** - водитель приехал на точку А
            * **ready_for_pickup_confirmation** - водитель ждет, когда отправитель назовет ему код подтверждения
            * **pickuped** - водитель успешно забрал груз
            * **delivery_arrived** - водитель приехал на точку Б
            * **ready_for_delivery_confirmation** - водитель ждет, когда получатель назовет ему код подтверждения
            * **pay_waiting** - заказ ожидает оплаты (актуально для оплаты при получении)
            * **delivered** - водитель успешно доставил груз (ввел смс код). Код приходит после оплаты, если была оплата при получении.
            * **delivered_finish** - заказ завершен
            * **returning** -  водителю пришлось вернуть груз и он едет в точку возврата
            * **return_arrived** - водитель приехал на точку возврата
            * **ready_for_return_confirmation** - водитель в точке возврата ожидает, когда ему назовут код подтверждения
            * **returned** - водитель успешно вернул груз (ввел смс код)
            * **returned_finish** - заказ завершен
            * **failed** - терминальный статус, не удалось начать выполнение заказа
            * **cancelled** - заказ был отменен клиентом бесплатно
            * **cancelled_with_payment** - заказ был отменен клиентом платно (водитель уже приехал)
            * **cancelled_by_taxi** - водитель отменил заказ (до получения груза)
            * **cancelled_with_items_on_hands** - клиент платно отменил заявку без необходимости возврата груза (заявка была создана с флагом optional_return)

        :rtype: str
        """
        return self.body.get("status")

    @property
    def version(self) -> int:
        """

        :return: Версия заявки из запроса
        :rtype: int
        """
        return self.body.get("version")

    @property
    def taxi_order_id(self) -> Optional[str]:
        """

        :return: taxi_order_id в такси (uuid)
        :rtype: Optional[str]
        """
        return self.body.get("taxi_order_id")


class Event(YCBase):
    """

    Информация об изменении заказа

    :param int operation_id: Идентификатор операции *(Обязательный параметр)* (1)
    :param str claim_id: Идентификатор заявки claim_id *(Обязательный параметр)* (3b8d1af142664fde824626a7c19e2bd9)
    :param str change_type: Тип изменения. Возможные значения status_changed — изменение статуса; price_changed — изменение цены *(Обязательный параметр)* (status_changed)
    :param str updated_ts: Время события в формате ISO 8601 *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
    :param str new_status: Статус заявки *(Обязательный параметр)* (new)

        * **new** - новая заявка
        * **estimating** - идет процесс оценки заявки (подбор типа автомобиля по параметрам груза и расчет стоимости)
        * **estimating_failed** - не удалось оценить заявку. Причину можно увидеть в error_messages в ответе ручки /info
        * **ready_for_approval** - заявка успешно оценена и ожидает подтверждения от клиента
        * **accepted** - заявка подтверждена клиентом
        * **performer_lookup** - заявка взята в обработку. Промежуточный статус перед созданием заказа
        * **performer_draft** - идет поиск водителя
        * **performer_found** - водитель найден и едет в точку А
        * **performer_not_found** - не удалось найти водителя. Можно попробовать снова через некоторое время
        * **pickup_arrived** - водитель приехал на точку А
        * **ready_for_pickup_confirmation** - водитель ждет, когда отправитель назовет ему код подтверждения
        * **pickuped** - водитель успешно забрал груз
        * **delivery_arrived** - водитель приехал на точку Б
        * **ready_for_delivery_confirmation** - водитель ждет, когда получатель назовет ему код подтверждения
        * **pay_waiting** - заказ ожидает оплаты (актуально для оплаты при получении)
        * **delivered** - водитель успешно доставил груз (ввел смс код). Код приходит после оплаты, если была оплата при получении.
        * **delivered_finish** - заказ завершен
        * **returning** -  водителю пришлось вернуть груз и он едет в точку возврата
        * **return_arrived** - водитель приехал на точку возврата
        * **ready_for_return_confirmation** - водитель в точке возврата ожидает, когда ему назовут код подтверждения
        * **returned** - водитель успешно вернул груз (ввел смс код)
        * **returned_finish** - заказ завершен
        * **failed** - терминальный статус, не удалось начать выполнение заказа
        * **cancelled** - заказ был отменен клиентом бесплатно
        * **cancelled_with_payment** - заказ был отменен клиентом платно (водитель уже приехал)
        * **cancelled_by_taxi** - водитель отменил заказ (до получения груза)
        * **cancelled_with_items_on_hands** - клиент платно отменил заявку без необходимости возврата груза (заявка была создана с флагом optional_return)

    :param Optional[str] new_price: Цена заказа (20.00)
    :param Optional[str] new_currency: Код валюты заказа (RUB)
    :param Optional[str] resolution: Резолюция терминального статуса (success)

        * **success** - завершился успешно
        * **failed** - завершился с ошибкой

    :param int revision: Версия изменения заявки *(Обязательный параметр)* (1)
    :param Optional[str] client_id: Идентификатор клиента (95d010b2471041499b8cb1bfa282692f)
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
        if operation_id is None:
            raise InputParamError("<operation_id> (=>operation_id) of <Event> is a required parameter")

        if claim_id is not None:
            self.body["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <Event> is a required parameter")

        if change_type is not None:
            self.body["change_type"] = validate_fields('change_type', change_type, str)
        if change_type is None:
            raise InputParamError("<change_type> (=>change_type) of <Event> is a required parameter")

        if updated_ts is not None:
            self.body["updated_ts"] = validate_fields('updated_ts', updated_ts, str)
        if updated_ts is None:
            raise InputParamError("<updated_ts> (=>updated_ts) of <Event> is a required parameter")

        if new_status is not None:
            self.body["new_status"] = validate_fields('new_status', new_status, str)
        if new_status is None:
            raise InputParamError("<new_status> (=>new_status) of <Event> is a required parameter")

        if new_status not in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found',
                              'pickup_arrived', 'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish',
                              'returning', 'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi',
                              'cancelled_with_items_on_hands']:
            raise InputParamError(
                "<new_status> of <Event> should be in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived', 'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning', 'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi', 'cancelled_with_items_on_hands']")

        if new_price is not None:
            self.body["new_price"] = validate_fields('new_price', new_price, str)

        if new_currency is not None:
            self.body["new_currency"] = validate_fields('new_currency', new_currency, str)

        if resolution is not None:
            self.body["resolution"] = validate_fields('resolution', resolution, str)

        if resolution not in ['success', 'failed']:
            raise InputParamError("<resolution> of <Event> should be in ['success', 'failed']")

        if revision is not None:
            self.body["revision"] = validate_fields('revision', revision, int)
        if revision is None:
            raise InputParamError("<revision> (=>revision) of <Event> is a required parameter")

        if client_id is not None:
            self.body["client_id"] = validate_fields('client_id', client_id, str)

    def __repr__(self):
        return "<Event>"

    @property
    def operation_id(self) -> int:
        """

        :return: Идентификатор операции
        :rtype: int
        """
        return self.body.get("operation_id")

    @property
    def claim_id(self) -> str:
        """

        :return: Идентификатор заявки claim_id
        :rtype: str
        """
        return self.body.get("claim_id")

    @property
    def change_type(self) -> str:
        """

        :return: Тип изменения. Возможные значения status_changed — изменение статуса; price_changed — изменение цены
        :rtype: str
        """
        return self.body.get("change_type")

    @property
    def updated_ts(self) -> str:
        """

        :return: Время события в формате ISO 8601
        :rtype: str
        """
        return self.body.get("updated_ts")

    @property
    def new_status(self) -> str:
        """

        :return: Статус заявки

            * **new** - новая заявка
            * **estimating** - идет процесс оценки заявки (подбор типа автомобиля по параметрам груза и расчет стоимости)
            * **estimating_failed** - не удалось оценить заявку. Причину можно увидеть в error_messages в ответе ручки /info
            * **ready_for_approval** - заявка успешно оценена и ожидает подтверждения от клиента
            * **accepted** - заявка подтверждена клиентом
            * **performer_lookup** - заявка взята в обработку. Промежуточный статус перед созданием заказа
            * **performer_draft** - идет поиск водителя
            * **performer_found** - водитель найден и едет в точку А
            * **performer_not_found** - не удалось найти водителя. Можно попробовать снова через некоторое время
            * **pickup_arrived** - водитель приехал на точку А
            * **ready_for_pickup_confirmation** - водитель ждет, когда отправитель назовет ему код подтверждения
            * **pickuped** - водитель успешно забрал груз
            * **delivery_arrived** - водитель приехал на точку Б
            * **ready_for_delivery_confirmation** - водитель ждет, когда получатель назовет ему код подтверждения
            * **pay_waiting** - заказ ожидает оплаты (актуально для оплаты при получении)
            * **delivered** - водитель успешно доставил груз (ввел смс код). Код приходит после оплаты, если была оплата при получении.
            * **delivered_finish** - заказ завершен
            * **returning** -  водителю пришлось вернуть груз и он едет в точку возврата
            * **return_arrived** - водитель приехал на точку возврата
            * **ready_for_return_confirmation** - водитель в точке возврата ожидает, когда ему назовут код подтверждения
            * **returned** - водитель успешно вернул груз (ввел смс код)
            * **returned_finish** - заказ завершен
            * **failed** - терминальный статус, не удалось начать выполнение заказа
            * **cancelled** - заказ был отменен клиентом бесплатно
            * **cancelled_with_payment** - заказ был отменен клиентом платно (водитель уже приехал)
            * **cancelled_by_taxi** - водитель отменил заказ (до получения груза)
            * **cancelled_with_items_on_hands** - клиент платно отменил заявку без необходимости возврата груза (заявка была создана с флагом optional_return)

        :rtype: str
        """
        return self.body.get("new_status")

    @property
    def new_price(self) -> Optional[str]:
        """

        :return: Цена заказа
        :rtype: Optional[str]
        """
        return self.body.get("new_price")

    @property
    def new_currency(self) -> Optional[str]:
        """

        :return: Код валюты заказа
        :rtype: Optional[str]
        """
        return self.body.get("new_currency")

    @property
    def resolution(self) -> Optional[str]:
        """

        :return: Резолюция терминального статуса

            * **success** - завершился успешно
            * **failed** - завершился с ошибкой

        :rtype: Optional[str]
        """
        return self.body.get("resolution")

    @property
    def revision(self) -> int:
        """

        :return: Версия изменения заявки
        :rtype: int
        """
        return self.body.get("revision")

    @property
    def client_id(self) -> Optional[str]:
        """

        :return: Идентификатор клиента
        :rtype: Optional[str]
        """
        return self.body.get("client_id")


class HumanErrorMessage(YCBase):
    """

    Информация о человеко-понятной ошибке

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
        if code is None:
            raise InputParamError("<code> (=>code) of <HumanErrorMessage> is a required parameter")

        if message is not None:
            self.body["message"] = validate_fields('message', message, str)
        if message is None:
            raise InputParamError("<message> (=>message) of <HumanErrorMessage> is a required parameter")

    def __repr__(self):
        return "<HumanErrorMessage>"

    @property
    def code(self) -> str:
        """

        :return: Машино-понятный код ошибки
        :rtype: str
        """
        return self.body.get("code")

    @property
    def message(self) -> str:
        """

        :return: Человеко-понятный локализованный текст ошибки
        :rtype: str
        """
        return self.body.get("message")


class MatchedCar(YCBase):
    """

    Информация о подобранной машине

    :param str taxi_class: Класс такси. Возможные значения courier, express, cargo *(Обязательный параметр)* (express)
    :param Optional[str] client_taxi_class: Подмененный тариф (e.g., cargo, хотя в cars cargocorp)  (cargo)
    :param Optional[str] cargo_type: Тип грузовика (lcv_m)
    :param Optional[int] cargo_type_int: Тип грузовика (2 is equal to "lcv_m")
    :param Optional[int] cargo_loaders: Требуемое число грузчиков
    :param Optional[bool] door_to_door: Опция "от двери до двери" для тарифа "доставка"
    """

    def __init__(self,
                 taxi_class: str = None,
                 client_taxi_class: Optional[str] = None,
                 cargo_type: Optional[str] = None,
                 cargo_type_int: Optional[int] = None,
                 cargo_loaders: Optional[int] = None,
                 door_to_door: Optional[bool] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if taxi_class is not None:
            self.body["taxi_class"] = validate_fields('taxi_class', taxi_class, str)
        if taxi_class is None:
            raise InputParamError("<taxi_class> (=>taxi_class) of <MatchedCar> is a required parameter")

        if client_taxi_class is not None:
            self.body["client_taxi_class"] = validate_fields('client_taxi_class', client_taxi_class, str)

        if cargo_type is not None:
            self.body["cargo_type"] = validate_fields('cargo_type', cargo_type, str)

        if cargo_type_int is not None:
            self.body["cargo_type_int"] = validate_fields('cargo_type_int', cargo_type_int, int)

        if cargo_loaders is not None:
            self.body["cargo_loaders"] = validate_fields('cargo_loaders', cargo_loaders, int)
        if cargo_loaders and cargo_loaders < 0:
            raise InputParamError("<cargo_loaders> of <MatchedCar> should be more than 0")

        if door_to_door is not None:
            self.body["door_to_door"] = validate_fields('door_to_door', door_to_door, bool)

    def __repr__(self):
        return "<MatchedCar>"

    @property
    def taxi_class(self) -> str:
        """

        :return: Класс такси. Возможные значения courier, express, cargo
        :rtype: str
        """
        return self.body.get("taxi_class")

    @property
    def client_taxi_class(self) -> Optional[str]:
        """

        :return: Подмененный тариф (e.g., cargo, хотя в cars cargocorp)
        :rtype: Optional[str]
        """
        return self.body.get("client_taxi_class")

    @property
    def cargo_type(self) -> Optional[str]:
        """

        :return: Тип грузовика
        :rtype: Optional[str]
        """
        return self.body.get("cargo_type")

    @property
    def cargo_type_int(self) -> Optional[int]:
        """

        :return: Тип грузовика
        :rtype: Optional[int]
        """
        return self.body.get("cargo_type_int")

    @property
    def cargo_loaders(self) -> Optional[int]:
        """

        :return: Требуемое число грузчиков
        :rtype: Optional[int]
        """
        return self.body.get("cargo_loaders")

    @property
    def door_to_door(self) -> Optional[bool]:
        """

        :return: Опция "от двери до двери" для тарифа "доставка"
        :rtype: Optional[bool]
        """
        return self.body.get("door_to_door")


class PerformerPositionResponse(YCBase):
    """

    Информация о позиции исполнителя

    :param float position_lat: Широта *(Обязательный параметр)*
    :param float position_lon: Долгота *(Обязательный параметр)*
    :param int position_timestamp: Время снятия сигнала GPS, unix-time *(Обязательный параметр)*
    :param Optional[float] position_accuracy: Точность GPS. Пока запрещена к передаче т.к. не решили с единицами измерения.
    :param Optional[float] position_speed: Средняя скорость, в м/с
    :param Optional[float] position_direction: Направление. Угол от 0 градусов до 360 градусов от направления на север, по часовой стрелке. 0 - север, 90 - восток, 180 - юг, 270 - запад.
    """

    def __init__(self,
                 position_lat: float = None,
                 position_lon: float = None,
                 position_timestamp: int = None,
                 position_accuracy: Optional[float] = None,
                 position_speed: Optional[float] = None,
                 position_direction: Optional[float] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if position_lat is not None:
            self.body["position"]["lat"] = validate_fields('position_lat', position_lat, float)
        if position_lat and position_lat < -90:
            raise InputParamError("<position_lat> of <PerformerPositionResponse> should be more than -90")
        if position_lat and position_lat > 90:
            raise InputParamError("<position_lat> of <PerformerPositionResponse> should be less than 90")
        if position_lat is None:
            raise InputParamError("<position_lat> (position=>lat) of <PerformerPositionResponse> is a required parameter")

        if position_lon is not None:
            self.body["position"]["lon"] = validate_fields('position_lon', position_lon, float)
        if position_lon and position_lon < -180:
            raise InputParamError("<position_lon> of <PerformerPositionResponse> should be more than -180")
        if position_lon and position_lon > 180:
            raise InputParamError("<position_lon> of <PerformerPositionResponse> should be less than 180")
        if position_lon is None:
            raise InputParamError("<position_lon> (position=>lon) of <PerformerPositionResponse> is a required parameter")

        if position_timestamp is not None:
            self.body["position"]["timestamp"] = validate_fields('position_timestamp', position_timestamp, int)
        if position_timestamp is None:
            raise InputParamError("<position_timestamp> (position=>timestamp) of <PerformerPositionResponse> is a required parameter")

        if position_accuracy is not None:
            self.body["position"]["accuracy"] = validate_fields('position_accuracy', position_accuracy, float)

        if position_speed is not None:
            self.body["position"]["speed"] = validate_fields('position_speed', position_speed, float)

        if position_direction is not None:
            self.body["position"]["direction"] = validate_fields('position_direction', position_direction, float)

    def __repr__(self):
        return "<PerformerPositionResponse>"

    @property
    def position_lat(self) -> float:
        """

        :return: Широта
        :rtype: float
        """
        return self.body.get("position_lat")

    @property
    def position_lon(self) -> float:
        """

        :return: Долгота
        :rtype: float
        """
        return self.body.get("position_lon")

    @property
    def position_timestamp(self) -> int:
        """

        :return: Время снятия сигнала GPS, unix-time
        :rtype: int
        """
        return self.body.get("position_timestamp")

    @property
    def position_accuracy(self) -> Optional[float]:
        """

        :return: Точность GPS. Пока запрещена к передаче т.к. не решили с единицами измерения.
        :rtype: Optional[float]
        """
        return self.body.get("position_accuracy")

    @property
    def position_speed(self) -> Optional[float]:
        """

        :return: Средняя скорость, в м/с
        :rtype: Optional[float]
        """
        return self.body.get("position_speed")

    @property
    def position_direction(self) -> Optional[float]:
        """

        :return: Направление. Угол от 0 градусов до 360 градусов от направления на север, по часовой стрелке. 0 - север, 90 - восток, 180 - юг, 270 - запад.
        :rtype: Optional[float]
        """
        return self.body.get("position_direction")


class ResponseCargoPointMP(YCBase):
    """

    Описание точки в заявке с мультиточками

    :param int id: Целочисленный идентификатор точки *(Обязательный параметр)* (1)
    :param str contact_name: Имя контактного лица *(Обязательный параметр)* (Морти)
    :param str contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999998)
    :param Optional[str] contact_email: Email — обязательный параметр для точек source и return (morty@yandex.ru)
    :param str address_fullname: Полное название с указанием города (Москва, Садовническая набережная, 82с2, БЦ Аврора) *(Обязательный параметр)* (Санкт-Петербург, Большая Монетная улица, 1к1А)
    :param Optional[str] address_shortname: Адрес в пределах города, как показывается на Таксометре (Садовническая набережная, 82с2, БЦ Аврора) (Большая Монетная улица, 1к1А)
    :param List['float'] address_coordinates: Массив из двух вещественных чисел [долгота, широта]. Порядок важен! *(Обязательный параметр)*
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
    :param Optional[str] address_comment: Комментарий для курьера Для точки А (откуда забрать отправление) используйте шаблон: "Доставка из магазина <>. Сообщите менеджеру, что заказ по доставке Яндекс.Такси. Назовите номер заказа <> и заберите посылку. Заказ оплачен безналично, при передаче заказа нельзя требовать с получателя деньги за доставку." Для точек Б (куда доставить) в комментарий передавайте пожелания получателя. Например "домофон не работает" / "шлагбаум закрыт, позвонить за 10 минут" / "не звонить, спит ребенок".  (Домофон не работает)
    :param Optional[str] address_uri: Карточный uri геообъекта (ymapsbm1://geo?ll=38.805%2C55.084)
    :param str type: Тип точки *(Обязательный параметр)* (source)

        * **source** — точка получения отправления (ровно одна)
        * **destination** — точка доставки отправления
        * **return** — точка возврата части товаров, опциональная (не более одной)

    :param int visit_order: Порядок посещения точки *(Обязательный параметр)* (1)
    :param str visit_status: Статус посещения данной точки pending - точка еще не посещена arrived - водитель прибыл на точку visited - водитель передал/забрал груз на точке skipped - точка пропущена (в случае возврата, когда клиент не смог принять груз) *(Обязательный параметр)* (pending)

        * **pending** - ждет исполнения
        * **arrived** - курьер прибыл на точку, но еще не передал/забрал товар
        * **visited** - передали/забрали товар из точки
        * **skipped** - возврат (то есть клиент в этой точке не принял посылку и ее повезут в точку возврата. не значит, что товар уже вернули на склад)

    :param Optional[bool] skip_confirmation: Пропускать подтверждение через SMS в данной точке
    :param str payment_on_delivery_client_order_id: Идентификатор заказа *(Обязательный параметр)* (100)
    :param bool payment_on_delivery_is_paid: Признак оплаты заказа *(Обязательный параметр)*
    :param str payment_on_delivery_cost: Цена Decimal(19, 4) *(Обязательный параметр)* (12.50)
    :param Optional[str] payment_on_delivery_customer_full_name: Для юридического лица — название организации, для ИП и физического лица — ФИО (Morty)
    :param Optional[str] payment_on_delivery_customer_inn: ИНН пользователя (10 или 12 цифр) (3664069397)
    :param Optional[str] payment_on_delivery_customer_email: Электронная почта пользователя. Если не указано, будет использована почта получателя из точки (morty@yandex.ru)
    :param Optional[str] payment_on_delivery_customer_phone: Телефон пользователя. Если не указано, будет использован телефон получателя из точки (79000000000)
    :param Optional[int] payment_on_delivery_tax_system_code: Система налогообложения магазина (1)

        * **1** - Общая система налогообложения
        * **2** - Упрощенная (УСН, доходы)
        * **3** - Упрощенная (УСН, доходы минус расходы)
        * **4** - Единый налог на вмененный доход (ЕНВД)
        * **5** - Единый сельскохозяйственный налог (ЕСН)
        * **6** - Патентная система налогообложения

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
                 address_coordinates: List['float'] = None,
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
        if id is None:
            raise InputParamError("<id> (=>id) of <ResponseCargoPointMP> is a required parameter")

        if contact_name is not None:
            self.body["contact"]["name"] = validate_fields('contact_name', contact_name, str)
        if contact_name is None:
            raise InputParamError("<contact_name> (contact=>name) of <ResponseCargoPointMP> is a required parameter")

        if contact_phone is not None:
            self.body["contact"]["phone"] = validate_fields('contact_phone', contact_phone, str)
        if contact_phone is None:
            raise InputParamError("<contact_phone> (contact=>phone) of <ResponseCargoPointMP> is a required parameter")

        if contact_email is not None:
            self.body["contact"]["email"] = validate_fields('contact_email', contact_email, str)

        if address_fullname is not None:
            self.body["address"]["fullname"] = validate_fields('address_fullname', address_fullname, str)
        if address_fullname is None:
            raise InputParamError("<address_fullname> (address=>fullname) of <ResponseCargoPointMP> is a required parameter")

        if address_shortname is not None:
            self.body["address"]["shortname"] = validate_fields('address_shortname', address_shortname, str)

        if address_coordinates is not None:
            self.body["address"]["coordinates"] = validate_fields('address_coordinates', address_coordinates, List['float'])
        if address_coordinates and len(address_coordinates) < 2:
            raise InputParamError("<address_coordinates> of <ResponseCargoPointMP> should contain at least 2 element")
        if address_coordinates and len(address_coordinates) > 2:
            raise InputParamError("<address_coordinates> of <ResponseCargoPointMP> should not contain more than 2 element")
        if address_coordinates is None:
            raise InputParamError("<address_coordinates> (address=>coordinates) of <ResponseCargoPointMP> is a required parameter")

        if address_country is not None:
            self.body["address"]["country"] = validate_fields('address_country', address_country, str)

        if address_city is not None:
            self.body["address"]["city"] = validate_fields('address_city', address_city, str)

        if address_street is not None:
            self.body["address"]["street"] = validate_fields('address_street', address_street, str)

        if address_building is not None:
            self.body["address"]["building"] = validate_fields('address_building', address_building, str)

        if address_porch is not None:
            self.body["address"]["porch"] = validate_fields('address_porch', address_porch, str)

        if address_floor is not None:
            self.body["address"]["floor"] = validate_fields('address_floor', address_floor, int)

        if address_flat is not None:
            self.body["address"]["flat"] = validate_fields('address_flat', address_flat, int)

        if address_sfloor is not None:
            self.body["address"]["sfloor"] = validate_fields('address_sfloor', address_sfloor, str)

        if address_sflat is not None:
            self.body["address"]["sflat"] = validate_fields('address_sflat', address_sflat, str)

        if address_door_code is not None:
            self.body["address"]["door_code"] = validate_fields('address_door_code', address_door_code, str)

        if address_comment is not None:
            self.body["address"]["comment"] = validate_fields('address_comment', address_comment, str)

        if address_uri is not None:
            self.body["address"]["uri"] = validate_fields('address_uri', address_uri, str)

        if type is not None:
            self.body["type"] = validate_fields('type', type, str)
        if type is None:
            raise InputParamError("<type> (=>type) of <ResponseCargoPointMP> is a required parameter")

        if type not in ['source', 'destination', 'return']:
            raise InputParamError("<type> of <ResponseCargoPointMP> should be in ['source', 'destination', 'return']")

        if visit_order is not None:
            self.body["visit_order"] = validate_fields('visit_order', visit_order, int)
        if visit_order is None:
            raise InputParamError("<visit_order> (=>visit_order) of <ResponseCargoPointMP> is a required parameter")

        if visit_status is not None:
            self.body["visit_status"] = validate_fields('visit_status', visit_status, str)
        if visit_status is None:
            raise InputParamError("<visit_status> (=>visit_status) of <ResponseCargoPointMP> is a required parameter")

        if visit_status not in ['pending', 'arrived', 'visited', 'skipped']:
            raise InputParamError("<visit_status> of <ResponseCargoPointMP> should be in ['pending', 'arrived', 'visited', 'skipped']")

        if skip_confirmation is not None:
            self.body["skip_confirmation"] = validate_fields('skip_confirmation', skip_confirmation, bool)

        if payment_on_delivery_client_order_id is not None:
            self.body["payment_on_delivery"]["client_order_id"] = validate_fields('payment_on_delivery_client_order_id', payment_on_delivery_client_order_id, str)
        if payment_on_delivery_client_order_id is None:
            raise InputParamError("<payment_on_delivery_client_order_id> (payment_on_delivery=>client_order_id) of <ResponseCargoPointMP> is a required parameter")

        if payment_on_delivery_is_paid is not None:
            self.body["payment_on_delivery"]["is_paid"] = validate_fields('payment_on_delivery_is_paid', payment_on_delivery_is_paid, bool)
        if payment_on_delivery_is_paid is None:
            raise InputParamError("<payment_on_delivery_is_paid> (payment_on_delivery=>is_paid) of <ResponseCargoPointMP> is a required parameter")

        if payment_on_delivery_cost is not None:
            self.body["payment_on_delivery"]["cost"] = validate_fields('payment_on_delivery_cost', payment_on_delivery_cost, str)
        if payment_on_delivery_cost is None:
            raise InputParamError("<payment_on_delivery_cost> (payment_on_delivery=>cost) of <ResponseCargoPointMP> is a required parameter")

        if payment_on_delivery_customer_full_name is not None:
            self.body["payment_on_delivery"]["customer"]["full_name"] = validate_fields('payment_on_delivery_customer_full_name', payment_on_delivery_customer_full_name, str)

        if payment_on_delivery_customer_inn is not None:
            self.body["payment_on_delivery"]["customer"]["inn"] = validate_fields('payment_on_delivery_customer_inn', payment_on_delivery_customer_inn, str)

        if payment_on_delivery_customer_email is not None:
            self.body["payment_on_delivery"]["customer"]["email"] = validate_fields('payment_on_delivery_customer_email', payment_on_delivery_customer_email, str)

        if payment_on_delivery_customer_phone is not None:
            self.body["payment_on_delivery"]["customer"]["phone"] = validate_fields('payment_on_delivery_customer_phone', payment_on_delivery_customer_phone, str)

        if payment_on_delivery_tax_system_code is not None:
            self.body["payment_on_delivery"]["tax_system_code"] = validate_fields('payment_on_delivery_tax_system_code', payment_on_delivery_tax_system_code, int)
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code < 1:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <ResponseCargoPointMP> should be more than 1")
        if payment_on_delivery_tax_system_code and payment_on_delivery_tax_system_code > 6:
            raise InputParamError("<payment_on_delivery_tax_system_code> of <ResponseCargoPointMP> should be less than 6")

        if external_order_id is not None:
            self.body["external_order_id"] = validate_fields('external_order_id', external_order_id, str)

        if pickup_code is not None:
            self.body["pickup_code"] = validate_fields('pickup_code', pickup_code, str)

    def __repr__(self):
        return "<ResponseCargoPointMP>"

    @property
    def id(self) -> int:
        """

        :return: Целочисленный идентификатор точки
        :rtype: int
        """
        return self.body.get("id")

    @property
    def contact_name(self) -> str:
        """

        :return: Имя контактного лица
        :rtype: str
        """
        return self.body.get("contact_name")

    @property
    def contact_phone(self) -> str:
        """

        :return: Телефон контактного лица
        :rtype: str
        """
        return self.body.get("contact_phone")

    @property
    def contact_email(self) -> Optional[str]:
        """

        :return: Email — обязательный параметр для точек source и return
        :rtype: Optional[str]
        """
        return self.body.get("contact_email")

    @property
    def address_fullname(self) -> str:
        """

        :return: Полное название с указанием города (Москва, Садовническая набережная, 82с2, БЦ Аврора)
        :rtype: str
        """
        return self.body.get("address_fullname")

    @property
    def address_shortname(self) -> Optional[str]:
        """

        :return: Адрес в пределах города, как показывается на Таксометре (Садовническая набережная, 82с2, БЦ Аврора)
        :rtype: Optional[str]
        """
        return self.body.get("address_shortname")

    @property
    def address_coordinates(self) -> List['float']:
        """

        :return: Массив из двух вещественных чисел [долгота, широта]. Порядок важен!
        :rtype: List['float']
        """
        return [item for item in self.body.get("address_coordinates")]

    @property
    def address_country(self) -> Optional[str]:
        """

        :return: Страна
        :rtype: Optional[str]
        """
        return self.body.get("address_country")

    @property
    def address_city(self) -> Optional[str]:
        """

        :return: Город
        :rtype: Optional[str]
        """
        return self.body.get("address_city")

    @property
    def address_street(self) -> Optional[str]:
        """

        :return: Улица
        :rtype: Optional[str]
        """
        return self.body.get("address_street")

    @property
    def address_building(self) -> Optional[str]:
        """

        :return: Строение
        :rtype: Optional[str]
        """
        return self.body.get("address_building")

    @property
    def address_porch(self) -> Optional[str]:
        """

        :return: Подъезд (может быть A)
        :rtype: Optional[str]
        """
        return self.body.get("address_porch")

    @property
    def address_floor(self) -> Optional[int]:
        """

        :return: Этаж (DEPRECATED)
        :rtype: Optional[int]
        """
        return self.body.get("address_floor")

    @property
    def address_flat(self) -> Optional[int]:
        """

        :return: Квартира (DEPRECATED)
        :rtype: Optional[int]
        """
        return self.body.get("address_flat")

    @property
    def address_sfloor(self) -> Optional[str]:
        """

        :return: Этаж
        :rtype: Optional[str]
        """
        return self.body.get("address_sfloor")

    @property
    def address_sflat(self) -> Optional[str]:
        """

        :return: Квартира
        :rtype: Optional[str]
        """
        return self.body.get("address_sflat")

    @property
    def address_door_code(self) -> Optional[str]:
        """

        :return: Код домофона
        :rtype: Optional[str]
        """
        return self.body.get("address_door_code")

    @property
    def address_comment(self) -> Optional[str]:
        """

        :return: Комментарий для курьера Для точки А (откуда забрать отправление) используйте шаблон: "Доставка из магазина <>. Сообщите менеджеру, что заказ по доставке Яндекс.Такси. Назовите номер заказа <> и заберите посылку. Заказ оплачен безналично, при передаче заказа нельзя требовать с получателя деньги за доставку." Для точек Б (куда доставить) в комментарий передавайте пожелания получателя. Например "домофон не работает" / "шлагбаум закрыт, позвонить за 10 минут" / "не звонить, спит ребенок".
        :rtype: Optional[str]
        """
        return self.body.get("address_comment")

    @property
    def address_uri(self) -> Optional[str]:
        """

        :return: Карточный uri геообъекта
        :rtype: Optional[str]
        """
        return self.body.get("address_uri")

    @property
    def type(self) -> str:
        """

        :return: Тип точки

            * **source** — точка получения отправления (ровно одна)
            * **destination** — точка доставки отправления
            * **return** — точка возврата части товаров, опциональная (не более одной)

        :rtype: str
        """
        return self.body.get("type")

    @property
    def visit_order(self) -> int:
        """

        :return: Порядок посещения точки
        :rtype: int
        """
        return self.body.get("visit_order")

    @property
    def visit_status(self) -> str:
        """

        :return: Статус посещения данной точки pending - точка еще не посещена arrived - водитель прибыл на точку visited - водитель передал/забрал груз на точке skipped - точка пропущена (в случае возврата, когда клиент не смог принять груз)

            * **pending** - ждет исполнения
            * **arrived** - курьер прибыл на точку, но еще не передал/забрал товар
            * **visited** - передали/забрали товар из точки
            * **skipped** - возврат (то есть клиент в этой точке не принял посылку и ее повезут в точку возврата. не значит, что товар уже вернули на склад)

        :rtype: str
        """
        return self.body.get("visit_status")

    @property
    def skip_confirmation(self) -> Optional[bool]:
        """

        :return: Пропускать подтверждение через SMS в данной точке
        :rtype: Optional[bool]
        """
        return self.body.get("skip_confirmation")

    @property
    def payment_on_delivery_client_order_id(self) -> str:
        """

        :return: Идентификатор заказа
        :rtype: str
        """
        return self.body.get("payment_on_delivery_client_order_id")

    @property
    def payment_on_delivery_is_paid(self) -> bool:
        """

        :return: Признак оплаты заказа
        :rtype: bool
        """
        return self.body.get("payment_on_delivery_is_paid")

    @property
    def payment_on_delivery_cost(self) -> str:
        """

        :return: Цена Decimal(19, 4)
        :rtype: str
        """
        return self.body.get("payment_on_delivery_cost")

    @property
    def payment_on_delivery_customer_full_name(self) -> Optional[str]:
        """

        :return: Для юридического лица — название организации, для ИП и физического лица — ФИО
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_full_name")

    @property
    def payment_on_delivery_customer_inn(self) -> Optional[str]:
        """

        :return: ИНН пользователя (10 или 12 цифр)
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_inn")

    @property
    def payment_on_delivery_customer_email(self) -> Optional[str]:
        """

        :return: Электронная почта пользователя. Если не указано, будет использована почта получателя из точки
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_email")

    @property
    def payment_on_delivery_customer_phone(self) -> Optional[str]:
        """

        :return: Телефон пользователя. Если не указано, будет использован телефон получателя из точки
        :rtype: Optional[str]
        """
        return self.body.get("payment_on_delivery_customer_phone")

    @property
    def payment_on_delivery_tax_system_code(self) -> Optional[int]:
        """

        :return: Система налогообложения магазина

        * **1** - Общая система налогообложения
        * **2** - Упрощенная (УСН, доходы)
        * **3** - Упрощенная (УСН, доходы минус расходы)
        * **4** - Единый налог на вмененный доход (ЕНВД)
        * **5** - Единый сельскохозяйственный налог (ЕСН)
        * **6** - Патентная система налогообложения

        :rtype: Optional[int]
        """
        return self.body.get("payment_on_delivery_tax_system_code")

    @property
    def external_order_id(self) -> Optional[str]:
        """

        :return: Номер заказа клиента
        :rtype: Optional[str]
        """
        return self.body.get("external_order_id")

    @property
    def pickup_code(self) -> Optional[str]:
        """

        :return: Код выдачи товара (ПВЗ)
        :rtype: Optional[str]
        """
        return self.body.get("pickup_code")


class SearchClaimsResponseMP(YCBase):
    """

    Информация о результатах поиска

    :param List['SearchedClaimMP'] claims: Список найденных заявок *(Обязательный параметр)*
    """

    def __init__(self,
                 claims: List['SearchedClaimMP'] = None,
                 ):
        self.body = collections.defaultdict(dict)

        if claims is not None:
            self.body["claims"] = validate_fields('claims', claims, List['SearchedClaimMP'])
        if claims is None:
            raise InputParamError("<claims> (=>claims) of <SearchClaimsResponseMP> is a required parameter")

    def __repr__(self):
        return "<SearchClaimsResponseMP>"

    @property
    def claims(self) -> List['SearchedClaimMP']:
        """

        :return: Список найденных заявок
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
                                revision=item.get("revision", None),
                                ) for item in self.body.get("claims")]


class SearchedClaimMP(YCBase):
    """

    Информация о заявке

    :param str id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)* (741cedf82cd464fa6fa16d87155c636)
    :param Optional[str] corp_client_id: Идентификатор корпоративного клиента (из OAuth токена) (cd8cc018bde34597932855e3cfdce927)
    :param Optional[str] yandex_uid: yandex uid (3a4e06e733a3433880e4900ffeaf7b62)
    :param List['CargoItemMP'] items: Перечисление наименований грузов для отправления *(Обязательный параметр)*
    :param List['ResponseCargoPointMP'] route_points: Информация по точкам маршрута *(Обязательный параметр)*
    :param int current_point_id: Целочисленный идентификатор точки *(Обязательный параметр)* (6987)
    :param str status: Статус заявки *(Обязательный параметр)* (new)

        * **new** - новая заявка
        * **estimating** - идет процесс оценки заявки (подбор типа автомобиля по параметрам груза и расчет стоимости)
        * **estimating_failed** - не удалось оценить заявку. Причину можно увидеть в error_messages в ответе ручки /info
        * **ready_for_approval** - заявка успешно оценена и ожидает подтверждения от клиента
        * **accepted** - заявка подтверждена клиентом
        * **performer_lookup** - заявка взята в обработку. Промежуточный статус перед созданием заказа
        * **performer_draft** - идет поиск водителя
        * **performer_found** - водитель найден и едет в точку А
        * **performer_not_found** - не удалось найти водителя. Можно попробовать снова через некоторое время
        * **pickup_arrived** - водитель приехал на точку А
        * **ready_for_pickup_confirmation** - водитель ждет, когда отправитель назовет ему код подтверждения
        * **pickuped** - водитель успешно забрал груз
        * **delivery_arrived** - водитель приехал на точку Б
        * **ready_for_delivery_confirmation** - водитель ждет, когда получатель назовет ему код подтверждения
        * **pay_waiting** - заказ ожидает оплаты (актуально для оплаты при получении)
        * **delivered** - водитель успешно доставил груз (ввел смс код). Код приходит после оплаты, если была оплата при получении.
        * **delivered_finish** - заказ завершен
        * **returning** -  водителю пришлось вернуть груз и он едет в точку возврата
        * **return_arrived** - водитель приехал на точку возврата
        * **ready_for_return_confirmation** - водитель в точке возврата ожидает, когда ему назовут код подтверждения
        * **returned** - водитель успешно вернул груз (ввел смс код)
        * **returned_finish** - заказ завершен
        * **failed** - терминальный статус, не удалось начать выполнение заказа
        * **cancelled** - заказ был отменен клиентом бесплатно
        * **cancelled_with_payment** - заказ был отменен клиентом платно (водитель уже приехал)
        * **cancelled_by_taxi** - водитель отменил заказ (до получения груза)
        * **cancelled_with_items_on_hands** - клиент платно отменил заявку без необходимости возврата груза (заявка была создана с флагом optional_return)

    :param int version: Версия *(Обязательный параметр)*
    :param Optional[List['HumanErrorMessage']] error_messages: Список сообщений об ошибках
    :param str emergency_contact_name: Имя контактного лица *(Обязательный параметр)* (Рик)
    :param str emergency_contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999999)
    :param Optional[bool] skip_door_to_door: Отказ от доставки до двери. В случае true — курьер доставит заказ только на улицу, до подъезда
    :param Optional[bool] skip_client_notify: Не отправлять получателю нотификации, когда к нему направится курьер
    :param Optional[bool] skip_emergency_notify: Не отправлять нотификации emergency контакту
    :param Optional[bool] skip_act: Не показывать акт
    :param Optional[bool] optional_return: Не требуется возврат товаров в случае отмены заказа. В случае true — курьер оставляет товар себе
    :param Optional[int] eta: Ожидаемое время исполнения заказа в минутах (10)
    :param str created_ts: Дата-время создания *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
    :param str updated_ts: Дата-время последнего обновления *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
    :param str taxi_offer_offer_id: Идентификатор предложения *(Обязательный параметр)* (28ae5f1d72364468be3f5e26cd6a66bf)
    :param int taxi_offer_price_raw: (deprecated) Цена по офферу в валюте, указанной в договоре *(Обязательный параметр)* (12)
    :param str taxi_offer_price: Цена Decimal(19, 4) *(Обязательный параметр)* (12.50)
    :param str pricing_offer_offer_id: Идентификатор предложения *(Обязательный параметр)* (28ae5f1d72364468be3f5e26cd6a66bf)
    :param int pricing_offer_price_raw: (deprecated) Цена по предложению в валюте, указанной в договоре *(Обязательный параметр)* (12)
    :param str pricing_offer_price: Цена Decimal(19, 4) *(Обязательный параметр)* (12.50)
    :param Optional[str] pricing_currency: Трехзначный код валюты, в которой ведется расчет (RUB)
    :param str pricing_currency_rules_code: Трехзначный код валюты, в которой ведется расчет *(Обязательный параметр)* (RUB)
    :param str pricing_currency_rules_text: Сокращенное наименование валюты *(Обязательный параметр)* (руб.)
    :param str pricing_currency_rules_template: Шаблон *(Обязательный параметр)* ($VALUE$ $SIGN$$CURRENCY$)
    :param Optional[str] pricing_currency_rules_sign: Символ валюты (₽)
    :param str pricing_final_price: Цена Decimal(19, 4) *(Обязательный параметр)* (12.50)
    :param Optional[str] available_cancel_state: Признак возможности платной/бесплатной отмены (free)

        * **free** - платная отмена
        * **paid** - бесплатная отмена

    :param str client_requirements_taxi_class: Класс такси. Возможные значения courier, express, cargo. *(Обязательный параметр)* (express)
    :param Optional[str] client_requirements_cargo_type: Тип грузовика (lcv_m)
    :param Optional[int] client_requirements_cargo_loaders: Требуемое число грузчиков
    :param Optional[List['str']] client_requirements_cargo_options: Дополнительные опции тарифа
    :param Optional[List['MatchedCar']] matched_cars: Информация об исполнителе (массив, на данный момент всегда 1 элемент)
    :param Optional[List['ClaimWarning']] warnings: Предупреждения по циклу заявки
    :param str performer_info_courier_name: Имя курьера, доставляющего посылку *(Обязательный параметр)* (Личность)
    :param str performer_info_legal_name: Данные о юридическом лице, которое осуществляет доставку *(Обязательный параметр)* (ИП Птичья личность)
    :param Optional[str] performer_info_car_model: Модель машины (Hyundai Solaris)
    :param Optional[str] performer_info_car_number: Номер машины (А100РА100)
    :param str callback_properties_callback_url: URL, который будет вызываться при смене статусов по заявке.  Данный механизм устарел, вместо него следует использовать операцию v1/claims/journal.  *(Обязательный параметр)* (https://www.example.com)
    :param Optional[str] due: Создать заказ к определенному времени (например, заказ на завтра). Согласуйте с менеджером использование опции! (2020-01-01T00:00:00+00:00)
    :param Optional[str] shipping_document: Сопроводительные документы
    :param Optional[str] comment: Общий комментарий к заказу (Ресторан)
    :param int revision: ??? *(Обязательный параметр)* (1)
    """

    def __init__(self,
                 id: str = None,
                 corp_client_id: Optional[str] = None,
                 yandex_uid: Optional[str] = None,
                 items: List['CargoItemMP'] = None,
                 route_points: List['ResponseCargoPointMP'] = None,
                 current_point_id: int = None,
                 status: str = None,
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
                 taxi_offer_price: str = None,
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
                 revision: int = None,
                 ):
        self.body = collections.defaultdict(dict)

        if id is not None:
            self.body["id"] = validate_fields('id', id, str)
        if id is None:
            raise InputParamError("<id> (=>id) of <SearchedClaimMP> is a required parameter")

        if corp_client_id is not None:
            self.body["corp_client_id"] = validate_fields('corp_client_id', corp_client_id, str)
        if corp_client_id and len(corp_client_id) < 32:
            raise InputParamError("<corp_client_id> of <SearchedClaimMP> should contain at least 32 element")
        if corp_client_id and len(corp_client_id) > 32:
            raise InputParamError("<corp_client_id> of <SearchedClaimMP> should not contain more than 32 element")

        if yandex_uid is not None:
            self.body["yandex_uid"] = validate_fields('yandex_uid', yandex_uid, str)

        if items is not None:
            self.body["items"] = validate_fields('items', items, List['CargoItemMP'])
        if items and len(items) < 1:
            raise InputParamError("<items> of <SearchedClaimMP> should contain at least 1 element")
        if items is None:
            raise InputParamError("<items> (=>items) of <SearchedClaimMP> is a required parameter")

        if route_points is not None:
            self.body["route_points"] = validate_fields('route_points', route_points, List['ResponseCargoPointMP'])
        if route_points and len(route_points) < 2:
            raise InputParamError("<route_points> of <SearchedClaimMP> should contain at least 2 element")
        if route_points is None:
            raise InputParamError("<route_points> (=>route_points) of <SearchedClaimMP> is a required parameter")

        if current_point_id is not None:
            self.body["current_point_id"] = validate_fields('current_point_id', current_point_id, int)
        if current_point_id is None:
            raise InputParamError("<current_point_id> (=>current_point_id) of <SearchedClaimMP> is a required parameter")

        if status is not None:
            self.body["status"] = validate_fields('status', status, str)
        if status is None:
            raise InputParamError("<status> (=>status) of <SearchedClaimMP> is a required parameter")

        if status not in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived',
                          'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning',
                          'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi',
                          'cancelled_with_items_on_hands']:
            raise InputParamError(
                "<status> of <SearchedClaimMP> should be in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived', 'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning', 'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi', 'cancelled_with_items_on_hands']")

        if version is not None:
            self.body["version"] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <SearchedClaimMP> is a required parameter")

        if error_messages is not None:
            self.body["error_messages"] = validate_fields('error_messages', error_messages, List['HumanErrorMessage'])

        if emergency_contact_name is not None:
            self.body["emergency_contact"]["name"] = validate_fields('emergency_contact_name', emergency_contact_name, str)
        if emergency_contact_name is None:
            raise InputParamError("<emergency_contact_name> (emergency_contact=>name) of <SearchedClaimMP> is a required parameter")

        if emergency_contact_phone is not None:
            self.body["emergency_contact"]["phone"] = validate_fields('emergency_contact_phone', emergency_contact_phone, str)
        if emergency_contact_phone is None:
            raise InputParamError("<emergency_contact_phone> (emergency_contact=>phone) of <SearchedClaimMP> is a required parameter")

        if skip_door_to_door is not None:
            self.body["skip_door_to_door"] = validate_fields('skip_door_to_door', skip_door_to_door, bool)

        if skip_client_notify is not None:
            self.body["skip_client_notify"] = validate_fields('skip_client_notify', skip_client_notify, bool)

        if skip_emergency_notify is not None:
            self.body["skip_emergency_notify"] = validate_fields('skip_emergency_notify', skip_emergency_notify, bool)

        if skip_act is not None:
            self.body["skip_act"] = validate_fields('skip_act', skip_act, bool)

        if optional_return is not None:
            self.body["optional_return"] = validate_fields('optional_return', optional_return, bool)

        if eta is not None:
            self.body["eta"] = validate_fields('eta', eta, int)

        if created_ts is not None:
            self.body["created_ts"] = validate_fields('created_ts', created_ts, str)
        if created_ts is None:
            raise InputParamError("<created_ts> (=>created_ts) of <SearchedClaimMP> is a required parameter")

        if updated_ts is not None:
            self.body["updated_ts"] = validate_fields('updated_ts', updated_ts, str)
        if updated_ts is None:
            raise InputParamError("<updated_ts> (=>updated_ts) of <SearchedClaimMP> is a required parameter")

        if taxi_offer_offer_id is not None:
            self.body["taxi_offer"]["offer_id"] = validate_fields('taxi_offer_offer_id', taxi_offer_offer_id, str)
        if taxi_offer_offer_id is None:
            raise InputParamError("<taxi_offer_offer_id> (taxi_offer=>offer_id) of <SearchedClaimMP> is a required parameter")

        if taxi_offer_price_raw is not None:
            self.body["taxi_offer"]["price_raw"] = validate_fields('taxi_offer_price_raw', taxi_offer_price_raw, int)
        if taxi_offer_price_raw is None:
            raise InputParamError("<taxi_offer_price_raw> (taxi_offer=>price_raw) of <SearchedClaimMP> is a required parameter")

        if taxi_offer_price is not None:
            self.body["taxi_offer"]["price"] = validate_fields('taxi_offer_price', taxi_offer_price, str)
        if taxi_offer_price is None:
            raise InputParamError("<taxi_offer_price> (taxi_offer=>price) of <SearchedClaimMP> is a required parameter")

        if pricing_offer_offer_id is not None:
            self.body["pricing"]["offer"]["offer_id"] = validate_fields('pricing_offer_offer_id', pricing_offer_offer_id, str)
        if pricing_offer_offer_id is None:
            raise InputParamError("<pricing_offer_offer_id> (pricing=>offer=>offer_id) of <SearchedClaimMP> is a required parameter")

        if pricing_offer_price_raw is not None:
            self.body["pricing"]["offer"]["price_raw"] = validate_fields('pricing_offer_price_raw', pricing_offer_price_raw, int)
        if pricing_offer_price_raw is None:
            raise InputParamError("<pricing_offer_price_raw> (pricing=>offer=>price_raw) of <SearchedClaimMP> is a required parameter")

        if pricing_offer_price is not None:
            self.body["pricing"]["offer"]["price"] = validate_fields('pricing_offer_price', pricing_offer_price, str)
        if pricing_offer_price is None:
            raise InputParamError("<pricing_offer_price> (pricing=>offer=>price) of <SearchedClaimMP> is a required parameter")

        if pricing_currency is not None:
            self.body["pricing"]["currency"] = validate_fields('pricing_currency', pricing_currency, str)

        if pricing_currency_rules_code is not None:
            self.body["pricing"]["currency_rules"]["code"] = validate_fields('pricing_currency_rules_code', pricing_currency_rules_code, str)
        if pricing_currency_rules_code is None:
            raise InputParamError("<pricing_currency_rules_code> (pricing=>currency_rules=>code) of <SearchedClaimMP> is a required parameter")

        if pricing_currency_rules_text is not None:
            self.body["pricing"]["currency_rules"]["text"] = validate_fields('pricing_currency_rules_text', pricing_currency_rules_text, str)
        if pricing_currency_rules_text is None:
            raise InputParamError("<pricing_currency_rules_text> (pricing=>currency_rules=>text) of <SearchedClaimMP> is a required parameter")

        if pricing_currency_rules_template is not None:
            self.body["pricing"]["currency_rules"]["template"] = validate_fields('pricing_currency_rules_template', pricing_currency_rules_template, str)
        if pricing_currency_rules_template is None:
            raise InputParamError("<pricing_currency_rules_template> (pricing=>currency_rules=>template) of <SearchedClaimMP> is a required parameter")

        if pricing_currency_rules_sign is not None:
            self.body["pricing"]["currency_rules"]["sign"] = validate_fields('pricing_currency_rules_sign', pricing_currency_rules_sign, str)

        if pricing_final_price is not None:
            self.body["pricing"]["final_price"] = validate_fields('pricing_final_price', pricing_final_price, str)
        if pricing_final_price is None:
            raise InputParamError("<pricing_final_price> (pricing=>final_price) of <SearchedClaimMP> is a required parameter")

        if available_cancel_state is not None:
            self.body["available_cancel_state"] = validate_fields('available_cancel_state', available_cancel_state, str)

        if available_cancel_state not in ['free', 'paid']:
            raise InputParamError("<available_cancel_state> of <SearchedClaimMP> should be in ['free', 'paid']")

        if client_requirements_taxi_class is not None:
            self.body["client_requirements"]["taxi_class"] = validate_fields('client_requirements_taxi_class', client_requirements_taxi_class, str)
        if client_requirements_taxi_class is None:
            raise InputParamError("<client_requirements_taxi_class> (client_requirements=>taxi_class) of <SearchedClaimMP> is a required parameter")

        if client_requirements_cargo_type is not None:
            self.body["client_requirements"]["cargo_type"] = validate_fields('client_requirements_cargo_type', client_requirements_cargo_type, str)

        if client_requirements_cargo_loaders is not None:
            self.body["client_requirements"]["cargo_loaders"] = validate_fields('client_requirements_cargo_loaders', client_requirements_cargo_loaders, int)
        if client_requirements_cargo_loaders and client_requirements_cargo_loaders < 0:
            raise InputParamError("<client_requirements_cargo_loaders> of <SearchedClaimMP> should be more than 0")

        if client_requirements_cargo_options is not None:
            self.body["client_requirements"]["cargo_options"] = validate_fields('client_requirements_cargo_options', client_requirements_cargo_options, List['str'])

        if matched_cars is not None:
            self.body["matched_cars"] = validate_fields('matched_cars', matched_cars, List['MatchedCar'])

        if warnings is not None:
            self.body["warnings"] = validate_fields('warnings', warnings, List['ClaimWarning'])

        if performer_info_courier_name is not None:
            self.body["performer_info"]["courier_name"] = validate_fields('performer_info_courier_name', performer_info_courier_name, str)
        if performer_info_courier_name is None:
            raise InputParamError("<performer_info_courier_name> (performer_info=>courier_name) of <SearchedClaimMP> is a required parameter")

        if performer_info_legal_name is not None:
            self.body["performer_info"]["legal_name"] = validate_fields('performer_info_legal_name', performer_info_legal_name, str)
        if performer_info_legal_name is None:
            raise InputParamError("<performer_info_legal_name> (performer_info=>legal_name) of <SearchedClaimMP> is a required parameter")

        if performer_info_car_model is not None:
            self.body["performer_info"]["car_model"] = validate_fields('performer_info_car_model', performer_info_car_model, str)

        if performer_info_car_number is not None:
            self.body["performer_info"]["car_number"] = validate_fields('performer_info_car_number', performer_info_car_number, str)

        if callback_properties_callback_url is not None:
            self.body["callback_properties"]["callback_url"] = validate_fields('callback_properties_callback_url', callback_properties_callback_url, str)
        if callback_properties_callback_url is None:
            raise InputParamError("<callback_properties_callback_url> (callback_properties=>callback_url) of <SearchedClaimMP> is a required parameter")

        if due is not None:
            self.body["due"] = validate_fields('due', due, str)

        if shipping_document is not None:
            self.body["shipping_document"] = validate_fields('shipping_document', shipping_document, str)

        if comment is not None:
            self.body["comment"] = validate_fields('comment', comment, str)

        if revision is not None:
            self.body["revision"] = validate_fields('revision', revision, int)
        if revision is None:
            raise InputParamError("<revision> (=>revision) of <SearchedClaimMP> is a required parameter")

    def __repr__(self):
        return "<SearchedClaimMP>"

    @property
    def id(self) -> str:
        """

        :return: Идентификатор заявки, полученный на этапе создания заявки
        :rtype: str
        """
        return self.body.get("id")

    @property
    def corp_client_id(self) -> Optional[str]:
        """

        :return: Идентификатор корпоративного клиента (из OAuth токена)
        :rtype: Optional[str]
        """
        return self.body.get("corp_client_id")

    @property
    def yandex_uid(self) -> Optional[str]:
        """

        :return: yandex uid
        :rtype: Optional[str]
        """
        return self.body.get("yandex_uid")

    @property
    def items(self) -> List['CargoItemMP']:
        """

        :return: Перечисление наименований грузов для отправления
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

        :return: Информация по точкам маршрута
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
    def current_point_id(self) -> int:
        """

        :return: Целочисленный идентификатор точки
        :rtype: int
        """
        return self.body.get("current_point_id")

    @property
    def status(self) -> str:
        """

        :return: Статус заявки

            * **new** - новая заявка
            * **estimating** - идет процесс оценки заявки (подбор типа автомобиля по параметрам груза и расчет стоимости)
            * **estimating_failed** - не удалось оценить заявку. Причину можно увидеть в error_messages в ответе ручки /info
            * **ready_for_approval** - заявка успешно оценена и ожидает подтверждения от клиента
            * **accepted** - заявка подтверждена клиентом
            * **performer_lookup** - заявка взята в обработку. Промежуточный статус перед созданием заказа
            * **performer_draft** - идет поиск водителя
            * **performer_found** - водитель найден и едет в точку А
            * **performer_not_found** - не удалось найти водителя. Можно попробовать снова через некоторое время
            * **pickup_arrived** - водитель приехал на точку А
            * **ready_for_pickup_confirmation** - водитель ждет, когда отправитель назовет ему код подтверждения
            * **pickuped** - водитель успешно забрал груз
            * **delivery_arrived** - водитель приехал на точку Б
            * **ready_for_delivery_confirmation** - водитель ждет, когда получатель назовет ему код подтверждения
            * **pay_waiting** - заказ ожидает оплаты (актуально для оплаты при получении)
            * **delivered** - водитель успешно доставил груз (ввел смс код). Код приходит после оплаты, если была оплата при получении.
            * **delivered_finish** - заказ завершен
            * **returning** -  водителю пришлось вернуть груз и он едет в точку возврата
            * **return_arrived** - водитель приехал на точку возврата
            * **ready_for_return_confirmation** - водитель в точке возврата ожидает, когда ему назовут код подтверждения
            * **returned** - водитель успешно вернул груз (ввел смс код)
            * **returned_finish** - заказ завершен
            * **failed** - терминальный статус, не удалось начать выполнение заказа
            * **cancelled** - заказ был отменен клиентом бесплатно
            * **cancelled_with_payment** - заказ был отменен клиентом платно (водитель уже приехал)
            * **cancelled_by_taxi** - водитель отменил заказ (до получения груза)
            * **cancelled_with_items_on_hands** - клиент платно отменил заявку без необходимости возврата груза (заявка была создана с флагом optional_return)

        :rtype: str
        """
        return self.body.get("status")

    @property
    def version(self) -> int:
        """

        :return: Версия
        :rtype: int
        """
        return self.body.get("version")

    @property
    def error_messages(self) -> Optional[List['HumanErrorMessage']]:
        """

        :return: Список сообщений об ошибках
        :rtype: Optional[List['HumanErrorMessage']]
        """
        return [HumanErrorMessage(code=item.get("code", None),
                                  message=item.get("message", None),
                                  ) for item in self.body.get("error_messages")]

    @property
    def emergency_contact_name(self) -> str:
        """

        :return: Имя контактного лица
        :rtype: str
        """
        return self.body.get("emergency_contact_name")

    @property
    def emergency_contact_phone(self) -> str:
        """

        :return: Телефон контактного лица
        :rtype: str
        """
        return self.body.get("emergency_contact_phone")

    @property
    def skip_door_to_door(self) -> Optional[bool]:
        """

        :return: Отказ от доставки до двери. В случае true — курьер доставит заказ только на улицу, до подъезда
        :rtype: Optional[bool]
        """
        return self.body.get("skip_door_to_door")

    @property
    def skip_client_notify(self) -> Optional[bool]:
        """

        :return: Не отправлять получателю нотификации, когда к нему направится курьер
        :rtype: Optional[bool]
        """
        return self.body.get("skip_client_notify")

    @property
    def skip_emergency_notify(self) -> Optional[bool]:
        """

        :return: Не отправлять нотификации emergency контакту
        :rtype: Optional[bool]
        """
        return self.body.get("skip_emergency_notify")

    @property
    def skip_act(self) -> Optional[bool]:
        """

        :return: Не показывать акт
        :rtype: Optional[bool]
        """
        return self.body.get("skip_act")

    @property
    def optional_return(self) -> Optional[bool]:
        """

        :return: Не требуется возврат товаров в случае отмены заказа. В случае true — курьер оставляет товар себе
        :rtype: Optional[bool]
        """
        return self.body.get("optional_return")

    @property
    def eta(self) -> Optional[int]:
        """

        :return: Ожидаемое время исполнения заказа в минутах
        :rtype: Optional[int]
        """
        return self.body.get("eta")

    @property
    def created_ts(self) -> str:
        """

        :return: Дата-время создания
        :rtype: str
        """
        return self.body.get("created_ts")

    @property
    def updated_ts(self) -> str:
        """

        :return: Дата-время последнего обновления
        :rtype: str
        """
        return self.body.get("updated_ts")

    @property
    def taxi_offer_offer_id(self) -> str:
        """

        :return: Идентификатор предложения
        :rtype: str
        """
        return self.body.get("taxi_offer_offer_id")

    @property
    def taxi_offer_price_raw(self) -> int:
        """

        :return: (deprecated) Цена по офферу в валюте, указанной в договоре
        :rtype: int
        """
        return self.body.get("taxi_offer_price_raw")

    @property
    def taxi_offer_price(self) -> str:
        """

        :return: Цена Decimal(19, 4)
        :rtype: str
        """
        return self.body.get("taxi_offer_price")

    @property
    def pricing_offer_offer_id(self) -> str:
        """

        :return: Идентификатор предложения
        :rtype: str
        """
        return self.body.get("pricing_offer_offer_id")

    @property
    def pricing_offer_price_raw(self) -> int:
        """

        :return: (deprecated) Цена по предложению в валюте, указанной в договоре
        :rtype: int
        """
        return self.body.get("pricing_offer_price_raw")

    @property
    def pricing_offer_price(self) -> str:
        """

        :return: Цена Decimal(19, 4)
        :rtype: str
        """
        return self.body.get("pricing_offer_price")

    @property
    def pricing_currency(self) -> Optional[str]:
        """

        :return: Трехзначный код валюты, в которой ведется расчет
        :rtype: Optional[str]
        """
        return self.body.get("pricing_currency")

    @property
    def pricing_currency_rules_code(self) -> str:
        """

        :return: Трехзначный код валюты, в которой ведется расчет
        :rtype: str
        """
        return self.body.get("pricing_currency_rules_code")

    @property
    def pricing_currency_rules_text(self) -> str:
        """

        :return: Сокращенное наименование валюты
        :rtype: str
        """
        return self.body.get("pricing_currency_rules_text")

    @property
    def pricing_currency_rules_template(self) -> str:
        """

        :return: Шаблон
        :rtype: str
        """
        return self.body.get("pricing_currency_rules_template")

    @property
    def pricing_currency_rules_sign(self) -> Optional[str]:
        """

        :return: Символ валюты
        :rtype: Optional[str]
        """
        return self.body.get("pricing_currency_rules_sign")

    @property
    def pricing_final_price(self) -> str:
        """

        :return: Цена Decimal(19, 4)
        :rtype: str
        """
        return self.body.get("pricing_final_price")

    @property
    def available_cancel_state(self) -> Optional[str]:
        """

        :return: Признак возможности платной/бесплатной отмены

            * **free** - платная отмена
            * **paid** - бесплатная отмена

        :rtype: Optional[str]
        """
        return self.body.get("available_cancel_state")

    @property
    def client_requirements_taxi_class(self) -> str:
        """

        :return: Класс такси. Возможные значения courier, express, cargo.
        :rtype: str
        """
        return self.body.get("client_requirements_taxi_class")

    @property
    def client_requirements_cargo_type(self) -> Optional[str]:
        """

        :return: Тип грузовика
        :rtype: Optional[str]
        """
        return self.body.get("client_requirements_cargo_type")

    @property
    def client_requirements_cargo_loaders(self) -> Optional[int]:
        """

        :return: Требуемое число грузчиков
        :rtype: Optional[int]
        """
        return self.body.get("client_requirements_cargo_loaders")

    @property
    def client_requirements_cargo_options(self) -> Optional[List['str']]:
        """

        :return: Дополнительные опции тарифа
        :rtype: Optional[List['str']]
        """
        return [item for item in self.body.get("client_requirements_cargo_options")]

    @property
    def matched_cars(self) -> Optional[List['MatchedCar']]:
        """

        :return: Информация об исполнителе (массив, на данный момент всегда 1 элемент)
        :rtype: Optional[List['MatchedCar']]
        """
        return [MatchedCar(taxi_class=item.get("taxi_class", None),
                           client_taxi_class=item.get("client_taxi_class", None),
                           cargo_type=item.get("cargo_type", None),
                           cargo_type_int=item.get("cargo_type_int", None),
                           cargo_loaders=item.get("cargo_loaders", None),
                           door_to_door=item.get("door_to_door", None),
                           ) for item in self.body.get("matched_cars")]

    @property
    def warnings(self) -> Optional[List['ClaimWarning']]:
        """

        :return: Предупреждения по циклу заявки
        :rtype: Optional[List['ClaimWarning']]
        """
        return [ClaimWarning(source=item.get("source", None),
                             code=item.get("code", None),
                             message=item.get("message", None),
                             ) for item in self.body.get("warnings")]

    @property
    def performer_info_courier_name(self) -> str:
        """

        :return: Имя курьера, доставляющего посылку
        :rtype: str
        """
        return self.body.get("performer_info_courier_name")

    @property
    def performer_info_legal_name(self) -> str:
        """

        :return: Данные о юридическом лице, которое осуществляет доставку
        :rtype: str
        """
        return self.body.get("performer_info_legal_name")

    @property
    def performer_info_car_model(self) -> Optional[str]:
        """

        :return: Модель машины
        :rtype: Optional[str]
        """
        return self.body.get("performer_info_car_model")

    @property
    def performer_info_car_number(self) -> Optional[str]:
        """

        :return: Номер машины
        :rtype: Optional[str]
        """
        return self.body.get("performer_info_car_number")

    @property
    def callback_properties_callback_url(self) -> str:
        """

        :return: URL, который будет вызываться при смене статусов по заявке.  Данный механизм устарел, вместо него следует использовать операцию v1/claims/journal.
        :rtype: str
        """
        return self.body.get("callback_properties_callback_url")

    @property
    def due(self) -> Optional[str]:
        """

        :return: Создать заказ к определенному времени (например, заказ на завтра). Согласуйте с менеджером использование опции!
        :rtype: Optional[str]
        """
        return self.body.get("due")

    @property
    def shipping_document(self) -> Optional[str]:
        """

        :return: Сопроводительные документы
        :rtype: Optional[str]
        """
        return self.body.get("shipping_document")

    @property
    def comment(self) -> Optional[str]:
        """

        :return: Общий комментарий к заказу
        :rtype: Optional[str]
        """
        return self.body.get("comment")

    @property
    def revision(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.body.get("revision")


class TimeInterval(YCBase):
    """

    Временной интервал, который можно навесить на точку для придания ей дополнительных свойств

    :param str type: Тип интервала: strict_match - необходимо найти кандидата, который попадает в указанный интервал времени, иначе фолбечная логика (настраивается); perfect_match - кандидаты, попадающие в этот интервал времени, имеют преимущество перед не попадающими.  *(Обязательный параметр)*

        * **strict_match** - ???
        * **perfect_match** - ???

    :param str _from: Начало интервала *(Обязательный параметр)* (2020-01-01T00:00:00+00:00)
    :param str to: Окончание интервала *(Обязательный параметр)* (2020-01-02T00:00:00+00:00)
    """

    def __init__(self,
                 type: str = None,
                 _from: str = None,
                 to: str = None,
                 ):
        self.body = collections.defaultdict(dict)

        if type is not None:
            self.body["type"] = validate_fields('type', type, str)
        if type is None:
            raise InputParamError("<type> (=>type) of <TimeInterval> is a required parameter")

        if type not in ['strict_match', 'perfect_match']:
            raise InputParamError("<type> of <TimeInterval> should be in ['strict_match', 'perfect_match']")

        if _from is not None:
            self.body["from"] = validate_fields('_from', _from, str)
        if _from is None:
            raise InputParamError("<_from> (=>from) of <TimeInterval> is a required parameter")

        if to is not None:
            self.body["to"] = validate_fields('to', to, str)
        if to is None:
            raise InputParamError("<to> (=>to) of <TimeInterval> is a required parameter")

    def __repr__(self):
        return "<TimeInterval>"

    @property
    def type(self) -> str:
        """

        :return: Тип интервала: strict_match - необходимо найти кандидата, который попадает в указанный интервал времени, иначе фолбечная логика (настраивается); perfect_match - кандидаты, попадающие в этот интервал времени, имеют преимущество перед не попадающими.

            * **strict_match** - ???
            * **perfect_match** - ???

        :rtype: str
        """
        return self.body.get("type")

    @property
    def _from(self) -> str:
        """

        :return: Начало интервала
        :rtype: str
        """
        return self.body.get("_from")

    @property
    def to(self) -> str:
        """

        :return: Окончание интервала
        :rtype: str
        """
        return self.body.get("to")


class VoiceforwardingResponse(YCBase):
    """

    Информация о номере телефона для звонка водителю

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
        if phone is None:
            raise InputParamError("<phone> (=>phone) of <VoiceforwardingResponse> is a required parameter")

        if ext is not None:
            self.body["ext"] = validate_fields('ext', ext, str)
        if ext is None:
            raise InputParamError("<ext> (=>ext) of <VoiceforwardingResponse> is a required parameter")

        if ttl_seconds is not None:
            self.body["ttl_seconds"] = validate_fields('ttl_seconds', ttl_seconds, int)
        if ttl_seconds and ttl_seconds < 2088:
            raise InputParamError("<ttl_seconds> of <VoiceforwardingResponse> should be more than 2088")
        if ttl_seconds is None:
            raise InputParamError("<ttl_seconds> (=>ttl_seconds) of <VoiceforwardingResponse> is a required parameter")

    def __repr__(self):
        return "<VoiceforwardingResponse>"

    @property
    def phone(self) -> str:
        """

        :return: Номер телефона
        :rtype: str
        """
        return self.body.get("phone")

    @property
    def ext(self) -> str:
        """

        :return: Добавочный номер
        :rtype: str
        """
        return self.body.get("ext")

    @property
    def ttl_seconds(self) -> int:
        """

        :return: Время, в течение которого этот номер действителен
        :rtype: int
        """
        return self.body.get("ttl_seconds")
