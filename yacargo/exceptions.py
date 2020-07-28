# -*- coding: utf-8 -*-
"""
Модуль с эксепшенами сервера API
"""
import logging


class NetworkAPIError(BaseException):
    """
        Сетевая ошибка
    """
    pass


class BaseAPIError(BaseException):
    """
        Базовая ошибка API
    """

    def __init__(self, data):
        self.code = data.get('code')
        self.message = data.get('message')
        if self.code not in ('cancel_error',
                             'change_destination_error',
                             'db_error',
                             'double_request',
                             'esignature_error',
                             'esignature_too_many_requests',
                             'inappropriate_status',
                             'not_allowed',
                             'not_found',
                             'old_lookup_version',
                             'old_version',
                             'payment_sms_send_failed',
                             'payment_terminal_error',
                             'payment_on_delivery_disabled',
                             'payment_on_delivery_invalid_token',
                             'payment_on_delivery_invalid_request',
                             'pdf_failure',
                             'send_email_error',
                             'state_mismatch',
                             'validation_error',
                             'wrong_corp_client_id',
                             'wrong_taxi_order_id',
                             'confirmation_code_required',
                             'items_without_parameters_forbidden',
                             'payment_and_skip_sms_conflict',
                             'no_input_point',
                             'no_required_email_for_point',
                             'unsupported_points_count',
                             'invalid_source_point',
                             'invalid_destination_point',
                             'invalid_item_source_point',
                             'invalid_item_destination_point',
                             'item_source_point_not_found',
                             'item_destination_point_not_found',
                             'state_transition_forbidden',
                             'invalid_cursor',
                             'inappropriate_point',
                             'external_order_id_not_allowed'):
            logging.error('Unknown server status: %s', self.code)
        logging.error('Server error: %s', self.message)


class NotAuthorized(BaseException):
    """
        Ошибка авторизации
    """
    pass


class InputParamError(BaseException):
    """
        Ошибка в передаваемых полях
    """
    pass
