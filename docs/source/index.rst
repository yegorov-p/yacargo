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
   >>> a = ya.claim_create(request_id='asasdasdad',
   >>>                     items=[yacargo.CargoItemMP(pickup_point=1,
   >>>                                                droppof_point=2,
   >>>                                                title='Шоколадка',
   >>>                                                cost_value='13.1',
   >>>                                                cost_currency='RUB',
   >>>                                                quantity=1,
   >>>                                                size_length=0.1,
   >>>                                                size_width=0.1,
   >>>                                                size_height=0.1,
   >>>                                                weight=1
   >>>                                                )],
   >>>                     route_points=[yacargo.CargoPointMP(type='source',
   >>>                                                        visit_order=1,
   >>>                                                        point_id=1,
   >>>                                                        contact_name='Иван',
   >>>                                                        contact_phone='+78231234567',
   >>>                                                        contact_email='asd@asd.com',
   >>>                                                        address_fullname='БЦ Аврора',
   >>>                                                        address_coordinates=[37.642474, 55.735520],
   >>>                                                        ),
   >>>                                   yacargo.CargoPointMP(type='destination',
   >>>                                                        visit_order=2,
   >>>                                                        point_id=2,
   >>>                                                        contact_name='Петр',
   >>>                                                        contact_phone='+78237654321',
   >>>                                                        contact_email='sss@sss.com',
   >>>                                                        address_fullname='улица Вавилова, 3',
   >>>                                                        address_coordinates=[37.590860, 55.707368],
   >>>                                                        )
   >>>                                   ],
   >>>                     emergency_contact_name='Сергей',
   >>>                     emergency_contact_phone='+78232341234',
   >>>                     client_requirements_taxi_class='express',
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
        ~yacargo.YCAPI.claim_accept
        ~yacargo.YCAPI.claim_bulk
        ~yacargo.YCAPI.claim_cancel
        ~yacargo.YCAPI.claim_confirmation_code
        ~yacargo.YCAPI.claim_create
        ~yacargo.YCAPI.claim_document
        ~yacargo.YCAPI.claim_edit
        ~yacargo.YCAPI.claim_info
        ~yacargo.YCAPI.claim_journal
        ~yacargo.YCAPI.claim_search
        ~yacargo.YCAPI.performer_position
        ~yacargo.YCAPI.report_download
        ~yacargo.YCAPI.report_generate
        ~yacargo.YCAPI.report_status
        ~yacargo.YCAPI.search_active
        ~yacargo.YCAPI.voiceforwarding

:ref:`genindex`

.. toctree::

   yacargo
