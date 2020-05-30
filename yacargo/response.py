# -*- coding: utf-8 -*-
import logging
from typing import List, Optional

from yacargo.objects import CargoItemMP, CargoItemSizes, CargoPointMP, \
    ContactOnPoint, CargoPointAddress, HumanErrorMessage, ContactWithPhone, \
    TaxiOffer, ClaimPricing, CurrencyRules, ClientRequirements, MatchedCar, \
    ClaimWarning, PerformerInfo, C2CData, Event

logger = logging.getLogger('yacargo')


class Base():
    def __init__(self, data):
        if isinstance(data, dict):
            self.resp = data
            self.headers = {}
        else:
            (self.headers, self.resp) = data

    def json(self) -> dict:
        """

        :return: ответ в формате JSON
        :rtype: dict
        """
        return self.resp


class SearchedClaimMP(Base):
    """
        Найденная заявка
    """

    def __repr__(self):
        return '<{} id={}>'.format(self.__class__.__name__, self.claim_id)

    @property
    def claim_id(self) -> str:
        """

        :return: Uuid id (cargo_id в базе)
        :rtype: str
        """
        return self.resp.get('id')

    @property
    def corp_client_id(self) -> str:
        """

        :return: Id клиента в корп кабинете (32)
        :rtype: str
        """
        return self.resp.get('corp_client_id')

    @property
    def yandex_uid(self) -> Optional[str]:
        """

        :return: yandex uid
        :rtype: Optional[str]
        """
        return self.resp.get('yandex_uid')

    @property
    def items(self) -> List[CargoItemMP]:
        """

        :return: Перечисление коробок к отправлению (минимум 1 )
        :rtype: List[CargoItemMP]
        """
        result = []
        for item in self.resp.get('items'):
            size = item.get('size')
            if size:
                cargoitem = CargoItemSizes(length=size.get('length'),
                                           width=size.get('width'),
                                           height=size.get('height'))
            else:
                cargoitem = None
            result.append(CargoItemMP(pickup_point=item.get('pickup_point'),
                                      droppof_point=item.get('droppof_point'),
                                      title=item.get('title'),
                                      cost_value=item.get('cost_value'),
                                      cost_currency=item.get('cost_currency'),
                                      quantity=item.get('quantity'),
                                      extra_id=item.get('extra_id'),
                                      size=cargoitem,
                                      weight=item.get('weight'),
                                      fiscalization=item.get('fiscalization'),
                                      )
                          )

        return result

    @property
    def route_points(self) -> List[CargoPointMP]:
        """

        :return: Список точек для заявки с мультиточками (минимум 2)
        :rtype: List[CargoPointMP]
        """
        result = []
        for item in self.resp.get('route_points'):
            contact = item.get('contact')
            address = item.get('address')
            result.append(CargoPointMP(
                point_id=item.get('id'),
                visit_order=item.get('visit_order'),
                contact=ContactOnPoint(name=contact.get('name'),
                                       phone=contact.get('phone'),
                                       email=contact.get('email')),
                address=CargoPointAddress(fullname=address.get('fullname'),
                                          coordinates=address.get('coordinates'),
                                          country=address.get('country'),
                                          city=address.get('city'),
                                          street=address.get('street'),
                                          building=address.get('building'),
                                          porch=address.get('porch'),
                                          sfloor=address.get('sfloor'),
                                          sflat=address.get('sflat'),
                                          door_code=address.get('door_code'),
                                          uri=address.get('uri'),
                                          ),
                point_type=item.get('type'),
                skip_confirmation=item.get('skip_confirmation'),
                payment_on_delivery=item.get('payment_on_delivery'),
                external_order_id=item.get('external_order_id'),
                pickup_code=item.get('pickup_code'),
                visit_status=item.get('visit_status')
                ))
        return result

    @property
    def current_point_id(self) -> Optional[int]:
        """

        :return: Уникальный идентификатор точки (id в таблице claim_points)
        :rtype: Optional[int]
        """
        return self.resp.get('current_point_id')

    @property
    def status(self) -> str:
        """

        :return: Статус
        :rtype: str
        """
        return self.resp.get('status')

    @property
    def version(self) -> int:
        """

        :return: Версия
        :rtype: int
        """
        return self.resp.get('version')

    @property
    def error_messages(self) -> List[HumanErrorMessage]:
        """

        :return: Сообщения об ошибках
        :rtype: List[HumanErrorMessage]
        """
        result = []
        for i in self.resp.get('error_messages', []):
            result.append(HumanErrorMessage(code=i.get('code'),
                                            message=i.get('message')))
        return result

    @property
    def emergency_contact(self) -> ContactWithPhone:
        """

        :return: Контакт для экстренной связи
        :rtype: ContactWithPhone
        """
        data = self.resp.get('emergency_contact')
        return ContactWithPhone(name=data['name'],
                                phone=data['phone'])

    @property
    def skip_door_to_door(self) -> bool:
        """

        :return: Выключить опцию "От двери до двери"
        :rtype: bool
        """
        return self.resp.get('skip_door_to_door')

    @property
    def skip_client_notify(self) -> bool:
        """

        :return: Не отправлять нотификации получателю
        :rtype: bool
        """
        return self.resp.get('skip_client_notify')

    @property
    def skip_emergency_notify(self) -> bool:
        """

        :return: Не отправлять нотификации emergency контакту
        :rtype: bool
        """
        return self.resp.get('skip_emergency_notify')

    @property
    def optional_return(self) -> bool:
        """

        :return: Водитель не возвращает товары в случае отмены заказа.
        :rtype: bool
        """
        return self.resp.get('optional_return')

    @property
    def eta(self) -> Optional[int]:
        """

        :return: Ожидаемое время исполнения заказа в минутах
        :rtype: Optional[int]
        """
        return self.resp.get('eta')

    @property
    def created_ts(self) -> str:
        """

        :return: Дата-время создания
        :rtype: str
        """
        return self.resp.get('created_ts')

    @property
    def updated_ts(self) -> str:
        """

        :return: Дата-время последнего обновления date-time
        :rtype: str
        """
        return self.resp.get('updated_ts')

    @property
    def taxi_offer(self) -> Optional[TaxiOffer]:
        """

        :return: ???
        :rtype: Optional[TaxiOffer]
        """
        data = self.resp.get('taxi_offer')
        if data:
            return TaxiOffer(offer_id=data.get('offer_id'),
                             price_raw=data.get('price_raw'),
                             price=data.get('price'))
        return None

    @property
    def pricing(self) -> Optional[ClaimPricing]:
        """

        :return: ???
        :rtype: Optional[ClaimPricing]
        """
        data = self.resp.get('pricing')
        if data:
            offer = self.resp.get('offer')
            if offer:
                taxioffer = TaxiOffer(offer_id=offer.get('offer_id'),
                                      price_raw=offer.get('price_raw'),
                                      price=offer.get('price'))
            else:
                taxioffer = None

            currency_rules = self.resp.get('currency_rules')
            if currency_rules:
                currency_rules = CurrencyRules(code=currency_rules.get('code'),
                                               text=currency_rules.get('text'),
                                               template=currency_rules.get('template'),
                                               sign=currency_rules.get('sign'),
                                               )
            else:
                currency_rules = None
            return ClaimPricing(offer=taxioffer,
                                currency=data.get('currency'),
                                currency_rules=currency_rules,
                                final_price=data.get('final_price'))
        return None

    @property
    def available_cancel_state(self) -> Optional[str]:
        """

        :return: Актуальный статус возможности отмены заказа

            * **free** - бесплатная отмена
            * **paid** - платная отмена

        :rtype: Optional[str]
        """
        return self.resp.get('available_cancel_state')

    @property
    def client_requirements(self) -> Optional[ClientRequirements]:
        """

        :return: Требования клиента
        :type: Optional[ClientRequirements]
        """
        data = self.resp.get('client_requirements')
        if data:
            return ClientRequirements(taxi_class=data.get('taxi_class'),
                                      cargo_type=data.get('cargo_type'),
                                      cargo_loaders=data.get('cargo_loaders'))
        return None


    @property
    def matched_cars(self) -> Optional[List[MatchedCar]]:
        """

        :return: Информация о подобранных машинах
        :rtype: Union[List[MatchedCar],None]
        """
        if self.resp.get('matched_cars'):
            result = []
            for data in self.resp.get('matched_cars'):
                result.append(MatchedCar(taxi_class=data.get('taxi_class'),
                                         client_taxi_class=data.get('client_taxi_class'),
                                         cargo_type=data.get('cargo_type'),
                                         cargo_loaders=data.get('cargo_loaders'),
                                         door_to_door=data.get('door_to_door'),
                                         cargo_points=data.get('cargo_points'),
                                         cargo_points_field=data.get('cargo_points_field'))
                              )
            return result
        return None

    @property
    def warnings(self) -> Optional[List[ClaimWarning]]:
        """

        :return: Предупреждения по заявке
        :rtype: Optional[List[ClaimWarning]]
        """
        if self.resp.get('warnings'):
            result = []
            for data in self.resp.get('warnings'):
                result.append(ClaimWarning(source=data.get('source'),
                                           code=data.get('code'),
                                           message=data.get('message'))
                              )
            return result
        return None

    @property
    def performer_info(self) -> Optional[PerformerInfo]:
        """

        :return: Информация об исполнителе
        :rtype: Optional[PerformerInfo]
        """
        data = self.resp.get('performer_info')
        if data:
            return PerformerInfo(courier_name=data.get('courier_name'),
                                 legal_name=data.get('legal_name'),
                                 car_model=data.get('car_model'),
                                 car_number=data.get('car_number'))
        return None

    @property
    def callback_properties(self) -> Optional[str]:
        """

        :return: Параметры уведомления сервера клиента о смене статуса заявки.

            Уведомление представляет собой POST-запрос по указанному url, к
            которому будут добавлены информация о дате последнего изменения
            заявки и идентификатор заказа в системе b2b cargo в виде
            'updated_ts=<ISO-8601>&claim_id=<id заказа>', то есть url вида
            'https://example.com/?my_order_id=123&' будет расширен до
            'https://example.com/?my_order_id=123&updated_ts=...&claim_id=...'.

            Важно! Параметры добавляются конкатенацией к callback_url, то есть
            url вида 'https://example.com' превратится в невалидный
            'https://example.comupdated_ts=...&claim_id=...'.

            Поддерживаются только http и https. При https ssl-сертификат должен
            быть выдан известным серверу центром сертификации.

            К уведомлениям следует относиться как к push ahead of polling, как
            к ускорению получения информации о смене статусов. Сервер ожидает
            ответ 200, при таймаутах или любом другом ответе какое-то время
            будет пытаться доставить уведомление, после чего прекратит попытки.
            То есть, для надёжного получения статуса по заявке клиенту
            необходимо запрашивать информацию из ручки v1/claims/info.

            Клиенту следует учесть, что ответ ручки v1/claims/info может
            содержать более старое состояние заявки (надо ориентироваться на
            значение поля updated_ts). В этом случает необходимо повторить
            вызов ручки через некоторое время (от 5 до 30 секунд).

        :rtype: Optional[str]
        """
        return self.resp.get('callback_properties')

    @property
    def due(self) -> Optional[str]:
        """

        :return: Время, к которому нужно подать машину date-time
        :rtype: Optional[str]
        """
        return self.resp.get('due')

    @property
    def shipping_document(self) -> Optional[str]:
        """

        :return: Сопроводительные документы
        :rtype: Optional[str]
        """
        return self.resp.get('shipping_document')

    @property
    def comment(self) -> Optional[str]:
        """

        :return: Общий комментарий к заказу
        :rtype: Optional[str]
        """
        return self.resp.get('comment')

    @property
    def c2c_data(self) -> Optional[C2CData]:
        """

        :return: ???
        :rtype: Optional[C2CData]
        """
        data = self.resp.get('c2c_data')
        if data:
            return C2CData(payment_type=data.get('payment_type'),
                           payment_method_id=data.get('payment_method_id'))
        return None


