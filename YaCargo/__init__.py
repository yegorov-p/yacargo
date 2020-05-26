# -*- coding: utf-8 -*-
import socket
import ssl
import uuid
from typing import List

import requests
from requests.exceptions import ReadTimeout, SSLError

from YaCargo.constants import *
from YaCargo.exceptions import *
from YaCargo.objects import *
from YaCargo.objects import validate_fields
from YaCargo.response import *

__title__ = 'yaCargo'
__version__ = constants.VERSION
__author__ = 'Pasha Yegorov'
__license__ = 'Apache 2.0'

logger = logging.getLogger('yaCargo')


class YCAPI:
    """

    :param str authorization_key: Авторизационный ключ
    """

    def __init__(self, authorization_key=None):
        if not authorization_key:
            raise NotAuthorized(
                "You must provide authorization key to access cargo API!")
        self.session = requests.Session()
        self.session.headers = {
            'Host': DOMAIN,
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

        url = '{}://{}/b2b/cargo/integration/{}'.format(PROTOCOL, DOMAIN, resource)

        try:
            logger.debug('Requesting resource {}'.format(url))
            logger.debug('Requesting params {}'.format(params))
            logger.debug('Requesting body {}'.format(body))
            r = self.session.request(
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

            headers = ["'{0}: {1}'".format(k, v) for k, v in r.request.headers.items()]
            headers = " -H ".join(sorted(headers))
            command = "curl -H {headers} -d '{data}' '{uri}'".format(
                data=r.request.body or "",
                headers=headers,
                uri=r.request.url,
            )
            logger.debug('CURL: {}'.format(command))
            logger.debug('Status code {}'.format(r.status_code))
            logger.debug('Received headers: {}'.format(r.headers))

            if filename:
                with open(filename, 'wb') as f:
                    f.write(r.content)
                return (r.headers, True)
            else:
                data = r.json()
                logger.debug('Received JSON: {}'.format(data))

                if r.status_code in (400, 401, 403, 404, 409):
                    raise BaseAPIError(data)

                return (r.headers, data)

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

        :param List[CargoItemMP] items: Перечисление коробок к отправлению (Обязательный параметр)
        :param List[CargoPointMP] route_points: ??? (Обязательный параметр, минимум 2)
        :param ContactWithPhone emergency_contact: (Обязательный параметр)
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
        :param str due: Время, к которому нужно подать машину date-time
        :param str comment: Общий комментарий к заказу
        :param C2CData c2c_data: ???

        :return:  ???
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

        :param str claim_id: Uuid id (cargo_id в базе) (Обязательный параметр)

        :param List[CargoItemMP] items: Перечисление коробок к отправлению (минимум 1) (Обязательный параметр)

        :param List[CargoPointMP] route_points:         минимум 2 (Обязательный параметр)

        :param ContactWithPhone emergency_contact: (Обязательный параметр)

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

        :return: ???
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

        :param str claim_id: Uuid id (cargo_id в базе) (Обязательный параметр)

        :return: ???
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

        :param str claim_id: Uuid id (cargo_id в базе) (Обязательный параметр)

        :param int offset: Смещение (пагинация)   минимум 0 (Обязательный параметр)

        :param int limit: Лимит (пагинация) 1 -1000 (Обязательный параметр)

        :param str status: Статус заявки (список будет расширяться):
          * **new** - ???
          * **estimating** - ???
          * **estimating_failed** - ???
          * **ready_for_approval** - ???
          * **accepted** - ???
          * **performer_lookup** - ???
          * **performer_draft** - ???
          * **performer_found** - ???
          * **performer_not_found** - ???
          * **cancelled** - ???
          * **pickup_arrived** - ???
          * **ready_for_pickup_confirmation** - ???
          * **pickuped** - ???
          * **delivery_arrived** - ???
          * **ready_for_delivery_confirmation** - ???
          * **delivered** - ???
          * **pay_waiting** - ???
          * **delivered_finish** - ???
          * **returning** - ???
          * **return_arrived** - ???
          * **ready_for_return_confirmation** - ???
          * **returned** - ???
          * **returned_finish** - ???
          * **failed** - ???
          * **cancelled_with_payment** - ???
          * **cancelled_by_taxi** - ???
          * **cancelled_with_items_on_hands** - ???

        :param str created_from: Начало периода поиска (isoformat) date-time

        :param str created_to: Окончание периода поиска (isoformat) date-time

        :return: ???
        :rtype: SearchClaimsResponseMP


        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}
        body = {'offset': validate_fields('offset', offset, int),
                'limit': validate_fields('limit', limit, int)}
        if status:
            body['status'] = validate_fields('status', status, str)
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

        :param int offset: Смещение (пагинация)   минимум 0  (Обязательный параметр)

        :param int limit: Лимит (пагинация) 1 -1000  (Обязательный параметр)

        :return: ???
        :rtype: SearchClaimsResponseMP


        """

        body = {'offset': validate_fields('offset', offset, int),
                'limit': validate_fields('limit', limit, int)}

        return SearchClaimsResponseMP(self._request(resource='v2/claims/search/active', params={}, body=body))

    def claim_bulk(self,
                   claim_ids: List[str]) -> SearchClaimsResponseMP:
        """
        Поиск по заявкам

        :param List[str] claim_ids: Массив claim_id, для которых нужно отдать info 1-1000 (Обязательный параметр)

        :return: ???
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


        :return: ???
        :rtype: VoiceforwardingResponse

        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}

        return VoiceforwardingResponse(self._request(resource='v1/driver-voiceforwarding', params=params, body={}))

    def claim_document(self,
                       claim_id: str,
                       version: int,
                       status: str,
                       document_type: str = "act"):
        """
        Голосовой шлюз с водителем

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

    def claim_journal(self,
                      curson: str) -> ClaimsJournalResponse:
        """
        Subscription to journal of claims change events

        :param str curson: Cursor points to last consumed event in journal. Handler returns all
                    records registered after that event.

                    If skipped handler returns records start from first registred record
                    in journal.

        :return: ???
        :rtype: ClaimsJournalResponse

        """
        body = {'curson': validate_fields('curson', curson, str)}

        return ClaimsJournalResponse(self._request(resource='v1/claims/journal', params={}, body=body))

    def claim_document(self,
                       claim_id: str,
                       version: int,
                       status: str,
                       document_type: str = "act"):
        """
        Голосовой шлюз с водителем

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
        :param str cancel_state: Статус отмены (платная или бесплатная):
                    - free
                    - paid

        :return: ???
        :rtype: CutClaimResponse

        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}
        body = {
            'version': validate_fields('version', version, int),
            'cancel_state': validate_fields('cancel_state', cancel_state, str),
        }

        return CutClaimResponse(self._request(resource='v1/claims/journal', params=params, body=body))


    def claim_cancel(self,
                     claim_id: str) -> PerformerPositionResponse:
        """
        Получение координаты исполнителя заказа

        :param str claim_id: claim_id заявки cargo-claims (UUID)


        :return: ???
        :rtype: PerformerPositionResponse

        """
        params = {'claim_id': validate_fields('claim_id', claim_id, str)}

        return PerformerPositionResponse(self._request(resource='v1/claims/performer-position', params=params, body={}, method='get'))
