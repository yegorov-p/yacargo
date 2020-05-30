# # -*- coding: utf-8 -*-
import re
from typing import List, Optional

from typeguard import check_type

from yacargo.constants import VAT_CODE, PAYMENT_SUBJECT, PAYMENT_MODE, COUNTRY_OF_ORIGIN_CODE, TAX_SYSTEM_CODE, TAXI_CLASS, CARGO_TYPE
from yacargo.exceptions import InputParamError


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
        return field if isinstance(field, (bool, str, int, float, tuple, list, dict)) else field.json()


class YCBase:
    """
        Базовый класс
    """
    def __init__(self):
        self.body = {}

    def json(self) -> dict:
        """

        :return: Объект в виде JSON
        :rtype: dict
        """
        return self.body


class CargoItemSizes(YCBase):
    """
        Линейные размеры одного предмета в метрах

        :param float length: глубина в метрах *(Обязательный параметр)*

        :param float width: ширина в метрах *(Обязательный параметр)*

        :param float height: высота в метрах *(Обязательный параметр)*
    """

    def __init__(self, length, width, height):
        super().__init__()
        self.body['length'] = validate_fields('length', length, float)
        self.body['width'] = validate_fields('width', width, float)
        self.body['height'] = validate_fields('height', height, float)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def length(self) -> float:
        """

        :return: глубина в метрах
        :rtype: float
        """
        return self.body.get('length')

    @property
    def width(self) -> float:
        """

        :return: ширина в метрах
        :rtype: float
        """
        return self.body.get('width')

    @property
    def height(self) -> float:
        """

        :return: высота в метрах
        :rtype: float
        """
        return self.body.get('height')


class ItemFiscalization(YCBase):
    """
        Детализация по товару для фискализации

        :param int vat_code: Ставка НДС *(Обязательный параметр)*

            * **1** - Без НДС
            * **2** - НДС по ставке 0%
            * **3** - НДС по ставке 10%
            * **4** - НДС чека по ставке 20%
            * **5**	- НДС чека по расчетной ставке 10/110
            * **6** - НДС чека по расчетной ставке 20/120

        :param str payment_subject: Признак предмета расчета *(Обязательный параметр)*

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

        :param str payment_mode: Признак способа расчета *(Обязательный параметр)*

            * **full_prepayment** - Полная предоплата
            * **partial_prepayment** - Частичная предоплата
            * **advance** - Аванс
            * **full_payment** - Полный расчет
            * **partial_payment** - Частичный расчет и кредит
            * **credit** - Кредит
            * **credit_payment** - Выплата по кредиту

        :param str product_code: Уникальный номер, который присваивается экземпляру товара при `маркировке <http://docs.cntd.ru/document/902192509>`__

                                Формат: число в шестнадцатеричном представлении с пробелами. Максимальная длина — 32 байта.

                                Пример: *00 00 00 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00*.

                                Обязательный параметр, если товар нужно `маркировке <http://docs.cntd.ru/document/557297080>`__.

        :param str country_of_origin_code: Код страны происхождения товара по `общероссийскому классификатору стран мира <http://docs.cntd.ru/document/842501280>`__. Пример: RU.

        :param str customs_declaration_number: Номер таможенной декларации (от 1 до 32 символов).

        :param float excise: Сумма акциза товара с учетом копеек. Десятичное число с точностью до 2 символов после точки.
    """

    def __init__(self,
                 vat_code: int,
                 payment_subject: str,
                 payment_mode: str,
                 product_code: str = None,
                 country_of_origin_code: str = None,
                 customs_declaration_number: str = None,
                 excise: float = None):
        super().__init__()

        self.body['vat_code'] = validate_fields('vat_code', vat_code, int)
        if self.body['vat_code'] not in VAT_CODE:
            raise InputParamError('"vat_code" should be {}'.format(', '.join(VAT_CODE)))

        self.body['payment_subject'] = validate_fields('payment_subject', payment_subject, str)
        if self.body['payment_subject'] not in PAYMENT_SUBJECT:
            raise InputParamError('"payment_subject" should be {}'.format(', '.join(PAYMENT_SUBJECT)))

        self.body['payment_mode'] = validate_fields('payment_mode', payment_mode, str)
        if self.body['payment_mode'] not in PAYMENT_MODE:
            raise InputParamError('"payment_mode" should be {}'.format(', '.join(PAYMENT_MODE)))

        if product_code:
            self.body['product_code'] = validate_fields('product_code', product_code, str)
            if not re.match('([0-9A-F]{2} ){31}[0-9A-F]{2}', self.body['product_code']):
                raise InputParamError('"product_code" is in a wrong format')

        if country_of_origin_code:
            self.body['country_of_origin_code'] = validate_fields('country_of_origin_code', country_of_origin_code, str)
            if self.body['country_of_origin_code'] not in COUNTRY_OF_ORIGIN_CODE:
                raise InputParamError('"country_of_origin_code" should be {}'.format(', '.join(COUNTRY_OF_ORIGIN_CODE)))

        if customs_declaration_number:
            self.body['customs_declaration_number'] = validate_fields('customs_declaration_number', customs_declaration_number, str)
            if len(self.body['customs_declaration_number']) > 32:
                raise InputParamError('"customs_declaration_number" should be shorter than 32 symbols')

        if excise:
            self.body['excise'] = validate_fields('excise', excise, float)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def vat_code(self) -> int:
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
        return self.body.get('vat_code')

    @property
    def payment_subject(self) -> str:
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
        return self.body.get('payment_subject')

    @property
    def payment_mode(self) -> str:
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
        return self.body.get('payment_mode')

    @property
    def product_code(self) -> str:
        """

        :return: Уникальный номер, который присваивается экземпляру товара при `маркировке <http://docs.cntd.ru/document/902192509>`__

                Формат: число в шестнадцатеричном представлении с пробелами. Максимальная длина — 32 байта.

                Пример: *00 00 00 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00*.

                Обязательный параметр, если товар нужно `маркировке <http://docs.cntd.ru/document/557297080>`__.

        :rtype: str
        """
        return self.body.get('product_code')

    def country_of_origin_code(self) -> str:
        """

        :return: Код страны происхождения товара по `общероссийскому классификатору стран мира <http://docs.cntd.ru/document/842501280>`__. Пример: RU.
        :rtype: str
        """
        return self.body.get('country_of_origin_code')

    def customs_declaration_number(self) -> str:
        """

        :return Номер таможенной декларации (от 1 до 32 символов).
        :rtype: str
        """
        return self.body.get('customs_declaration_number')

    def excise(self) -> float:
        """

        :return Сумма акциза товара с учетом копеек. Десятичное число с точностью до 2 символов после точки.
        :rtype: float
        """
        return self.body.get('excise')


