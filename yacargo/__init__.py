# -*- coding: utf-8 -*-
import logging
import socket
import ssl
import uuid
from typing import List

import requests
from requests.exceptions import ReadTimeout, SSLError

from yacargo.constants import VERSION, DOMAIN_TEST, DOMAIN, USER_AGENT, RESOURCES, PROTOCOL, CLAIM_STATUS, CANCEL_STATE
from yacargo.exceptions import NotAuthorized, NetworkAPIError, InputParamError
from yacargo.objects import validate_fields
from yacargo.response import CargoItemMP, CargoPointMP, ContactWithPhone, ClientRequirements, \
    C2CData, SearchedClaimMP, SearchClaimsResponseMP, CutClaimResponse, VoiceforwardingResponse, \
    ClaimsJournalResponse, PerformerPositionResponse

__title__ = 'yaCargo'
__version__ = VERSION
__author__ = 'Pasha Yegorov'
__license__ = 'Apache 2.0'

logger = logging.getLogger('yaCargo')


class YCAPI:
    """

    :param str authorization_key: Авторизационный ключ
    :param bool test_server: Использовать ли тестовый сервер?
    """

    def __init__(self, authorization_key=None, test_server=False):
        if not authorization_key:
            raise NotAuthorized(
                "You must provide authorization key to access cargo API!")
        self.test_server = test_server
        self.session = requests.Session()
        self.session.headers = {
            'Host': DOMAIN_TEST if self.test_server else DOMAIN,
            'Authorization': 'Bearer {}'.format(authorization_key),
            'User-agent': USER_AGENT,
            'Accept-Language': 'ru'
        }

    def _request(self, resource, params, body, filename='', method='post'):
        """

        :param str resource: Запрашиваемый ресурс
        :param dict params: Параметры
        :param dict body: Тело запроса
        :param str filename: Если указано - ответ будет сохранен в filename

        :return:
        """
        if resource not in RESOURCES:
            raise Exception('Resource "%s" unsupported' % resource)

        url = '{}://{}/b2b/cargo/integration/{}'.format(PROTOCOL, DOMAIN_TEST if self.test_server else DOMAIN, resource)

        try:
            logger.debug('Requesting resource %s', url)
            logger.debug('Requesting params %s', params)
            logger.debug('Requesting body %s', body)
            req = self.session.request(
                method=method,
                url=url,
                params=params,
                json=body
            )

        except (ConnectionError, ReadTimeout, SSLError, ssl.SSLError,
                socket.error) as exception:
            logger.error(exception)
            raise NetworkAPIError()
        else:

            headers = ["'{0}: {1}'".format(k, v) for k, v in req.request.headers.items()]
            headers = " -H ".join(sorted(headers))
            command = "curl -H {headers} -d '{data}' '{uri}'".format(
                data=req.request.body or "",
                headers=headers,
                uri=req.request.url,
            )
            logger.debug('CURL: %s', command)
            logger.debug('Status code %d', req.status_code)
            logger.debug('Received headers: %s', req.headers)

            if filename:
                with open(filename, 'wb') as file:
                    file.write(req.content)
                return req.headers, True

            data = req.json()
            logger.debug('Received JSON: %s', data)

            if req.status_code in (400, 401, 403, 404, 409):
                raise NotAuthorized(data)

            return req.headers, data

    def claim_create(self,
                     items: List[CargoItemMP],
                     route_points: List[CargoPointMP],
                     emergency_contact: ContactWithPhone,
                     shipping_document: str = '',
                     client_requirements: ClientRequirements = None,
                     callback_properties: str = None,
                     skip_door_to_door: bool = False,
                     skip_client_notify: bool = False,
                     skip_emergency_notify: bool = False,
                     optional_return: bool = False,
                     due: str = None,
                     comment: str = None,
                     c2c_data: C2CData = None) -> SearchedClaimMP:
        """
            Создание заявки с мультиточками

            :param List[CargoItemMP] items: Перечисление коробок к отправлению *(Обязательный параметр)*
            :param List[CargoPointMP] route_points: Точки маршрута *(Обязательный параметр, минимум 2)*
            :param ContactWithPhone emergency_contact: *(Обязательный параметр)*
            :param str shipping_document: Сопроводительные документы
            :param ClientRequirements client_requirements:
            :param str callback_properties:

                Параметры уведомления сервера клиента о смене статуса заявки.
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

            :param bool skip_door_to_door: Выключить опцию "От двери до двери"
            :param bool skip_client_notify: Не отправлять нотификации получателю
            :param bool skip_emergency_notify: Не отправлять нотификации emergency контакту
            :param bool optional_return: Водитель не возвращает товары в случае отмены заказа.
            :param str due: Время, к которому нужно подать машину date-time
            :param str comment: Общий комментарий к заказу
            :param C2CData c2c_data: ???

            :return: Найденная заявка
            :rtype: SearchedClaimMP

            :raises InputParamError: неверное значение параметра
        """
        params = {'request_id': uuid.uuid4().hex}
        body = {'items': validate_fields('items', items, List[CargoItemMP]),
                'route_points': validate_fields('route_points', route_points, List[CargoPointMP])}

        if len(route_points) < 2:
            raise InputParamError('"route_points" should contain at least two elements')

        body['emergency_contact'] = validate_fields('emergency_contact', emergency_contact, ContactWithPhone)

        if shipping_document:
            body['shipping_document'] = validate_fields('shipping_document', shipping_document, str)
        if client_requirements:
            body['client_requirements'] = validate_fields('client_requirements', client_requirements, ClientRequirements)
        if callback_properties:
            body['callback_properties'] = validate_fields('callback_properties', callback_properties, str)
            if not callback_properties.lower().startswith('http://') or not callback_properties.lower().startswith('https://'):
                raise InputParamError('"callback_properties" should be a valid URI')
        if skip_door_to_door:
            body['skip_door_to_door'] = validate_fields('skip_door_to_door', skip_door_to_door, bool)
        if skip_client_notify:
            body['skip_client_notify'] = validate_fields('skip_client_notify', skip_client_notify, bool)
        if skip_emergency_notify:
            body['skip_emergency_notify'] = validate_fields('skip_emergency_notify', skip_emergency_notify, bool)
        if optional_return:
            body['optional_return'] = validate_fields('optional_return', optional_return, bool)
        if due:
            body['due'] = validate_fields('due', due, str)
        if comment:
            body['comment'] = validate_fields('comment', comment, str)
        if c2c_data:
            body['c2c_data'] = validate_fields('c2c_data', c2c_data, C2CData)

        return SearchedClaimMP(self._request(resource='v2/claims/create', params=params, body=body))

    def claim_edit(self,
                   claim_id: str,
                   items: List[CargoItemMP],
                   route_points: List[CargoPointMP],
                   emergency_contact: ContactWithPhone,
                   shipping_document: str = None,
                   client_requirements: ClientRequirements = None,
                   callback_properties: str = None,
                   skip_door_to_door: bool = None,
                   skip_client_notify: bool = None,
                   skip_emergency_notify: bool = None,
                   optional_return: bool = None,
                   eta: str = None,
                   comment: str = None,
                   c2c_data: C2CData = None,
                   ) -> SearchedClaimMP:
        """
            Изменение параметров заявки с мультиточками. Метод доступен только на начальных статусах - до принятия офера клиентом

            :param str claim_id: Uuid id (cargo_id в базе) *(Обязательный параметр)*
            :param List[CargoItemMP] items: Перечисление коробок к отправлению (минимум 1) *(Обязательный параметр)*
            :param List[CargoPointMP] route_points: точки маршрута *(Обязательный параметр)*
            :param ContactWithPhone emergency_contact: *(Обязательный параметр)*
            :param str shipping_document: Сопроводительные документы
            :param ClientRequirements client_requirements:
            :param str callback_properties: Параметры уведомления сервера клиента о смене статуса заявки.

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


            :param bool skip_door_to_door: Выключить опцию "От двери до двери"
            :param bool skip_client_notify: Не отправлять нотификации получателю
            :param bool skip_emergency_notify: Не отправлять нотификации emergency контакту
            :param bool optional_return: Водитель не возвращает товары в случае отмены заказа.
            :param str eta: Время, к которому нужно подать машину date-time
            :param str comment: Общий комментарий к заказу
            :param C2CData c2c_data:

            :return: Найденная заявка
            :rtype: SearchedClaimMP
        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}
        body = {'items': validate_fields('items', items, List[CargoItemMP]),
                'route_points': validate_fields('route_points', route_points, List[CargoPointMP]),
                'emergency_contact': validate_fields('emergency_contact', emergency_contact, ContactWithPhone)}

        if emergency_contact:
            body['emergency_contact'] = validate_fields('emergency_contact', emergency_contact, ContactWithPhone)
        if shipping_document:
            body['shipping_document'] = validate_fields('shipping_document', shipping_document, str)
        if client_requirements:
            body['client_requirements'] = validate_fields('client_requirements', client_requirements, ClientRequirements)
        if callback_properties:
            body['callback_properties'] = validate_fields('callback_properties', callback_properties, str)
            if not callback_properties.lower().startswith('http://') or not callback_properties.lower().startswith('https://'):
                raise InputParamError('"callback_properties" should be a valid URI')
        if skip_door_to_door:
            body['skip_door_to_door'] = validate_fields('skip_door_to_door', skip_door_to_door, bool)
        if skip_client_notify:
            body['skip_client_notify'] = validate_fields('skip_client_notify', skip_client_notify, bool)
        if skip_emergency_notify:
            body['skip_emergency_notify'] = validate_fields('skip_emergency_notify', skip_emergency_notify, bool)
        if optional_return:
            body['optional_return'] = validate_fields('optional_return', optional_return, bool)
        if eta:
            body['eta'] = validate_fields('eta', eta, str)
        if comment:
            body['comment'] = validate_fields('comment', comment, str)
        if c2c_data:
            body['c2c_data'] = validate_fields('c2c_data', c2c_data, C2CData)

        return SearchedClaimMP(self._request(resource='v2/claims/info', params=params, body=body))

    def claim_info(self,
                   claim_id: str) -> SearchedClaimMP:
        """
            Получение полной информации о заявке

            :param str claim_id: Uuid id (cargo_id в базе) *(Обязательный параметр)*

            :return: Найденная заявка
            :rtype: SearchedClaimMP
        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}
        return SearchedClaimMP(self._request(resource='v2/claims/info', params=params, body={}))

    def claim_search(self,
                     claim_id: str,
                     offset: str = 0,
                     limit: str = 100,
                     status: str = None,
                     created_from: str = None,
                     created_to: str = None,
                     ) -> SearchClaimsResponseMP:
        """
            Поиск по заявкам

            :param str claim_id: Uuid id (cargo_id в базе) *(Обязательный параметр)*
            :param int offset: Смещение (пагинация), минимум 0 *(Обязательный параметр)*
            :param int limit: Лимит (пагинация) 1 -1000 *(Обязательный параметр)*
            :param str status: Статус заявки (список будет расширяться):

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

            :param str created_from: Начало периода поиска (isoformat) date-time
            :param str created_to: Окончание периода поиска (isoformat) date-time

            :return: Найденные заявки
            :rtype: SearchClaimsResponseMP
        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}
        body = {'offset': validate_fields('offset', offset, int),
                'limit': validate_fields('limit', limit, int)}
        if status:
            body['status'] = validate_fields('status', status, str)
            if body['status'] not in CLAIM_STATUS:
                raise InputParamError('"status" should be {}'.format(', '.join(CLAIM_STATUS)))

        if created_from:
            body['created_from'] = validate_fields('created_from', created_from, str)
        if created_to:
            body['created_to'] = validate_fields('created_to', created_to, str)
        return SearchClaimsResponseMP(self._request(resource='v2/claims/search', params=params, body=body))

    def search_active(self,
                      offset: int = 0,
                      limit: int = 100) -> SearchClaimsResponseMP:
        """
            Тело запроса поиска активных заявок

            :param int offset: Смещение (пагинация), минимум 0 *(Обязательный параметр)*
            :param int limit: Лимит (пагинация) 1-1000 *(Обязательный параметр)*

            :return: Найденные заявки
            :rtype: SearchClaimsResponseMP
        """

        body = {'offset': validate_fields('offset', offset, int),
                'limit': validate_fields('limit', limit, int)}

        return SearchClaimsResponseMP(self._request(resource='v2/claims/search/active', params={}, body=body))

    def claim_bulk(self,
                   claim_ids: List[str]) -> SearchClaimsResponseMP:
        """
            Поиск по заявкам

            :param List[str] claim_ids: Массив claim_id, для которых нужно отдать сведения 1-1000 *(Обязательный параметр)*

            :return: Найденные заявки
            :rtype: SearchClaimsResponseMP
        """
        body = {'claim_ids': validate_fields('claim_ids', claim_ids, List[str])}

        return SearchClaimsResponseMP(self._request(resource='v2/   claims/bulk_info', params={}, body=body))

    def claim_accept(self,
                     claim_id: str,
                     version: int) -> CutClaimResponse:
        """
            Пометка заявки как подтвержденной

            :param str claim_id: claim_id заявки cargo-claims (UUID)
            :param int version: Версия, для которой меняем статус

            :return: ???
            :rtype: CutClaimResponse
        """
        params = {'claim_ids': validate_fields('claim_id', claim_id, str)}
        body = {'version': validate_fields('version', version, int)}

        return CutClaimResponse(self._request(resource='v1/claims/accept', params=params, body=body))

    def voiceforwarding(self,
                        claim_id: str) -> VoiceforwardingResponse:
        """
        Голосовой шлюз с водителем

        :param str claim_id: claim_id заявки cargo-claims (UUID)

        :return: Информация о временном телефонном номере
        :rtype: VoiceforwardingResponse

        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}

        return VoiceforwardingResponse(self._request(resource='v1/driver-voiceforwarding', params=params, body={}))

    def claim_journal(self,
                      cursor: str) -> ClaimsJournalResponse:
        """
            Subscription to journal of claims change events

            :param str cursor: Позиция курсора, с которой должен быть передан журнал

            :return: ???
            :rtype: ClaimsJournalResponse
        """
        body = {'cursor': validate_fields('cursor', cursor, str)}

        return ClaimsJournalResponse(self._request(resource='v1/claims/journal', params={}, body=body))

    def claim_document(self,
                       claim_id: str,
                       version: int,
                       status: str,
                       document_type: str = "act"):
        """
            Получить накладную или акт приёма-передачи

            :param str claim_id:  заявки cargo-claims (UUID)
            :param str document_type: Тип документа
            :param int version: version
            :param str status: Статус заявки

            :return: ???
            :rtype: bool
        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str),
                  'document_type': validate_fields('document_type', document_type, str),
                  'version': validate_fields('version', version, int),
                  'status': validate_fields('status', status, str)
                  }

        return self._request(resource='v1/claims/document', params=params, body={}, filename='asd.pdf')

    def claim_cancel(self,
                     claim_id: str,
                     version: int,
                     cancel_state: str) -> CutClaimResponse:
        """
            Пометка заявки как отмененной

            :param str claim_id: claim_id заявки cargo-claims (UUID)
            :param int version: Версия, для которой меняем статус
            :param str cancel_state: Статус отмены:

                * **free** - бесплатная отмена
                * **paid** - платная отмена

            :return: ???
            :rtype: CutClaimResponse
        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}

        body = {
            'version': validate_fields('version', version, int),
            'cancel_state': validate_fields('cancel_state', cancel_state, str),
        }

        if cancel_state not in CANCEL_STATE:
            raise InputParamError('"cancel_state" should be {}'.format(', '.join(CANCEL_STATE)))

        return CutClaimResponse(self._request(resource='v1/claims/cancel', params=params, body=body))

    def performer_position(self,
                           claim_id: str) -> PerformerPositionResponse:
        """
            Получение координаты исполнителя заказа

            :param str claim_id: claim_id заявки cargo-claims (UUID)

            :return: Позиция исполнителя
            :rtype: PerformerPositionResponse
        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}

        return PerformerPositionResponse(self._request(resource='v1/claims/performer-position', params=params, body={}, method='get'))
