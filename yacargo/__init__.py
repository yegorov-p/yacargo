# -*- coding: utf-8 -*-
"""
Модуль с запросами для сервера API
"""
import socket
import ssl

import requests
from requests.exceptions import ReadTimeout, SSLError

from yacargo.exceptions import NotAuthorized, NetworkAPIError, InputParamError, BaseAPIError
from yacargo.objects import *

USER_AGENT = 'yacargo'
DOMAIN = 'b2b.taxi.yandex.net'
DOMAIN_TEST = 'b2b.taxi.tst.yandex.net'

__title__ = 'yaCargo'
__version__ = '0.0.6'
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
        # if resource not in RESOURCES:
        #    raise Exception('Resource "%s" unsupported' % resource)

        url = 'https://{}{}'.format(DOMAIN_TEST if self.test_server else DOMAIN, resource)

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
                data=req.request.body.decode() or "",
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

            if req.status_code == 403:
                raise NotAuthorized(data)

            if req.status_code in (400, 401, 404, 409):
                raise BaseAPIError(data)

            return data

    def claim_accept(self,
                     claim_id: str = None,
                     version: int = None,
                     ) -> CutClaimResponse:
        """

        Подтверждение заявки

        Подтверждает заявку при успешной оценке. После подтверждения заявки сервис запустит процесс поиска исполнителя. Предложение pricing.offer действительно в течение ограниченного времени. Если предложение более недействительно, то заказ перейдет в статус performer_not_found.

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)*
        :param int version: Версия заявки. Изменяется после редактирования заявки *(Обязательный параметр)* (1)

        `Официальная документация /b2b/cargo/integration/v1/claims/accept <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/claims/IntegrationV1ClaimsAccept-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            params["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <claim_accept> is a required parameter")

        if version is not None:
            body["version"] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <claim_accept> is a required parameter")

        item = self._request(resource="/b2b/cargo/integration/v1/claims/accept", params=params, body=body, method="post")
        return CutClaimResponse(id=item.get("id", None),
                                status=item.get("status", None),
                                version=item.get("version", None),
                                taxi_order_id=item.get("taxi_order_id", None),
                                )

    def claim_cancel(self,
                     claim_id: str = None,
                     version: int = None,
                     cancel_state: str = None,
                     ) -> CutClaimResponse:
        """

        Отмена заявки

        Отменяет заявку, которая была подтверждена. Операция может быть выполнена в течение ограниченного времени. Отмена заявки может быть платной и бесплатной. Чтобы узнать тип отмены, используйте операцию получения информации по заявке claims/info в поле available_cancel_state.

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)*
        :param int version: Версия отменяемой заявки *(Обязательный параметр)* (1)
        :param str cancel_state: Статус отмены (платная или бесплатная) *(Обязательный параметр)* (free)

            * **free** - бесплатная отмена
            * **paid** - платная отмена


        `Официальная документация /b2b/cargo/integration/v1/claims/cancel <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/claims/IntegrationV1ClaimsCancelC-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            params["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <claim_cancel> is a required parameter")

        if version is not None:
            body["version"] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <claim_cancel> is a required parameter")

        if cancel_state is not None:
            body["cancel_state"] = validate_fields('cancel_state', cancel_state, str)
        if cancel_state is None:
            raise InputParamError("<cancel_state> (=>cancel_state) of <claim_cancel> is a required parameter")

        if cancel_state not in ['free', 'paid']:
            raise InputParamError("<cancel_state> of <claim_cancel> should be in ['free', 'paid']")

        item = self._request(resource="/b2b/cargo/integration/v1/claims/cancel", params=params, body=body, method="post")
        return CutClaimResponse(id=item.get("id", None),
                                status=item.get("status", None),
                                version=item.get("version", None),
                                taxi_order_id=item.get("taxi_order_id", None),
                                )

    def claim_document(self,
                       claim_id: str = None,
                       document_type: str = None,
                       version: int = None,
                       status: str = None,
                       ) -> str:
        """

        Получение накладной или акта приема-передачи

        Возвращает ЭТН в формате PDF. Операцию можно выполнить после того, как на заказ будет найден исполнитель. Электронные цифровые подписи добавляются в документ в процессе выполнения заказа. Если по какой-то причине требуется перейти на бумажный акт, то с помощью данной операции можно получить частично подписанный документ.

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)*
        :param str document_type: Тип документа (на данный момент поддерживается только act) *(Обязательный параметр)*

            * **act** - акт

        :param int version: Версия заявки *(Обязательный параметр)*
        :param str status: Статус заявки *(Обязательный параметр)*

        `Официальная документация /b2b/cargo/integration/v1/claims/document <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/claims/IntegrationV1ClaimsDocument-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            params["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <claim_document> is a required parameter")

        if document_type is not None:
            params["document_type"] = validate_fields('document_type', document_type, str)
        if document_type is None:
            raise InputParamError("<document_type> (=>document_type) of <claim_document> is a required parameter")

        if document_type not in ['act']:
            raise InputParamError("<document_type> of <claim_document> should be in ['act']")

        if version is not None:
            params["version"] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <claim_document> is a required parameter")

        if status is not None:
            params["status"] = validate_fields('status', status, str)
        if status is None:
            raise InputParamError("<status> (=>status) of <claim_document> is a required parameter")

        return self._request(resource="/b2b/cargo/integration/v1/claims/document", params=params, body=body, method="get")

    def claim_journal(self,
                      cursor: str = None,
                      ) -> ClaimsJournalResponse:
        """

        Журнал изменений заказа

        Возвращает историю изменения заявки. Вы можете узнать об изменении статусов и цены заказа. Для терминальных статусов возвращается поле resolution, возможные значения success, failed.

        :param Optional[str] cursor: Строка с идентификатором последнего изменения, полученного клиентом. Если cursor не передан, то будут выданы все изменения для данного клиента с некоторым лимитом

        `Официальная документация /b2b/cargo/integration/v1/claims/journal <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/claims/IntegrationV1ClaimsJournal-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if cursor is not None:
            body["cursor"] = validate_fields('cursor', cursor, str)

        item = self._request(resource="/b2b/cargo/integration/v1/claims/journal", params=params, body=body, method="post")
        return ClaimsJournalResponse(cursor=item.get("cursor", None),
                                     events=item.get("events", None),
                                     )

    def voiceforwarding(self,
                        claim_id: str = None,
                        ) -> VoiceforwardingResponse:
        """

        Получение номера телефона для звонка водителю

        Возвращает номер телефона для звонка водителю, который выполняет заявку.

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)*

        `Официальная документация /b2b/cargo/integration/v1/driver-voiceforwarding <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/performer/IntegrationV1DriverVoiceForwarding-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            body["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <voiceforwarding> is a required parameter")

        item = self._request(resource="/b2b/cargo/integration/v1/driver-voiceforwarding", params=params, body=body, method="post")
        return VoiceforwardingResponse(phone=item.get("phone", None),
                                       ext=item.get("ext", None),
                                       ttl_seconds=item.get("ttl_seconds", None),
                                       )

    def performer_position(self,
                           claim_id: str = None,
                           ) -> PerformerPositionResponse:
        """

        Получение позиции исполнителя заявки

        Возвращает координаты, скорость и направления движения исполнителя заявки.

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)*

        `Официальная документация /b2b/cargo/integration/v1/claims/performer-position <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/performer/IntegrationV1ClaimsPerformerPosition-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            params["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <performer_position> is a required parameter")

        item = self._request(resource="/b2b/cargo/integration/v1/claims/performer-position", params=params, body=body, method="get")
        return PerformerPositionResponse(position_lat=item.get("position", {}).get("lat", None),
                                         position_lon=item.get("position", {}).get("lon", None),
                                         position_timestamp=item.get("position", {}).get("timestamp", None),
                                         position_accuracy=item.get("position", {}).get("accuracy", None),
                                         position_speed=item.get("position", {}).get("speed", None),
                                         position_direction=item.get("position", {}).get("direction", None),
                                         )

    def report_generate(self,
                        since_date: str = None,
                        till_date: str = None,
                        lang: str = None,
                        department_id: str = None,
                        idempotency_token: str = None,
                        ) -> ClaimsReportGenerateResponse:
        """

        Инициализация создания отчета по заявкам за период

        Инициализирует создания отчета. Отчет генерируется ассинхронно 

        :param str since_date: Дата начала отчетного периода *(Обязательный параметр)* (2020-01-01)
        :param str till_date: Дата конца отчетного периода *(Обязательный параметр)* (2020-01-02)
        :param Optional[str] lang: Язык, на котором надо генерировать отчет. Если не указан, будет использован Accept-Language  (ru)
        :param Optional[str] department_id: ID отдела (значение игнорируется). Поле нужно для совместимости с API КК
        :param str idempotency_token: Уникальный для данного клиента токен идемпотентности *(Обязательный параметр)* (f9b4825f45f64914affaeb07fbae9757)

        `Официальная документация /api/integration/v1/order-report/generate <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/reports/IntegrationV1OrderReportGenerate-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if since_date is not None:
            body["since_date"] = validate_fields('since_date', since_date, str)
        if since_date is None:
            raise InputParamError("<since_date> (=>since_date) of <report_generate> is a required parameter")

        if till_date is not None:
            body["till_date"] = validate_fields('till_date', till_date, str)
        if till_date is None:
            raise InputParamError("<till_date> (=>till_date) of <report_generate> is a required parameter")

        if lang is not None:
            body["lang"] = validate_fields('lang', lang, str)

        if department_id is not None:
            body["department_id"] = validate_fields('department_id', department_id, str)

        if idempotency_token is not None:
            body["idempotency_token"] = validate_fields('idempotency_token', idempotency_token, str)
        if idempotency_token is None:
            raise InputParamError("<idempotency_token> (=>idempotency_token) of <report_generate> is a required parameter")

        item = self._request(resource="/b2b/cargo/integration/v1/order-report/generate", params=params, body=body, method="post")
        return ClaimsReportGenerateResponse(task_id=item.get("task_id", None),
                                            )

    def report_status(self,
                      task_id: str = None,
                      ) -> ClaimsReportStatusResponse:
        """

        Проверка статуса отчета

        Возвращает состояние отчета

        :param str task_id: ID, полученный в результате успешного выполнения операции v1/order-report/generate *(Обязательный параметр)* (f9b4825f45f4914affaeb07fbae9757)

        `Официальная документация /api/integration/v1/order-report/status <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/reports/IntegrationV1OrderReportStatus-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if task_id is not None:
            body["task_id"] = validate_fields('task_id', task_id, str)
        if task_id is None:
            raise InputParamError("<task_id> (=>task_id) of <report_status> is a required parameter")

        item = self._request(resource="/b2b/cargo/integration/v1/order-report/status", params=params, body=body, method="post")
        return ClaimsReportStatusResponse(task_id=item.get("task_id", None),
                                          status=item.get("status", None),
                                          author=item.get("author", None),
                                          created_at=item.get("created_at", None),
                                          request_since_date=item.get("request", {}).get("since_date", None),
                                          request_till_date=item.get("request", {}).get("till_date", None),
                                          request_lang=item.get("request", {}).get("lang", None),
                                          request_department_id=item.get("request", {}).get("department_id", None),
                                          request_idempotency_token=item.get("request", {}).get("idempotency_token", None),
                                          url=item.get("url", None),
                                          )

    def report_download(self,
                        report_id: str = None,
                        ) -> str:
        """

        Получение файла отчета

        Возвращает файл отчета

        :param str report_id: Идентификатор отчета *(Обязательный параметр)*

        `Официальная документация /api/integration/v1/order-report/report <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v1/reports/IntegrationV1OrderReportReport-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if report_id is not None:
            params["report_id"] = validate_fields('report_id', report_id, str)
        if report_id is None:
            raise InputParamError("<report_id> (=>report_id) of <report_download> is a required parameter")

        return self._request(resource="/b2b/cargo/integration/v1/order-report/report", params=params, body=body, method="get")

    def claim_create(self,
                     request_id: str = None,
                     shipping_document: str = None,
                     items: List['CargoItemMP'] = None,
                     route_points: List['CargoPointMP'] = None,
                     emergency_contact_name: str = None,
                     emergency_contact_phone: str = None,
                     client_requirements_taxi_class: str = None,
                     client_requirements_cargo_type: str = None,
                     client_requirements_cargo_loaders: int = None,
                     client_requirements_cargo_options: List['str'] = None,
                     callback_properties_callback_url: str = None,
                     skip_door_to_door: bool = None,
                     skip_client_notify: bool = None,
                     skip_emergency_notify: bool = None,
                     skip_act: bool = None,
                     optional_return: bool = None,
                     due: str = None,
                     comment: str = None,
                     requirements_strict_requirements: List['ClaimRequirement'] = None,
                     requirements_soft_requirements: List['ClaimRequirement'] = None,
                     referral_source: str = None,
                     ) -> SearchedClaimMP:
        """

        Создание заявки с мультиточками

        Cоздает заявку с переданными параметрами. Заявка попадает в систему логистики и запускает процесс заказа. Отправка запроса не начинает обработку заказа. О результате оценки заказа можно узнать из операции v2/claims/info.

        :param str request_id: Токен идемпотентности (не более 32 символов), желательно использовать uuid *(Обязательный параметр)*
        :param Optional[str] shipping_document: Сопроводительные документы
        :param List['CargoItemMP'] items: Перечисление наименований грузов для отправления *(Обязательный параметр)*
        :param List['CargoPointMP'] route_points: Информация по точкам маршрута *(Обязательный параметр)*
        :param str emergency_contact_name: Имя контактного лица *(Обязательный параметр)* (Рик)
        :param str emergency_contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999999)
        :param str client_requirements_taxi_class: Класс такси. Возможные значения courier, express, cargo. *(Обязательный параметр)* (express)
        :param Optional[str] client_requirements_cargo_type: Тип грузовика (lcv_m)
        :param Optional[int] client_requirements_cargo_loaders: Требуемое число грузчиков
        :param Optional[List['str']] client_requirements_cargo_options: Дополнительные опции тарифа
        :param str callback_properties_callback_url: URL, который будет вызываться при смене статусов по заявке.  Данный механизм устарел, вместо него следует использовать операцию v1/claims/journal.  *(Обязательный параметр)* (https://www.example.com)
        :param Optional[bool] skip_door_to_door: Отказ от доставки до двери. В случае true — курьер доставит заказ только на улицу, до подъезда
        :param Optional[bool] skip_client_notify: Не отправлять получателю нотификации, когда к нему направится курьер
        :param Optional[bool] skip_emergency_notify: Не отправлять нотификации emergency контакту
        :param Optional[bool] skip_act: Не показывать акт
        :param Optional[bool] optional_return: Не требуется возврат товаров в случае отмены заказа. В случае true — курьер оставляет товар себе
        :param Optional[str] due: Создать заказ к определенному времени (например, заказ на завтра). Согласуйте с менеджером использование опции! (2020-01-01T00:00:00+00:00)
        :param Optional[str] comment: Общий комментарий к заказу (Ресторан)
        :param Optional[List['ClaimRequirement']] requirements_strict_requirements: Список дополнительных требований к заявке
        :param Optional[List['ClaimRequirement']] requirements_soft_requirements: Список дополнительных требований к заявке
        :param Optional[str] referral_source: Источник заявки (bitrix)

        `Официальная документация /b2b/cargo/integration/v2/claims/create <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v2/claims/IntegrationV2ClaimsCreate-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if request_id is not None:
            params["request_id"] = validate_fields('request_id', request_id, str)
        if request_id is None:
            raise InputParamError("<request_id> (=>request_id) of <claim_create> is a required parameter")

        if shipping_document is not None:
            body["shipping_document"] = validate_fields('shipping_document', shipping_document, str)

        if items is not None:
            body["items"] = validate_fields('items', items, List['CargoItemMP'])
        if items is None:
            raise InputParamError("<items> (=>items) of <claim_create> is a required parameter")
        if items and len(items) < 1:
            raise InputParamError("<items> of <claim_create> should contain at least 1 element")

        if route_points is not None:
            body["route_points"] = validate_fields('route_points', route_points, List['CargoPointMP'])
        if route_points is None:
            raise InputParamError("<route_points> (=>route_points) of <claim_create> is a required parameter")
        if route_points and len(route_points) < 2:
            raise InputParamError("<route_points> of <claim_create> should contain at least 2 element")

        if emergency_contact_name is not None:
            body["emergency_contact"]["name"] = validate_fields('emergency_contact_name', emergency_contact_name, str)
        if emergency_contact_name is None:
            raise InputParamError("<emergency_contact_name> (emergency_contact=>name) of <claim_create> is a required parameter")

        if emergency_contact_phone is not None:
            body["emergency_contact"]["phone"] = validate_fields('emergency_contact_phone', emergency_contact_phone, str)
        if emergency_contact_phone is None:
            raise InputParamError("<emergency_contact_phone> (emergency_contact=>phone) of <claim_create> is a required parameter")

        if client_requirements_taxi_class is not None:
            body["client_requirements"]["taxi_class"] = validate_fields('client_requirements_taxi_class', client_requirements_taxi_class, str)
        if client_requirements_taxi_class is None:
            raise InputParamError("<client_requirements_taxi_class> (client_requirements=>taxi_class) of <claim_create> is a required parameter")

        if client_requirements_cargo_type is not None:
            body["client_requirements"]["cargo_type"] = validate_fields('client_requirements_cargo_type', client_requirements_cargo_type, str)

        if client_requirements_cargo_loaders is not None:
            body["client_requirements"]["cargo_loaders"] = validate_fields('client_requirements_cargo_loaders', client_requirements_cargo_loaders, int)
        if client_requirements_cargo_loaders and client_requirements_cargo_loaders < 0:
            raise InputParamError("<client_requirements_cargo_loaders> of <claim_create> should be more than 0")

        if client_requirements_cargo_options is not None:
            body["client_requirements"]["cargo_options"] = validate_fields('client_requirements_cargo_options', client_requirements_cargo_options, List['str'])

        if callback_properties_callback_url is not None:
            body["callback_properties"]["callback_url"] = validate_fields('callback_properties_callback_url', callback_properties_callback_url, str)
        if callback_properties_callback_url is None:
            raise InputParamError("<callback_properties_callback_url> (callback_properties=>callback_url) of <claim_create> is a required parameter")

        if skip_door_to_door is not None:
            body["skip_door_to_door"] = validate_fields('skip_door_to_door', skip_door_to_door, bool)

        if skip_client_notify is not None:
            body["skip_client_notify"] = validate_fields('skip_client_notify', skip_client_notify, bool)

        if skip_emergency_notify is not None:
            body["skip_emergency_notify"] = validate_fields('skip_emergency_notify', skip_emergency_notify, bool)

        if skip_act is not None:
            body["skip_act"] = validate_fields('skip_act', skip_act, bool)

        if optional_return is not None:
            body["optional_return"] = validate_fields('optional_return', optional_return, bool)

        if due is not None:
            body["due"] = validate_fields('due', due, str)

        if comment is not None:
            body["comment"] = validate_fields('comment', comment, str)

        if requirements_strict_requirements is not None:
            body["requirements"]["strict_requirements"] = validate_fields('requirements_strict_requirements', requirements_strict_requirements, List['ClaimRequirement'])

        if requirements_soft_requirements is not None:
            body["requirements"]["soft_requirements"] = validate_fields('requirements_soft_requirements', requirements_soft_requirements, List['ClaimRequirement'])

        if referral_source is not None:
            body["referral_source"] = validate_fields('referral_source', referral_source, str)

        item = self._request(resource="/b2b/cargo/integration/v2/claims/create", params=params, body=body, method="post")
        return SearchedClaimMP(id=item.get("id", None),
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
                               )

    def claim_edit(self,
                   claim_id: str = None,
                   version: int = None,
                   shipping_document: str = None,
                   items: List['CargoItemMP'] = None,
                   route_points: List['CargoPointMP'] = None,
                   emergency_contact_name: str = None,
                   emergency_contact_phone: str = None,
                   client_requirements_taxi_class: str = None,
                   client_requirements_cargo_type: str = None,
                   client_requirements_cargo_loaders: int = None,
                   client_requirements_cargo_options: List['str'] = None,
                   callback_properties_callback_url: str = None,
                   skip_door_to_door: bool = None,
                   skip_client_notify: bool = None,
                   skip_emergency_notify: bool = None,
                   skip_act: bool = None,
                   optional_return: bool = None,
                   due: str = None,
                   comment: str = None,
                   requirements_strict_requirements: List['ClaimRequirement'] = None,
                   requirements_soft_requirements: List['ClaimRequirement'] = None,
                   referral_source: str = None,
                   ) -> SearchedClaimMP:
        """

        Редактирование заявки с мультиточками

        Изменяет параметры заявки. Операция доступна до принятия оффера клиентом.

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)*
        :param int version: Версия, с которой идет изменение *(Обязательный параметр)*
        :param Optional[str] shipping_document: Сопроводительные документы
        :param List['CargoItemMP'] items: Перечисление наименований грузов для отправления *(Обязательный параметр)*
        :param List['CargoPointMP'] route_points: Информация по точкам маршрута *(Обязательный параметр)*
        :param str emergency_contact_name: Имя контактного лица *(Обязательный параметр)* (Рик)
        :param str emergency_contact_phone: Телефон контактного лица *(Обязательный параметр)* (+79099999999)
        :param str client_requirements_taxi_class: Класс такси. Возможные значения courier, express, cargo. *(Обязательный параметр)* (express)
        :param Optional[str] client_requirements_cargo_type: Тип грузовика (lcv_m)
        :param Optional[int] client_requirements_cargo_loaders: Требуемое число грузчиков
        :param Optional[List['str']] client_requirements_cargo_options: Дополнительные опции тарифа
        :param str callback_properties_callback_url: URL, который будет вызываться при смене статусов по заявке.  Данный механизм устарел, вместо него следует использовать операцию v1/claims/journal.  *(Обязательный параметр)* (https://www.example.com)
        :param Optional[bool] skip_door_to_door: Отказ от доставки до двери. В случае true — курьер доставит заказ только на улицу, до подъезда
        :param Optional[bool] skip_client_notify: Не отправлять получателю нотификации, когда к нему направится курьер
        :param Optional[bool] skip_emergency_notify: Не отправлять нотификации emergency контакту
        :param Optional[bool] skip_act: Не показывать акт
        :param Optional[bool] optional_return: Не требуется возврат товаров в случае отмены заказа. В случае true — курьер оставляет товар себе
        :param Optional[str] due: Создать заказ к определенному времени (например, заказ на завтра). Согласуйте с менеджером использование опции! (2020-01-01T00:00:00+00:00)
        :param Optional[str] comment: Общий комментарий к заказу (Ресторан)
        :param Optional[List['ClaimRequirement']] requirements_strict_requirements: Список дополнительных требований к заявке
        :param Optional[List['ClaimRequirement']] requirements_soft_requirements: Список дополнительных требований к заявке
        :param Optional[str] referral_source: Источник заявки (bitrix)

        `Официальная документация /b2b/cargo/integration/v2/claims/edit <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v2/claims/IntegrationV2ClaimsEdit-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            params["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <claim_edit> is a required parameter")

        if version is not None:
            params["version"] = validate_fields('version', version, int)
        if version is None:
            raise InputParamError("<version> (=>version) of <claim_edit> is a required parameter")

        if shipping_document is not None:
            body["shipping_document"] = validate_fields('shipping_document', shipping_document, str)

        if items is not None:
            body["items"] = validate_fields('items', items, List['CargoItemMP'])
        if items is None:
            raise InputParamError("<items> (=>items) of <claim_edit> is a required parameter")
        if items and len(items) < 1:
            raise InputParamError("<items> of <claim_edit> should contain at least 1 element")

        if route_points is not None:
            body["route_points"] = validate_fields('route_points', route_points, List['CargoPointMP'])
        if route_points is None:
            raise InputParamError("<route_points> (=>route_points) of <claim_edit> is a required parameter")
        if route_points and len(route_points) < 2:
            raise InputParamError("<route_points> of <claim_edit> should contain at least 2 element")

        if emergency_contact_name is not None:
            body["emergency_contact"]["name"] = validate_fields('emergency_contact_name', emergency_contact_name, str)
        if emergency_contact_name is None:
            raise InputParamError("<emergency_contact_name> (emergency_contact=>name) of <claim_edit> is a required parameter")

        if emergency_contact_phone is not None:
            body["emergency_contact"]["phone"] = validate_fields('emergency_contact_phone', emergency_contact_phone, str)
        if emergency_contact_phone is None:
            raise InputParamError("<emergency_contact_phone> (emergency_contact=>phone) of <claim_edit> is a required parameter")

        if client_requirements_taxi_class is not None:
            body["client_requirements"]["taxi_class"] = validate_fields('client_requirements_taxi_class', client_requirements_taxi_class, str)
        if client_requirements_taxi_class is None:
            raise InputParamError("<client_requirements_taxi_class> (client_requirements=>taxi_class) of <claim_edit> is a required parameter")

        if client_requirements_cargo_type is not None:
            body["client_requirements"]["cargo_type"] = validate_fields('client_requirements_cargo_type', client_requirements_cargo_type, str)

        if client_requirements_cargo_loaders is not None:
            body["client_requirements"]["cargo_loaders"] = validate_fields('client_requirements_cargo_loaders', client_requirements_cargo_loaders, int)
        if client_requirements_cargo_loaders and client_requirements_cargo_loaders < 0:
            raise InputParamError("<client_requirements_cargo_loaders> of <claim_edit> should be more than 0")

        if client_requirements_cargo_options is not None:
            body["client_requirements"]["cargo_options"] = validate_fields('client_requirements_cargo_options', client_requirements_cargo_options, List['str'])

        if callback_properties_callback_url is not None:
            body["callback_properties"]["callback_url"] = validate_fields('callback_properties_callback_url', callback_properties_callback_url, str)
        if callback_properties_callback_url is None:
            raise InputParamError("<callback_properties_callback_url> (callback_properties=>callback_url) of <claim_edit> is a required parameter")

        if skip_door_to_door is not None:
            body["skip_door_to_door"] = validate_fields('skip_door_to_door', skip_door_to_door, bool)

        if skip_client_notify is not None:
            body["skip_client_notify"] = validate_fields('skip_client_notify', skip_client_notify, bool)

        if skip_emergency_notify is not None:
            body["skip_emergency_notify"] = validate_fields('skip_emergency_notify', skip_emergency_notify, bool)

        if skip_act is not None:
            body["skip_act"] = validate_fields('skip_act', skip_act, bool)

        if optional_return is not None:
            body["optional_return"] = validate_fields('optional_return', optional_return, bool)

        if due is not None:
            body["due"] = validate_fields('due', due, str)

        if comment is not None:
            body["comment"] = validate_fields('comment', comment, str)

        if requirements_strict_requirements is not None:
            body["requirements"]["strict_requirements"] = validate_fields('requirements_strict_requirements', requirements_strict_requirements, List['ClaimRequirement'])

        if requirements_soft_requirements is not None:
            body["requirements"]["soft_requirements"] = validate_fields('requirements_soft_requirements', requirements_soft_requirements, List['ClaimRequirement'])

        if referral_source is not None:
            body["referral_source"] = validate_fields('referral_source', referral_source, str)

        item = self._request(resource="/b2b/cargo/integration/v2/claims/edit", params=params, body=body, method="post")
        return SearchedClaimMP(id=item.get("id", None),
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
                               )

    def claim_info(self,
                   claim_id: str = None,
                   ) -> SearchedClaimMP:
        """

        Получение информации по заявкам с учетом мультиточек

        Возвращает основную информацию по заявке с учетом мультиточек (статус, стоимость, возможность бесплатной отмены и пр.). Вы можете использовать операцию для получения информации по заявке, созданной через v1/claims/create.

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)*

        `Официальная документация /b2b/cargo/integration/v2/claims/info <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v2/claims/IntegrationV2ClaimsInfo-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            params["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <claim_info> is a required parameter")

        item = self._request(resource="/b2b/cargo/integration/v2/claims/info", params=params, body=body, method="post")
        return SearchedClaimMP(id=item.get("id", None),
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
                               )

    def claim_search(self,
                     offset: int = None,
                     limit: int = None,
                     claim_id: str = None,
                     phone: str = None,
                     status: str = None,
                     created_from: str = None,
                     created_to: str = None,
                     state: str = None,
                     due_from: str = None,
                     due_to: str = None,
                     external_order_id: str = None,
                     ) -> SearchClaimsResponseMP:
        """

        Поиск заявок

        Выполняет поиск произвольных заявок с учетом мультиточек. Вы можете использовать операцию для получения информации по заявке, созданной через v1/claims/create. Найденные заявки сортируются по дате создания, выдача сегментирована для пагинации.

        :param int offset: Смещение (пагинация) выдачи заявок по заданному фильтру (заявки отсортированы по дате создания) *(Обязательный параметр)* (50)
        :param int limit: Максимальное число заявок в ответе *(Обязательный параметр)* (50)
        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)* (741cedf82cd464fa6fa16d87155c636)
        :param Optional[str] phone: Фильтр по номеру телефона (+79099999998)
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

        :param Optional[str] created_from: Начало периода поиска (isoformat) (2020-01-01T00:00:00+00:00)
        :param Optional[str] created_to: Окончание периода поиска (isoformat) (2020-01-02T00:00:00+00:00)
        :param Optional[str] state: Фильтр по состоянию заявки (active)

            * **active** - ???

        :param Optional[str] due_from: Начало периода поиска (isoformat) (2020-01-01T00:00:00+00:00)
        :param Optional[str] due_to: Окончание периода поиска (isoformat) (2020-01-02T00:00:00+00:00)
        :param Optional[str] external_order_id: Идентификатор внешнего заказа, привязанного к точке (100)

        `Официальная документация /b2b/cargo/integration/v2/claims/search <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v2/claims/IntegrationV2ClaimsSearch-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if offset is not None:
            body["offset"] = validate_fields('offset', offset, int)
        if offset is None:
            raise InputParamError("<offset> (=>offset) of <claim_search> is a required parameter")
        if offset and offset < 0:
            raise InputParamError("<offset> of <claim_search> should be more than 0")

        if limit is not None:
            body["limit"] = validate_fields('limit', limit, int)
        if limit is None:
            raise InputParamError("<limit> (=>limit) of <claim_search> is a required parameter")
        if limit and limit < 0:
            raise InputParamError("<limit> of <claim_search> should be more than 0")
        if limit and limit > 1000:
            raise InputParamError("<limit> of <claim_search> should be less than 1000")

        if claim_id is not None:
            body["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <claim_search> is a required parameter")

        if phone is not None:
            body["phone"] = validate_fields('phone', phone, str)

        if status is not None:
            body["status"] = validate_fields('status', status, str)
        if status is None:
            raise InputParamError("<status> (=>status) of <claim_search> is a required parameter")

        if status not in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived',
                          'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning',
                          'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi',
                          'cancelled_with_items_on_hands']:
            raise InputParamError(
                "<status> of <claim_search> should be in ['new', 'estimating', 'estimating_failed', 'ready_for_approval', 'accepted', 'performer_lookup', 'performer_draft', 'performer_found', 'performer_not_found', 'pickup_arrived', 'ready_for_pickup_confirmation', 'pickuped', 'delivery_arrived', 'ready_for_delivery_confirmation', 'pay_waiting', 'delivered', 'delivered_finish', 'returning', 'return_arrived', 'ready_for_return_confirmation', 'returned', 'returned_finish', 'failed', 'cancelled', 'cancelled_with_payment', 'cancelled_by_taxi', 'cancelled_with_items_on_hands']")

        if created_from is not None:
            body["created_from"] = validate_fields('created_from', created_from, str)

        if created_to is not None:
            body["created_to"] = validate_fields('created_to', created_to, str)

        if state is not None:
            body["state"] = validate_fields('state', state, str)

        if state not in ['active']:
            raise InputParamError("<state> of <claim_search> should be in ['active']")

        if due_from is not None:
            body["due_from"] = validate_fields('due_from', due_from, str)

        if due_to is not None:
            body["due_to"] = validate_fields('due_to', due_to, str)

        if external_order_id is not None:
            body["external_order_id"] = validate_fields('external_order_id', external_order_id, str)

        item = self._request(resource="/b2b/cargo/integration/v2/claims/search", params=params, body=body, method="post")
        return SearchClaimsResponseMP(claims=item.get("claims", None),
                                      )

    def search_active(self,
                      offset: int = None,
                      limit: int = None,
                      ) -> SearchClaimsResponseMP:
        """

        Поиск активных заявок

        Возвращает информацию по заявкам с учетом мультиточек, которые находятся в исполнении. Вы можете использовать операцию для получения информации по заявке, созданной через v1/claims/create. Найденные заявки сортируются по дате создания, выдача сегментирована для пагинации.

        :param int offset: Смещение (пагинация) выдачи заявок по заданному фильтру (заявки отсортированы по дате создания) *(Обязательный параметр)* (50)
        :param int limit: Максимальное число заявок в ответе *(Обязательный параметр)* (50)

        `Официальная документация /b2b/cargo/integration/v2/claims/search/active <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v2/claims/IntegrationV2ClaimsSearchActive-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if offset is not None:
            body["offset"] = validate_fields('offset', offset, int)
        if offset is None:
            raise InputParamError("<offset> (=>offset) of <search_active> is a required parameter")
        if offset and offset < 0:
            raise InputParamError("<offset> of <search_active> should be more than 0")

        if limit is not None:
            body["limit"] = validate_fields('limit', limit, int)
        if limit is None:
            raise InputParamError("<limit> (=>limit) of <search_active> is a required parameter")
        if limit and limit < 0:
            raise InputParamError("<limit> of <search_active> should be more than 0")
        if limit and limit > 1000:
            raise InputParamError("<limit> of <search_active> should be less than 1000")

        item = self._request(resource="/b2b/cargo/integration/v2/claims/search/active", params=params, body=body, method="post")
        return SearchClaimsResponseMP(claims=item.get("claims", None),
                                      )

    def claim_confirmation_code(self,
                                claim_id: str = None,
                                ) -> ConfirmationCodeResponse:
        """

        Получение кода подтверждения

        Возвращает код подтверждения в текущей точке (если это возможно)

        :param str claim_id: Идентификатор заявки, полученный на этапе создания заявки *(Обязательный параметр)* (741cedf82cd464fa6fa16d87155c636)

        `Официальная документация /b2b/cargo/integration/v2/claims/confirmation_code <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v2/claims/IntegrationV2ClaimsConfirmationCode-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_id is not None:
            body["claim_id"] = validate_fields('claim_id', claim_id, str)
        if claim_id is None:
            raise InputParamError("<claim_id> (=>claim_id) of <claim_confirmation_code> is a required parameter")

        item = self._request(resource="/b2b/cargo/integration/v2/claims/confirmation_code", params=params, body=body, method="post")
        return ConfirmationCodeResponse(code=item.get("code", None),
                                        attempts=item.get("attempts", None),
                                        )

    def claim_bulk(self,
                   claim_ids: List['str'] = None,
                   ) -> SearchClaimsResponseMP:
        """

        Получение информации по нескольким заявкам

        Возвращает информацию по нескольким заявкам с учетом мультиточек. Вы можете использовать операцию для получения информации по заявке, созданной через v1/claims/create.

        :param List['str'] claim_ids: Массив идентификаторов заявки для которых нужно получить информацию *(Обязательный параметр)*

        `Официальная документация /b2b/cargo/integration/v2/claims/bulk_info <https://yandex.ru/dev/taxi/doc/cargo-api/ref/v2/claims/IntegrationV2ClaimsBulkInfo-docpage/>`_
        """
        params = {}
        body = collections.defaultdict(dict)

        if claim_ids is not None:
            body["claim_ids"] = validate_fields('claim_ids', claim_ids, List['str'])
        if claim_ids is None:
            raise InputParamError("<claim_ids> (=>claim_ids) of <claim_bulk> is a required parameter")
        if claim_ids and len(claim_ids) < 1:
            raise InputParamError("<claim_ids> of <claim_bulk> should contain at least 1 element")
        if claim_ids and len(claim_ids) > 1000:
            raise InputParamError("<claim_ids> of <claim_bulk> should not contain more than 1000 element")

        item = self._request(resource="/b2b/cargo/integration/v2/claims/bulk_info", params=params, body=body, method="post")
        return SearchClaimsResponseMP(claims=item.get("claims", None),
                                      )