class SearchClaimsResponseMP(Base):
    """
        Найденные заявки

    """
    @property
    def claims(self) -> List[SearchedClaimMP]:
        """

        :return: Найденные заявки
        :rtype: List[SearchedClaimMP]
        """
        return [SearchedClaimMP(claim) for claim in self.resp.get('claims')]


class CutClaimResponse(Base):
    """
        ???

    """
    def __repr__(self):
        return '<{} id={}>'.format(self.__class__.__name__, self.claim_id)

    @property
    def claim_id(self) -> str:
        """

        :return: Uuid id (cargo_id в базе)
        :rtype: str
        """
        return self.resp.get('id')

    @property
    def status(self) -> str:
        """

        :return: Статус заявки (список будет расширяться):

            * **new** - новая заявка
            * **estimating** - идет процесс оценки заявки (подбор типа автомобиля по параметрам груза и расчет стоимости)
            * **estimating_failed** - не удалось оценить заявку. Причину можно увидеть в error_messages в ответе ручки /info
            * **ready_for_approval** - заявка успешно оценена и ожидает подтверждения от клиента
            * **accepted** - заявка подтверждена клиентом
            * **performer_lookup** - заявка взята в обработку. Промежуточный статус перед созданием заказа
            * **performer_draft** - идет поиск водителя
            * **performer_found** - водитель найден и едет в точку А
            * **performer_not_found** - не удалось найти водителя. Можно попробовать снова через некоторое время
            * **cancelled** - заказ был отменен клиентом бесплатно
            * **pickup_arrived** - водитель приехал на точку А
            * **ready_for_pickup_confirmation** - водитель ждет, когда отправитель назовет ему код подтверждения
            * **pickuped** - водитель успешно забрал груз
            * **delivery_arrived** - водитель приехал на точку Б
            * **ready_for_delivery_confirmation** - водитель ждет, когда получатель назовет ему код подтверждения
            * **delivered** - водитель успешно доставил груз (ввел смс код). Код приходит после оплаты, если была оплата при получении.
            * **pay_waiting** - заказ ожидает оплаты (актуально для оплаты при получении)
            * **delivered_finish** - заказ завершен
            * **returning** -  водителю пришлось вернуть груз и он едет в точку возврата
            * **return_arrived** - водитель приехал на точку возврата
            * **ready_for_return_confirmation** - водитель в точке возврата ожидает, когда ему назовут код подтверждения
            * **returned** - водитель успешно вернул груз (ввел смс код)
            * **returned_finish** - заказ завершен
            * **failed** - терминальный статус, не удалось начать выполнение заказа
            * **cancelled_with_payment** - заказ был отменен клиентом платно (водитель уже приехал)
            * **cancelled_by_taxi** - водитель отменил заказ (до получения груза)
            * **cancelled_with_items_on_hands** - клиент платно отменил заявку без необходимости возврата груза (заявка была создана с флагом optional_return)

        :rtype: str
        """
        return self.resp.get('status')

    @property
    def version(self) -> int:
        """

        :return: Версия
        :rtype: int
        """
        return self.resp.get('version')

    @property
    def taxi_order_id(self) -> str:
        """

        :return: taxi_order_id в такси (uuid)
        :rtype: str
        """
        return self.resp.get('taxi_order_id')


