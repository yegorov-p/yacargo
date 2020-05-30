yacargo
=========

Просто установить:

   pip3 install yacargo


Просто использовать:
   >>> import logging
   >>> import yacargo
   >>> from yacargo.objects import *
   >>>
   >>> logging.basicConfig(level=logging.DEBUG)
   >>>
   >>> ya = yacargo.YCAPI('SuperDuperToken')
   >>>
   >>> a = ya.claim_create(items=[CargoItemMP(pickup_point=1,
   >>>                                        droppof_point=2,
   >>>                                        title='Шоколадка',
   >>>                                        cost_value='13.1',
   >>>                                        cost_currency='RUB',
   >>>                                        quantity=1,
   >>>                                        size=CargoItemSizes(length=0.1,
   >>>                                                            width=0.1,
   >>>                                                            height=0.1),
   >>>                                        weight=1.0
   >>>                                        )],
   >>>                     route_points=[CargoPointMP(point_id=1,
   >>>                                                visit_order=1,
   >>>                                                contact=ContactOnPoint(name='Иван', phone='+78231234567'),
   >>>                                                address=CargoPointAddress(fullname='БЦ Аврора',
   >>>                                                                          coordinates=[37.642474, 55.735520],
   >>>                                                                          ),
   >>>                                                point_type='source'),
   >>>                                   yacargo.CargoPointMP(point_id=2,
   >>>                                                        visit_order=2,
   >>>                                                        contact=ContactOnPoint(name='Петр', phone='+78237654321'),
   >>>                                                        address=CargoPointAddress(fullname='улица Вавилова, 3',
   >>>                                                                                  coordinates=[37.590860, 55.707368],
   >>>                                                                                  ),
   >>>                                                        point_type='destination')],
   >>>                     emergency_contact=ContactWithPhone(name='Сергей', phone='+78232341234')
   >>>                     )
   >>> print(a.claim_id)
   4c23108d326345e9aba7bbaab4537a21
   >>> a = ya.claim_info('4c23108d326345e9aba7bbaab4537a21')
   >>> print(a.status)
   >>> ready_for_approval


Список доступных методов:
-------------------------

.. currentmodule:: yacargo

.. autosummary::
        ~yacargo.YCAPI.claim_create
        ~yacargo.YCAPI.claim_edit
        ~yacargo.YCAPI.claim_info
        ~yacargo.YCAPI.claim_search
        ~yacargo.YCAPI.search_active
        ~yacargo.YCAPI.claim_bulk
        ~yacargo.YCAPI.claim_accept
        ~yacargo.YCAPI.voiceforwarding
        ~yacargo.YCAPI.claim_journal
        ~yacargo.YCAPI.claim_document
        ~yacargo.YCAPI.claim_cancel
        ~yacargo.YCAPI.performer_position

:ref:`genindex`

.. toctree::

   yacargo
