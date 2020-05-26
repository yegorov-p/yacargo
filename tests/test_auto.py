# -*- coding: utf-8 -*-
import inspect
import logging.config
import os
import re
import sys
import types
from unittest import TestCase, skip

import typing_inspect

from YaCargo import YCAPI, response
from YaCargo.objects import *

api = YCAPI(os.environ['TOKEN'])
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(filename)s:%(lineno)d %(levelname)-8s %(funcName)s %(message)s',
            # 'format': '%(message)s',
            'datefmt': "%H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },

    },
    'loggers': {
        'YaCargo': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}
logging.config.dictConfig(LOGGING)

OBJECT_LIST = []
for name, obj in inspect.getmembers(sys.modules['YaCargo.objects']):
    if inspect.isclass(obj):
        OBJECT_LIST.append(obj.__name__)


def analyze(obj):
    print(obj)
    print(obj.__module__)
    print(obj.__class__)
    # print(re.search(':rtype: (.*)', inspect.getdoc(obj.__class__.__name__)).group(1))


def rvars_doc(s):
    return [r for r in re.findall('\* \*\*(.*)\*\*', s)]


def getmembers(test_object):
    '''Получение свойств объекта'''
    return [k[0] for k in inspect.getmembers(test_object, lambda x: isinstance(x, property))]


class TestYaCargoAPI(TestCase):
    created_claim = None
    def insp(self, data, tab=0):
        tabulate = ' ' * tab * 4
        obj = data.__class__.__name__
        logging.debug('{}INSPECTING object {}'.format(tabulate, obj))
        logging.debug('{}JSON {}'.format(tabulate, data.json()))
        for (k, v) in inspect.getmembers(getattr(response, data.__class__.__name__), lambda x: isinstance(x, (property, types.MethodType))):
            signature = inspect.signature(v.fget).return_annotation
            logging.debug('{}Property: {}'.format(tabulate, k))
            logging.debug('{}Value: {}'.format(tabulate, data.__getattribute__(k)))
            logging.debug('{}Types should be {} => {}'.format(tabulate, signature, type(data.__getattribute__(k))))
            check_type(k, data.__getattribute__(k), signature)
            if typing_inspect.get_origin(signature) is list:
                for el in data.__getattribute__(k):
                    self.insp(el, tab=tab + 1)
            logging.debug('{}{}'.format(tabulate, '-' * 80))
        logging.debug('{}\n'.format(tabulate))


    @skip("testing skipping")
    def test_1claim_create(self):
        claim = api.claim_create(items=[CargoItemMP(pickup_point=1,
                                                    droppof_point=2,
                                                    title='item_1',
                                                    cost_value='13',
                                                    cost_currency='RUB',
                                                    quantity=1,
                                                    size=CargoItemSizes(length=0.1,
                                                                        width=0.1,
                                                                        height=0.1),
                                                    weight=1.0
                                                    )],
                                 route_points=[CargoPointMP(point_id=1,
                                                            visit_order=1,
                                                            contact=ContactOnPoint(name='name', phone='+7823'),
                                                            address=CargoPointAddress(fullname='БЦ Аврора',
                                                                                      coordinates=[36.5778, 54.7392],
                                                                                      ),
                                                            point_type='source'),
                                               CargoPointMP(point_id=2,
                                                            visit_order=2,
                                                            contact=ContactOnPoint(name='name', phone='+7823'),
                                                            address=CargoPointAddress(fullname='ТЦ Радуга',
                                                                                      coordinates=[37.079133, 55.734603],
                                                                                      ),
                                                            point_type='destination')],
                                 emergency_contact=ContactWithPhone(name='name', phone='+7823'),
                                 # client_requirements=YaCargo.ClientRequirements(),
                                 # due='123',
                                 # comment='asd',
                                 # c2c_data=YaCargo.C2CData()
                                 )
        self.__class__.created_claim = claim.claim_id
        print(claim.claim_id)
        self.insp(claim)

    @skip("testing skipping")
    def test_claim_edit(self):
        self.insp(api.claim_edit(claim_id=self.__class__.created_claim,
                                 comment='111'))

    @skip("testing skipping")
    def test_claim_info(self):
        self.insp(api.claim_info(claim_id=self.__class__.created_claim))

    # @skip("testing skipping")
    def test_search_active(self):
        self.insp(api.search_active())

    @skip("testing skipping")
    def test_claim_search(self):
        self.insp(api.claim_search(claim_id=self.__class__.created_claim))

    @skip("testing skipping")
    def test_claim_bulk(self):
        # self.insp(api.claim_bulk(claim_ids=['42e1da8d289b4e1b9f11a88485241541']))
        # self.insp(api.claim_bulk(claim_ids=[123]))
        self.insp(api.claim_bulk(claim_ids=[self.__class__.created_claim]))
