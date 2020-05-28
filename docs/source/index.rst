YaCargo
=========

Просто установить:

   pip3 install yacargo


Просто использовать:

   >>> import YaCargo
   >>> ya = YaCargo.YCAPI('SuperDuperToken')
   >>> a = ya.claim_create(items=[YaCargo.CargoItemMP(pickup_point=1,
   >>>                                                droppof_point=2,
   >>>                                                title='item_1',
   >>>                                                cost_value='13',
   >>>                                                cost_currency='RUB',
   >>>                                                quantity=1,
   >>>                                                size=YaCargo.CargoItemSizes(length=0.1,
   >>>                                                                            width=0.1,
   >>>                                                                            height=0.1),
   >>>                                                weight=1.0
   >>>                                                )],
   >>>                     route_points=[YaCargo.CargoPointMP(point_id=1,
   >>>                                                        visit_order=1,
   >>>                                                        contact=YaCargo.ContactOnPoint(name='Иван', phone='+78231234567'),
   >>>                                                        address=YaCargo.CargoPointAddress(fullname='БЦ Аврора',
   >>>                                                                                          coordinates=[37.642474, 55.735520],
   >>>                                                                                          ),
   >>>                                                        point_type='source'),
   >>>                                   YaCargo.CargoPointMP(point_id=2,
   >>>                                                        visit_order=2,
   >>>                                                        contact=YaCargo.ContactOnPoint(name='Петр', phone='+78237654321'),
   >>>                                                        address=YaCargo.CargoPointAddress(fullname='улица Вавилова, 3',
   >>>                                                                                          coordinates=[37.590860, 55.707368],
   >>>                                                                                          ),
   >>>                                                        point_type='destination')],
   >>>                     emergency_contact=YaCargo.ContactWithPhone(name='Сергей', phone='+78232341234'),
   >>>                     )
   >>> print(a.claim_id)
   106f0124536f48c992961254b8259d20
   >>> a = ya.claim_info('106f0daed36f48c99296ed07b8259d20'.status)
   >>> print(a)
   new

Список доступных методов:
-------------------------

.. currentmodule:: YaCargo

.. autosummary::
        ~YaCargo

:ref:`genindex`

.. toctree::

   YaCargo