class VoiceforwardingResponse(Base):
    """
        Информация о временном телефонном номере
    """

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def phone(self) -> str:
        """

        :return: Номер телефона
        :rtype: str
        """
        return self.resp.get('phone')

    @property
    def ext(self) -> str:
        """

        :return: Добавочный номер
        :rtype: str
        """
        return self.resp.get('ext')

    @property
    def ttl_seconds(self) -> int:
        """

        :return: Время, в течение которого этот номер действителен
        :rtype: int
        """
        return self.resp.get('ttl_seconds')


class ClaimsJournalResponse(Base):
    """
        ???

    """

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def delay(self) -> str:
        """

        :return: Количество секунд, которое должно пройти до следующего запроса
        :rtype: int
        """
        return self.headers.get('X-Polling-Delay-Ms')

    @property
    def cursor(self) -> str:
        """

        :return: Позиция курсора, которая должна быть передана клиентом при следующем запросе
        :rtype: str
        """
        return self.resp.get('cursor')

    @property
    def events(self) -> List[Event]:
        """

        :return: ???
        :rtype: List[Event]
        """
        return self.resp.get('events')


class PerformerPositionResponse(Base):
    """
        Позиция исполнителя

    """

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def lat(self) -> float:
        """

        :return: Широта
        :rtype: float
        """
        position = self.resp.get('position')
        if position:
            return position.get('lat')
        return None

    @property
    def lon(self) -> float:
        """

        :return: Долгота
        :rtype: float
        """
        position = self.resp.get('position')
        if position:
            return position.get('lon')
        return None

    @property
    def timestamp(self) -> int:
        """

        :return: Время снятия сигнала GPS, unix-time
        :rtype: int
        """
        position = self.resp.get('position')
        if position:
            return position.get('timestamp')
        return None

    @property
    def speed(self) -> float:
        """

        :return: Средняя скорость, в м/с
        :rtype: float
        """
        position = self.resp.get('position')
        if position:
            return position.get('speed')
        return None

    @property
    def direction(self) -> float:
        """

        :return: Направление. Угол от 0 градусов до 360 градусов.
        :rtype: float
        """
        position = self.resp.get('position')
        if position:
            return position.get('direction')
        return None