class ContactOnPoint(YCBase):
    """
        Контактные данные

        :param str name: Имя контактного лица *(Обязательный параметр)*

        :param str phone: Телефон контактного лица *(Обязательный параметр)*

        :param str email: Email контактного лица *(Обязательный параметр для точек source и return)*

    """

    def __init__(self,
                 name: str,
                 phone: str,
                 email: str = None):
        super().__init__()

        self.body['name'] = validate_fields('name', name, str)
        self.body['phone'] = validate_fields('phone', phone, str)

        if email:
            self.body['email'] = validate_fields('email', email, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def name(self) -> str:
        """

        :return: Имя контактного лица
        :rtype: str
        """
        return self.body.get('name')

    @property
    def phone(self) -> str:
        """

        :return: Телефон контактного лица
        :rtype: str
        """
        return self.body.get('phone')

    @property
    def email(self) -> str:
        """

        :return: Email контактного лица
        :rtype: str
        """
        return self.body.get('email')


class CargoPointAddress(YCBase):
    """
        Адрес точки маршрута

        :param str fullname: Человеко-понятное название *(Обязательный параметр)* (Садовническая набережная, БЦ Аврора)

        :param List[float] coordinates: Координаты [долгота, широта] *(Обязательный параметр)*

        :param str country: Страна

        :param str city: Город

        :param str street: Название улицы

        :param str building: Номер дома/строение

        :param str porch: Номер подъезда

        :param str sfloor: Номер этажа

        :param str sflat: Номер квартиры

        :param str door_code: Код от подъезда/домофона

        :param str comment: Комментарий к адресу

        :param str uri: Карточный uri геообъекта
    """

    def __init__(self,
                 fullname: str,
                 coordinates: List[float],
                 country: str = None,
                 city: str = None,
                 street: str = None,
                 building: str = None,
                 porch: str = None,
                 sfloor: str = None,
                 sflat: str = None,
                 door_code: str = None,
                 comment: str = None,
                 uri: str = None,
                 ):
        super().__init__()

        self.body['fullname'] = validate_fields('fullname', fullname, str)
        self.body['coordinates'] = validate_fields('coordinates', coordinates, List[float])
        if country:
            self.body['country'] = validate_fields('country', country, str)
        if city:
            self.body['city'] = validate_fields('city', city, str)
        if street:
            self.body['street'] = validate_fields('street', street, str)
        if building:
            self.body['building'] = validate_fields('building', building, str)
        if porch:
            self.body['porch'] = validate_fields('porch', porch, str)
        if sfloor:
            self.body['sfloor'] = validate_fields('sfloor', sfloor, str)
        if sflat:
            self.body['sflat'] = validate_fields('sflat', sflat, str)
        if door_code:
            self.body['door_code'] = validate_fields('door_code', door_code, str)
        if comment:
            self.body['comment'] = validate_fields('comment', comment, str)
        if uri:
            self.body['uri'] = validate_fields('uri', uri, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def fullname(self) -> str:
        """

        :return: Человеко-понятное название (Садовническая набережная, БЦ Аврора) (обязательный параметр)
        :rtype: str
        """
        return self.body.get('fullname')

    @property
    def coordinates(self) -> List[float]:
        """

        :return: Координаты [долгота, широта]
        :rtype: List[float]
        """
        return self.body.get('coordinates')

    @property
    def country(self) -> str:
        """

        :return: Страна
        :rtype: str
        """
        return self.body.get('country')

    @property
    def city(self) -> str:
        """

        :return: Город
        :rtype: str
        """
        return self.body.get('city')

    @property
    def street(self) -> str:
        """

        :return: Название улицы
        :rtype: str
        """
        return self.body.get('street')

    @property
    def building(self) -> str:
        """

        :return: Номер дома/строение
        :rtype: str
        """
        return self.body.get('building')

    @property
    def porch(self) -> str:
        """

        :return: Номер подъезда (может быть A)
        :rtype: str
        """
        return self.body.get('porch')

    @property
    def sfloor(self) -> str:
        """

        :return: Номер этажа
        :rtype: str
        """
        return self.body.get('sfloor')

    @property
    def sflat(self) -> str:
        """

        :return: Номер квартиры
        :rtype: str
        """
        return self.body.get('sflat')

    @property
    def door_code(self) -> str:
        """

        :return: Код от подъезда/домофона
        :rtype: str
        """
        return self.body.get('door_code')

    @property
    def comment(self) -> str:
        """

        :return: Комментарий к адресу
        :rtype: str
        """
        return self.body.get('comment')

    @property
    def uri(self) -> str:
        """

        :return: Карточный uri геообъекта
        :rtype: str
        """
        return self.body.get('uri')


class CustomerFiscalization(YCBase):
    """
        Параметры оплаты при получении

        :param str full_name: Название организации или ФИО

        :param str inn: ИНН пользователя (10 или 12 цифр)

        :param str email: Электронная почта пользователя

        :param str phone: Телефон пользователя в формате ITU-T E.164 ("79000000000")
    """

    def __init__(self,
                 full_name: str,
                 inn: str,
                 email: str,
                 phone: str):
        super().__init__()

        if full_name:
            self.body['full_name'] = validate_fields('full_name', full_name, str)

        if inn:
            self.body['inn'] = validate_fields('inn', inn, str)
            if len(self.body['inn']) not in (10, 12):
                raise InputParamError('Wrong INN format')

        if email:
            self.body['email'] = validate_fields('email', email, str)

        if phone:
            self.body['phone'] = validate_fields('phone', phone, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def full_name(self) -> str:
        """

        :return: Название организации или ФИО
        :rtype: str
        """
        return self.body.get('full_name')

    @property
    def inn(self) -> str:
        """

        :return: ИНН пользователя (10 или 12 цифр)
        :rtype: str
        """
        return self.body.get('inn')

    @property
    def email(self) -> str:
        """

        :return: Электронная почта пользователя
        :rtype: str
        """
        return self.body.get('email')

    @property
    def phone(self) -> str:
        """

        :return: Телефон пользователя в формате ITU-T E.164 ("79000000000")
        :rtype: str
        """
        return self.body.get('phone')


class RequestPaymentOnDelivery(YCBase):
    """
        Параметры оплаты при получении (актуально для оплаты при получении только для destination точек)

        :param str client_order_id: id заказа клиента *(обязательный параметр)*

        :param float cost: Сумма платежа в рублях *(обязательный параметр)*

        :param CustomerFiscalization customer: Информация о пользователе

        :param int tax_system_code: Код системы налогообложения:

            * **1** - Общая система налогообложения
            * **2** - Упрощенная (УСН, доходы)
            * **3** - Упрощенная (УСН, доходы минус расходы)
            * **4** - Единый налог на вмененный доход (ЕНВД)
            * **5** - Единый сельскохозяйственный налог (ЕСН)
            * **6** - Патентная система налогообложения

    """

    def __init__(self,
                 client_order_id: str,
                 cost: float,
                 customer: CustomerFiscalization,
                 tax_system_code: int):
        super().__init__()

        self.body['client_order_id'] = validate_fields('client_order_id', client_order_id, str)
        self.body['cost'] = validate_fields('cost', cost, float)
        if customer:
            self.body['customer'] = validate_fields('customer', customer, CustomerFiscalization)
        if tax_system_code:
            self.body['tax_system_code'] = validate_fields('tax_system_code', tax_system_code, int)
            if self.body['tax_system_code'] not in TAX_SYSTEM_CODE:
                raise InputParamError('"tax_system_code" should be {}'.format(', '.join(TAX_SYSTEM_CODE)))

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def client_order_id(self) -> str:
        """

        :return: id заказа клиента
        :rtype: str
        """
        return self.body.get('client_order_id')

    def cost(self) -> float:
        """

        :return: Сумма платежа в рублях
        :rtype: float
        """
        return self.body.get('cost')

    def customer(self) -> CustomerFiscalization:
        """

        :return: Информация о пользователе
        :rtype: CustomerFiscalization
        """
        return self.body.get('customer')

    def tax_system_code(self) -> int:
        """

        :return: Код системы налогообложения:

            * **1** - Общая система налогообложения
            * **2** - Упрощенная (УСН, доходы)
            * **3** - Упрощенная (УСН, доходы минус расходы)
            * **4** - Единый налог на вмененный доход (ЕНВД)
            * **5** - Единый сельскохозяйственный налог (ЕСН)
            * **6** - Патентная система налогообложения

        :rtype: int
        """
        return self.body.get('tax_system_code')


class CargoItemMP(YCBase):
    """
        Коробка

        :param int pickup_point: id точки, откуда нужно забрать товар (отличается от id в заявке) *(обязательный параметр)*
        :param int droppof_point: id точки, куда нужно доставить товар (отличается от id в заявке) *(обязательный параметр)*
        :param str title: Именование единицы товара *(обязательный параметр)*
        :param str cost_value: Стоимость товара (для страховки) *(обязательный параметр)*
        :param str cost_currency: Валюта стоимости товара в международном формате ISO 4217 *(обязательный параметр)*
        :param int quantity: Количесто единиц товара (минимум 1) *(обязательный параметр)*
        :param str extra_id: Краткий уникальный идентификатор item'а (в рамках заявки) (БП-208)
        :param CargoItemSizes size: Размеры товара
        :param float weight: Вес в кг
        :param ItemFiscalization fiscalization: Информация по фискализации (актуально для оплаты при получении)

    """

    def __init__(self,
                 pickup_point: int,
                 droppof_point: int,
                 title: str,
                 cost_value: float,
                 cost_currency: str,
                 quantity: int,
                 extra_id: str = None,
                 size: CargoItemSizes = None,
                 weight: float = None,
                 fiscalization: ItemFiscalization = None
                 ):
        super().__init__()

        self.body['pickup_point'] = validate_fields('pickup_point', pickup_point, int)
        self.body['droppof_point'] = validate_fields('droppof_point', droppof_point, int)
        if pickup_point == droppof_point:
            raise InputParamError('"pickup_point" and "droppof_point" cannot be equal')
        self.body['title'] = validate_fields('title', title, str)
        self.body['cost_value'] = validate_fields('cost_value', cost_value, float)
        self.body['cost_currency'] = validate_fields('cost_currency', cost_currency, str)
        self.body['quantity'] = validate_fields('quantity', quantity, int)

        if extra_id:
            self.body['extra_id'] = validate_fields('extra_id', extra_id, str)
        if size:
            self.body['size'] = validate_fields('size', size, CargoItemSizes)
        if weight:
            self.body['weight'] = validate_fields('weight', weight, float)
        if quantity < 1:
            raise InputParamError('"quantity" should is more or equal 1')
        if fiscalization:
            self.body['fiscalization'] = validate_fields('fiscalization', fiscalization, ItemFiscalization)

    def __repr__(self):
        return '<{name} {title}>'.format(name=self.__class__.__name__, title=self.title)

    @property
    def pickup_point(self) -> int:
        """

        :return: id точки, откуда нужно забрать товар (отличается от id в заявке)
        :rtype: int
        """
        return self.body.get('pickup_point')

    @property
    def droppof_point(self) -> int:
        """

        :return: id точки, куда нужно доставить товар (отличается от id в заявке)
        :rtype: int
        """
        return self.body.get('droppof_point')

    @property
    def title(self) -> str:
        """

        :return: Именование единицы товара
        :rtype: str
        """
        return self.body.get('title')

    @property
    def cost_value(self) -> float:
        """

        :return: Стоимость товара (для страховки)
        :rtype: float
        """
        return self.body.get('cost_value')

    @property
    def cost_currency(self) -> str:
        """

        :return: Валюта стоимости товара в международном формате ISO 4217
        :rtype: str
        """
        return self.body.get('cost_currency')

    @property
    def quantity(self) -> int:
        """

        :return int: quantity: Количесто единиц товара
        """
        return self.body.get('quantity')

    @property
    def extra_id(self) -> Optional[str]:
        """

        :return: Краткий уникальный идентификатор item'а (в рамках заявки)
        :rtype: Optional[str]
        """
        return self.body.get('extra_id')

    @property
    def size(self) -> Optional[CargoItemSizes]:
        """

        :return: Размеры товара
        :rtype: Optional[CargoItemSizes]
        """
        size = self.body.get('size')
        if size:
            return CargoItemSizes(length=size.get('length'),
                                  width=size.get('width'),
                                  height=size.get('height'))
        return None

    @property
    def weight(self) -> Optional[float]:
        """

        :return: Вес в кг
        :rtype: Optional[float]
        """
        return self.body.get('weight')

    @property
    def fiscalization(self) -> Optional[ItemFiscalization]:
        """

        :return: Информация по фискализации
        :rtype: Optional[ItemFiscalization]
        """
        return self.body.get('fiscalization')


class CargoPointMP(YCBase):
    """
        Описание точки в заявке с мультиточками

        :param int point_id: Уникальный идентификатор точки (id в таблице claim_points) *(Обязательный параметр)*

        :param int visit_order: Порядок посещения точки *(Обязательный параметр)*

        :param ContactOnPoint contact: Контактные данные отправителя *(Обязательный параметр)*

        :param CargoPointAddress address: Адрес точки *(Обязательный параметр)*

        :param str point_type: Тип точки: *(Обязательный параметр)*

            * **source** — точка получения отправления (ровно одна)
            * **destination** — точка доставки отправления
            * **return** — точка возврата части товаров, опциональная (не более одной)

        :param bool skip_confirmation: Пропускать подтверждение через смс в данной точке

        :param RequestPaymentOnDelivery payment_on_delivery: Информация по оплате при получении (актуально для оплаты при получении только для destination точек)

        :param str external_order_id: Номер заказа клиента

        :param str pickup_code: Код выдачи товара (ПВЗ)


    """

    def __init__(self,
                 point_id: int,
                 visit_order: int,
                 contact: ContactOnPoint,
                 address: CargoPointAddress,
                 point_type: str,
                 skip_confirmation: bool = None,
                 payment_on_delivery: RequestPaymentOnDelivery = None,
                 external_order_id: str = None,
                 pickup_code: str = None,
                 visit_status: str = None
                 ):
        super().__init__()
        self.body['point_id'] = validate_fields('point_id', point_id, int)
        self.body['visit_order'] = validate_fields('visit_order', visit_order, int)
        self.body['contact'] = validate_fields('contact', contact, ContactOnPoint)
        self.body['address'] = validate_fields('address', address, CargoPointAddress)

        if point_type not in ('source', 'destination', 'return'):
            raise InputParamError('Wrong point type, should be source, destination or return')
        self.body['type'] = validate_fields('point_type', point_type, str)

        if skip_confirmation:
            self.body['skip_confirmation'] = validate_fields('skip_confirmation', skip_confirmation, bool)
        if payment_on_delivery:
            self.body['payment_on_delivery'] = validate_fields('payment_on_delivery', payment_on_delivery, RequestPaymentOnDelivery)
        if external_order_id:
            self.body['external_order_id'] = validate_fields('external_order_id', external_order_id, str)
        if pickup_code:
            self.body['pickup_code'] = validate_fields('pickup_code', pickup_code, str)

        self._visit_status = visit_status

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def visit_status(self) -> str:
        """

        :return: Статус посещения данной точки

              * **pending** - ждет исполнения
              * **arrived** - курьер прибыл на точку, но еще не передал/забрал товар
              * **visited** - передали/забрали товар из точки
              * **skipped** - возврат (то есть клиент в этой точке не принял посылку и ее повезут в точку возврата. не значит, что товар уже вернули на склад)

        :rtype: str
        """
        return self._visit_status

    @property
    def point_id(self) -> int:
        """

        :return: Уникальный идентификатор точки
        :rtype: int
        """
        return self.body.get('point_id')

    @property
    def visit_order(self) -> int:
        """

        :return: Порядок посещения
        :rtype: int
        """
        return self.body.get('visit_order')

    @property
    def contact(self) -> ContactOnPoint:
        """

        :return: Контактные данные отправителя
        :rtype: ContactOnPoint
        """
        contact = self.body.get('contact')
        return ContactOnPoint(name=contact.get('name'),
                              phone=contact.get('phone'),
                              email=contact.get('email'),
                              )

    @property
    def address(self) -> CargoPointAddress:
        """

        :return: Адрес точки
        :rtype: CargoPointAddress
        """
        address = self.body.get('address')
        return CargoPointAddress(fullname=address.get('fullname'),
                                 coordinates=address.get('coordinates'),
                                 country=address.get('country'),
                                 city=address.get('city'),
                                 street=address.get('street'),
                                 building=address.get('building'),
                                 porch=address.get('porch'),
                                 sfloor=address.get('sfloor'),
                                 sflat=address.get('sflat'),
                                 door_code=address.get('door_code'),
                                 comment=address.get('comment'),
                                 uri=address.get('uri')
                                 )

    @property
    def point_type(self) -> str:
        """

        :return: Тип точки:

            * **source** — точка получения отправления
            * **destination** — точка доставки отправления
            * **return** — точка возврата части товаров

        :rtype: str
        """
        return self.body.get('type')

    @property
    def skip_confirmation(self) -> bool:
        """

        :return: Пропускать подтверждение через смс в данной точке
        :rtype: bool
        """
        return self.body.get('skip_confirmation', False)

    @property
    def payment_on_delivery(self) -> Optional[RequestPaymentOnDelivery]:
        """

        :return: Информация по оплате при получении
        :rtype: Optional[RequestPaymentOnDelivery]
        """
        result = self.body.get('payment_on_delivery')
        if result:
            customer = result.get('customer')
            return RequestPaymentOnDelivery(client_order_id=result.get('client_order_id'),
                                            cost=result.get('cost'),
                                            customer=CustomerFiscalization(full_name=customer.get('full_name'),
                                                                           inn=customer.get('inn'),
                                                                           email=customer.get('email'),
                                                                           phone=customer.get('phone')),
                                            tax_system_code=result.get('tax_system_code')
                                            )
        return None

    @property
    def external_order_id(self) -> Optional[str]:
        """

        :return: Номер заказа клиента
        :rtype: Optional[str]
        """
        return self.body.get('external_order_id')

    @property
    def pickup_code(self) -> Optional[str]:
        """

        :return: Код выдачи товара (ПВЗ)
        :rtype: Optional[str]
        """
        return self.body.get('pickup_code')


class C2CData(YCBase):
    """

        :param str payment_type: ??? *(Обязательный параметр)*
        :param str payment_method_id:
    """

    def __init__(self,
                 payment_type,
                 payment_method_id=None):
        super().__init__()

        self.body['payment_type'] = validate_fields('payment_type', payment_type, str)
        if payment_method_id:
            self.body['payment_method_id'] = validate_fields('payment_method_id', payment_method_id, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def payment_type(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('payment_type')

    @property
    def payment_method_id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('payment_method_id')


class ContactWithPhone(YCBase):
    """
        Контакт с телефонным номером

        :param str name: Имя контактного лица *(Обязательный параметр)*

        :param str phone: Телефон контактного лица *(Обязательный параметр)*
    """

    def __init__(self,
                 name: str,
                 phone: str
                 ):
        super().__init__()

        self.body['name'] = validate_fields('name', name, str)
        self.body['phone'] = validate_fields('phone', phone, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def name(self) -> str:
        """

        :return: Имя контактного лица
        :rtype: str
        """
        return self.body.get('name')

    @property
    def phone(self) -> str:
        """

        :return: Телефон контактного лица
        :rtype: str
        """
        return self.body.get('phone')


class ClientRequirements(YCBase):
    """
        Требования от клиента

        :param str taxi_class: Класс такси *(Обязательный параметр)*

            * **express** - Легковое авто
            * **courier** - Курьер
            * **cargo** - Грузовое авто

        :param str cargo_type: Тип грузовика

            * **van** - 190см в длину, 100 в шириру, 90 в высоту
            * **lcv_m** - 260см в длину, 160 в ширину, 150 в высоту
            * **lcv_l** - 400 см в длину, 190 в ширину, 200 в высоту

        :param str cargo_loaders: Количество грузчиков (минимум 0)
    """

    def __init__(self,
                 taxi_class: str,
                 cargo_type: str,
                 cargo_loaders: str):
        super().__init__()

        if taxi_class:
            self.body['taxi_class'] = validate_fields('taxi_class', taxi_class, str)
            if self.body['taxi_class'] not in TAXI_CLASS:
                raise InputParamError('"taxi_class" should be {}'.format(', '.join(TAXI_CLASS)))

        if cargo_type:
            self.body['cargo_type'] = validate_fields('cargo_type', cargo_type, str)
            if self.body['cargo_type'] not in CARGO_TYPE:
                raise InputParamError('"cargo_type" should be {}'.format(', '.join(CARGO_TYPE)))

        if cargo_loaders:
            self.body['cargo_loaders'] = validate_fields('cargo_loaders', cargo_loaders, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def taxi_class(self) -> str:
        """

        :return: Класс такси

            * **express** - Легковое авто
            * **courier** - Курьер
            * **cargo** - Грузовое авто

        :rtype: str
        """
        return self.body.get('taxi_class')

    @property
    def cargo_type(self) -> str:
        """

        :return: Тип грузовика

            * **van** - 190см в длину, 100 в шириру, 90 в высоту
            * **lcv_m** - 260см в длину, 160 в ширину, 150 в высоту
            * **lcv_l** - 400 см в длину, 190 в ширину, 200 в высоту

        :rtype: str
        """
        return self.body.get('cargo_type')

    @property
    def cargo_loaders(self) -> str:
        """

        :return: Количество грузчиков (минимум 0)
        :rtype: str
        """
        return self.body.get('cargo_loaders')


class ResponsePaymentOnDelivery(YCBase):
    """
        Параметры оплаты при получение

        :param str client_order_id: id заказа клиента *(Обязательный параметр)*

        :param bool is_paid: Оплачен ли заказ *(Обязательный параметр)*

        :param float cost: Сумма платежа в рублях *(Обязательный параметр)*

        :param CustomerFiscalization customer: Информация о пользователе

        :param int tax_system_code: Код системы налогообложения:

            * **1** - Общая система налогообложения
            * **2** - Упрощенная (УСН, доходы)
            * **3** - Упрощенная (УСН, доходы минус расходы)
            * **4** - Единый налог на вмененный доход (ЕНВД)
            * **5** - Единый сельскохозяйственный налог (ЕСН)
            * **6** - Патентная система налогообложения

    """

    def __init__(self,
                 client_order_id: str,
                 is_paid: bool,
                 cost: float,
                 customer: CustomerFiscalization = None,
                 tax_system_code: int = None):
        super().__init__()

        self.body['client_order_id'] = validate_fields('client_order_id', client_order_id, str)
        self.body['is_paid'] = validate_fields('is_paid', is_paid, bool)
        self.body['cost'] = validate_fields('cost', cost, float)
        if customer:
            self.body['customer'] = validate_fields('customer', customer, CustomerFiscalization)
        if tax_system_code:
            self.body['tax_system_code'] = validate_fields('tax_system_code', tax_system_code, int)
            if self.body['tax_system_code'] not in TAX_SYSTEM_CODE:
                raise InputParamError('"tax_system_code" should be {}'.format(', '.join(TAX_SYSTEM_CODE)))

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def client_order_id(self) -> str:
        """

        :return: id заказа клиента
        :rtype: str
        """
        return self.body.get('client_order_id')

    @property
    def is_paid(self) -> bool:
        """

        :return: Оплачен ли заказ
        :rtype: bool
        """
        return self.body.get('is_paid')

    @property
    def cost(self) -> float:
        """

        :return: Сумма платежа в рублях
        :rtype: float
        """
        return self.body.get('cost')

    @property
    def customer(self) -> CustomerFiscalization:
        """

        :return: Информация о пользователе
        :rtype: CustomerFiscalization
        """
        return self.body.get('customer')

    @property
    def tax_system_code(self) -> int:
        """

        :return: Код системы налогообложения:

            * **1** - Общая система налогообложения
            * **2** - Упрощенная (УСН, доходы)
            * **3** - Упрощенная (УСН, доходы минус расходы)
            * **4** - Единый налог на вмененный доход (ЕНВД)
            * **5** - Единый сельскохозяйственный налог (ЕСН)
            * **6** - Патентная система налогообложения

        :rtype: int
        """
        return self.body.get('tax_system_code')


class TaxiOffer(YCBase):
    """
        Оффер в такси

        :param str offer_id: Идентификатор оффера *(Обязательный параметр)*

        :param int price_raw: Цена по офферу в валюте, указанной в договоре *(Обязательный параметр)*

        :param str price: Стоимость исполнения заявки *(Обязательный параметр)*

    """

    def __init__(self,
                 offer_id: str,
                 price_raw: int,
                 price: str):
        super().__init__()

        self.body['offer_id'] = validate_fields('offer_id', offer_id, str)
        self.body['price_raw'] = validate_fields('price_raw', price_raw, int)
        self.body['price'] = validate_fields('price', price, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def offer_id(self) -> str:
        """

        :return: Идентификатор оффера
        :rtype: str
        """
        return self.body.get('offer_id')

    @property
    def price_raw(self) -> int:
        """

        :return: Цена по офферу в валюте, указанной в договоре
        :rtype: int
        """
        return self.body.get('price_raw')

    @property
    def price(self) -> float:
        """

        :return: Стоимость исполнения заявки
        :rtype: float
        """
        return self.body.get('price')


class CurrencyRules(YCBase):
    """
        Правила отображения валюты

        :param str code: ??? ("RUB")

        :param str text: ??? ("руб.")

        :param str template: ??? ("$VALUE$ $SIGN$$CURRENCY$")

        :param str sign: ??? ("₽")

    """

    def __init__(self,
                 code: str = None,
                 text: str = None,
                 template: str = None,
                 sign: str = None):
        super().__init__()

        if code:
            self.body['code'] = validate_fields('code', code, str)
        if text:
            self.body['text'] = validate_fields('text', text, str)
        if template:
            self.body['template'] = validate_fields('template', template, str)
        if sign:
            self.body['sign'] = validate_fields('sign', sign, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def code(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('code')

    @property
    def text(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('text')

    @property
    def template(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('template')

    @property
    def sign(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('sign')


class ClaimPricing(YCBase):
    """

        :param TaxiOffer offer: Идентификатор оффера

        :param str currency: ???

        :param CurrencyRules currency_rules: ???

        :param float final_price: ??? (18, 4)

    """

    def __init__(self,
                 offer: TaxiOffer = None,
                 currency: str = None,
                 currency_rules: CurrencyRules = None,
                 final_price: float = None):
        super().__init__()

        if offer:
            self.body['offer'] = validate_fields('offer', offer, TaxiOffer)

        if currency:
            self.body['currency'] = validate_fields('currency', currency, str)

        if currency_rules:
            self.body['currency_rules'] = validate_fields('currency_rules', currency_rules, CurrencyRules)

        if final_price:
            self.body['final_price'] = validate_fields('final_price', final_price, float)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def offer(self) -> TaxiOffer:
        """

        :return: Идентификатор оффера
        :rtype: TaxiOffer
        """
        return self.body.get('offer')

    @property
    def currency(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('currency')

    @property
    def currency_rules(self) -> CurrencyRules:
        """

        :return: ???
        :rtype: CurrencyRules
        """
        return self.body.get('currency_rules')

    @property
    def final_price(self) -> float:
        """

        :return: ???
        :rtype: float
        """
        return self.body.get('final_price')


class MatchedCar(YCBase):
    """
        Информация о подобранной машине ???

        :param str taxi_class: Класс такси *(Обязательный параметр)*

        :param str client_taxi_class:  Подмененный тариф (e.g., cargo, хотя в cars cargocorp)

        :param str cargo_type: Тип грузовика

        :param int cargo_loaders: Количество грузчиков (минимум 0)

        :param bool door_to_door: Опция "от двери до двери" для тарифа "доставка"

        :param List[int] cargo_points: Значение cargo_points_field, фейковое требование для тарифа

        :param str cargo_points_field: Название требования для мультиточек

    """

    def __init__(self,
                 taxi_class: str,
                 client_taxi_class: str = None,
                 cargo_type: str = None,
                 cargo_loaders: int = None,
                 door_to_door: bool = None,
                 cargo_points: List[int] = None,
                 cargo_points_field: str = None):
        super().__init__()

        self.body['taxi_class'] = validate_fields('taxi_class', taxi_class, str)
        if client_taxi_class:
            self.body['client_taxi_class'] = validate_fields('client_taxi_class', client_taxi_class, str)
        if cargo_type:
            self.body['cargo_type'] = validate_fields('cargo_type', cargo_type, str)
        if cargo_loaders:
            self.body['cargo_loaders'] = validate_fields('cargo_loaders', cargo_loaders, int)
        if door_to_door:
            self.body['door_to_door'] = validate_fields('door_to_door', door_to_door, bool)
        if cargo_points:
            self.body['cargo_points'] = validate_fields('cargo_points', cargo_points, List[int])
        if cargo_points_field:
            self.body['cargo_points_field'] = validate_fields('cargo_points_field', cargo_points_field, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def taxi_class(self) -> str:
        """

        :return: Класс такси
        :rtype: str
        """
        return self.body.get('taxi_class')

    @property
    def client_taxi_class(self) -> str:
        """

        :return: Подмененный тариф
        :rtype: str
        """
        return self.body.get('client_taxi_class')

    @property
    def cargo_type(self) -> str:
        """

        :return: Тип грузовика
        :rtype: str
        """
        return self.body.get('cargo_type')

    @property
    def cargo_loaders(self) -> int:
        """

        :return: Количество грузчиков (минимум 0)
        :rtype: int
        """
        return self.body.get('cargo_loaders')

    @property
    def door_to_door(self) -> bool:
        """

        :return: Опция "от двери до двери" для тарифа "доставка"
        :rtype: bool
        """
        return self.body.get('door_to_door')

    @property
    def cargo_points(self) -> List[int]:
        """

        :return: Значение cargo_points_field, фейковое требование для тарифа
        :rtype: List[int]
        """
        return self.body.get('cargo_points')

    @property
    def cargo_points_field(self) -> str:
        """

        :return: Название требования для мультиточек
        :rtype: str
        """
        return self.body.get('cargo_points_field')


class HumanErrorMessage(YCBase):
    """
        Ошибка

        :param str code: Машино-понятный код ошибки *(Обязательный параметр)*

        :param str message: Локализованная информация с причиной предупреждения *(Обязательный параметр)*
    """

    def __init__(self,
                 code: str,
                 message: str):
        super().__init__()

        if code:
            self.body['code'] = validate_fields('code', code, str)
        if message:
            self.body['message'] = validate_fields('message', message, str)

    def __repr__(self):
        return '<{} code={}>'.format(self.__class__.__name__, self.code)

    @property
    def code(self) -> str:
        """

        :return: Машино-понятный код ошибки (обязательный параметр)
        :rtype: str
        """
        return self.body.get('code')

    @property
    def message(self) -> str:
        """

        :return: Локализованная информация с причиной предупреждение (обязательный параметр)
        :rtype: str
        """
        return self.body.get('message')


class ClaimWarning(YCBase):
    """
        Предупреждение

        :param str source: Откуда пришло предупреждение *(Обязательный параметр)*

            * **client_requirements** - Требования клиента
            * **taxi_requirements** - Требования такси

        :param str code: Машино-понятный код ошибки *(Обязательный параметр)*

            * **not_fit_in_car** - Товар не помещается в заявленное транспортное средство
            * **requirement_unavailable** - Некоторые из пожеланий недоступны на выбранном тарифе

        :param str message: Локализованная информация с причиной предупреждения
    """

    def __init__(self,
                 source: str,
                 code: str,
                 message: str = None):
        super().__init__()

        self.body['source'] = validate_fields('source', source, str)
        self.body['code'] = validate_fields('code', code, str)
        if message:
            self.body['message'] = validate_fields('message', message, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def source(self) -> str:
        """

        :return: source: Откуда пришло предупреждение (обязательный параметр)

            * **client_requirements** - ???
            * **taxi_requirements** - ???

        :rtype: str
        """
        return self.body.get('source')

    @property
    def code(self) -> str:
        """

        :return: Машино-понятный код ошибки  (обязательный параметр)

            * **not_fit_in_car** - ???
            * **requirement_unavailable** - ???

        :rtype: str
        """
        return self.body.get('code')

    @property
    def message(self) -> str:
        """

        :return: Локализованная информация с причиной предупреждение
        :rtype: str
        """
        return self.body.get('message')


class PerformerInfo(YCBase):
    """
        Информация об исполнителе

        :param str courier_name: Имя курьера, доставляющего посылку *(Обязательный параметр)*

        :param str legal_name: Данные о юридическом лице, осуществляющим доставку *(Обязательный параметр)*

        :param str car_model: Модель машины

        :param str car_number: Номер машины

    """

    def __init__(self,
                 courier_name: str,
                 legal_name: str,
                 car_model: str = None,
                 car_number: str = None):
        super().__init__()

        self.body['courier_name'] = validate_fields('courier_name', courier_name, str)
        self.body['legal_name'] = validate_fields('legal_name', legal_name, str)
        if car_model:
            self.body['car_model'] = validate_fields('car_model', car_model, str)
        if car_number:
            self.body['car_number'] = validate_fields('car_number', car_number, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def courier_name(self) -> str:
        """

        :return: Имя курьера, доставляющего посылку (обязательный параметр)
        :rtype: str
        """
        return self.body.get('courier_name')

    @property
    def legal_name(self) -> str:
        """

        :return: Данные о юр. лице, осуществляющим доставку  (обязательный параметр)
        :rtype: str
        """
        return self.body.get('legal_name')

    @property
    def car_model(self) -> str:
        """

        :return: Модель машины
        :rtype: str
        """
        return self.body.get('car_model')

    @property
    def car_number(self) -> str:
        """

        :return: Номер машины
        :rtype: str
        """
        return self.body.get('car_number')


class Event(YCBase):
    """
        ????

        :param str claim_id: ??? *(Обязательный параметр)*
        :param str change_type: ??? *(Обязательный параметр)*
        :param str updated_ts: ??? date-time *(Обязательный параметр)*
        :param str new_status: ???
        :param str new_price: ???
        :param str new_currency: ???

    """

    def __init__(self,
                 claim_id: str,
                 change_type: str,
                 updated_ts: str,
                 new_status: str = None,
                 new_price: str = None,
                 new_currency: str = None
                 ):
        super().__init__()

        self.body['claim_id'] = validate_fields('claim_id', claim_id, str)
        self.body['change_type'] = validate_fields('change_type', change_type, str)
        self.body['updated_ts'] = validate_fields('updated_ts', updated_ts, str)

        if new_status:
            self.body['new_status'] = validate_fields('new_status', new_status, str)
        if new_price:
            self.body['new_price'] = validate_fields('new_price', new_price, str)
        if new_currency:
            self.body['new_currency'] = validate_fields('new_currency', new_currency, str)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def claim_id(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('claim_id')

    @property
    def change_type(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('change_type')

    @property
    def updated_ts(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('updated_ts')

    @property
    def new_status(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('new_status')

    @property
    def new_price(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('new_price')

    @property
    def new_currency(self) -> str:
        """

        :return: ???
        :rtype: str
        """
        return self.body.get('new_currency')
