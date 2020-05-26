# -*- coding: utf-8 -*-
from YaCargo.objects import *
from typing import List, Optional

logger = logging.getLogger('YaCargo')

class Base(object):
    def __init__(self, data):
        if type(data) is dict:
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

        :return: Перечисление коробок к отправлению (vминимум 1 )
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
            )
            )

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

        :return: ???
        :rtype: str
        """
        return self.resp.get('status')

    @property
    def version(self) -> int:
        """

        :return: ???
        :rtype: int
        """
        return self.resp.get('version')

    @property
    def error_messages(self) -> List[HumanErrorMessage]:
        """

        :return: ???
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

        :return: ???
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

    @property
    def available_cancel_state(self) -> Optional[str]:
        """

        :return: Актуальный статус возможности отмены заказа
            - free
            - paid
        :rtype: Optional[str]
        """
        return self.resp.get('available_cancel_state')

    @property
    def client_requirements(self) -> Optional[ClientRequirements]:
        """

        :return: ???
        :type: Optional[ClientRequirements]
        """
        data = self.resp.get('client_requirements')
        if data:
            return ClientRequirements(taxi_class=data.get('taxi_class'),
                                      cargo_type=data.get('cargo_type'),
                                      cargo_loaders=data.get('cargo_loaders'))

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


class SearchClaimsResponseMP(Base):
    @property
    def claims(self) -> List[SearchedClaimMP]:
        """

        :return: ???
        :rtype: List[SearchedClaimMP]
        """

        return [SearchedClaimMP(claim) for claim in self.resp.get('claims')]


class CutClaimResponse(Base):
    """


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
          - new
          - estimating
          - estimating_failed
          - ready_for_approval
          - accepted
          - performer_lookup
          - performer_draft
          - performer_found
          - performer_not_found
          - cancelled
          - pickup_arrived
          - ready_for_pickup_confirmation
          - pickuped
          - delivery_arrived
          - ready_for_delivery_confirmation
          - delivered
          - pay_waiting
          - delivered_finish
          - returning
          - return_arrived
          - ready_for_return_confirmation
          - returned
          - returned_finish
          - failed
          - cancelled_with_payment
          - cancelled_by_taxi
          - cancelled_with_items_on_hands

        :rtype: str
        """
        return self.resp.get('status')

    @property
    def version(self) -> int:
        """

        :return: ???
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


    """

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @property
    def delay(self) -> str:
        """

        :return: Delay in milliseconds client should wait before performing new
                                request. Server can return 429 Too Often if client ignores
                                polling-delay policy.
        :rtype: int
        """
        return self.headers.get('X-Polling-Delay-Ms')

    @property
    def cursor(self) -> str:
        """

        :return: Номер телефона
        :rtype: str
        """
        return self.resp.get('cursor')

    @property
    def events(self) -> List[Event]:
        """

        :return: New position which client must pass in next request.
        :rtype: List[Event]
        """
        return self.resp.get('events')


class PerformerPositionResponse(Base):
    """


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

    @property
    def lon(self) -> float:
        """

        :return: Долгота
        :rtype: float
        """
        position = self.resp.get('position')
        if position:
            return position.get('lon')

    @property
    def timestamp(self) -> int:
        """

        :return: Время снятия сигнала GPS, unix-time
        :rtype: int
        """
        position = self.resp.get('position')
        if position:
            return position.get('timestamp')

    @property
    def speed(self) -> float:
        """

        :return: Средняя скорость, в м/с
        :rtype: float
        """
        position = self.resp.get('position')
        if position:
            return position.get('speed')

    @property
    def direction(self) -> float:
        """

        :return: Направление. Угол от 0 градусов до 360 градусов.
        :rtype: float
        """
        position = self.resp.get('position')
        if position:
            return position.get('direction')

