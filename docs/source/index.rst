yacargo
=========

Просто установить:

   pip3 install yacargo


Просто использовать:

   >>> import yacargo
   >>> ya = yacargo.YCAPI('SuperDuperToken')
   >>> a = ya.claim_create(items=[yacargo.CargoItemMP(pickup_point=1,
   >>>                                                droppof_point=2,
   >>>                                                title='item_1',
   >>>                                                cost_value='13',
   >>>                                                cost_currency='RUB',
   >>>                                                quantity=1,
   >>>                                                size=yacargo.CargoItemSizes(length=0.1,
   >>>                                                                            width=0.1,
   >>>                                                                            height=0.1),
   >>>                                                weight=1.0
   >>>                                                )],
   >>>                     route_points=[yacargo.CargoPointMP(point_id=1,
   >>>                                                        visit_order=1,
   >>>                                                        contact=yacargo.ContactOnPoint(name='Иван', phone='+78231234567'),
   >>>                                                        address=yacargo.CargoPointAddress(fullname='БЦ Аврора',
   >>>                                                                                          coordinates=[37.642474, 55.735520],
   >>>                                                                                          ),
   >>>                                                        point_type='source'),
   >>>                                   yacargo.CargoPointMP(point_id=2,
   >>>                                                        visit_order=2,
   >>>                                                        contact=yacargo.ContactOnPoint(name='Петр', phone='+78237654321'),
   >>>                                                        address=yacargo.CargoPointAddress(fullname='улица Вавилова, 3',
   >>>                                                                                          coordinates=[37.590860, 55.707368],
   >>>                                                                                          ),
   >>>                                                        point_type='destination')],
   >>>                     emergency_contact=yacargo.ContactWithPhone(name='Сергей', phone='+78232341234'),
   >>>                     )
   >>> print(a.claim_id)
   106f0124536f48c992961254b8259d20
   >>> a = ya.claim_info('106f0daed36f48c99296ed07b8259d20'.status)
   >>> print(a)
   new

   pip3 install yacargo


Список доступных методов:
-------------------------

.. currentmodule:: yacargo

.. autosummary::
        ~yacargo

:ref:`genindex`

.. toctree::

   yacargo
