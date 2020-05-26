YaCargo
=========

Просто установить:

   pip3 install yacargo


Просто использовать:

   >>> from YMContent import YMAPI
   >>> api = YMAPI('SuperSecretToken')
   >>> a = api.model('1732210983', geo_id=213, fields='ALL')
   >>> a.model.name
   Смартфон Apple iPhone X 256GB
   >>> a.model.description
   GSM, LTE-A, смартфон, iOS 11, вес 174 г, ШхВхТ 70.9x143.6x7.7 мм, экран 5.8", 2436x1125, Bluetooth, NFC, Wi-Fi, GPS, ГЛОНАСС, фотокамера 12 МП, память 256 Гб
   >>> a.model.price.json()
   {'max': '92930', 'min': '72290', 'avg': '77499'}

Список доступных методов:
-------------------------

.. currentmodule:: YaCargo

.. autosummary::
        ~YaCargo

:ref:`genindex`

.. toctree::

   YaCargo
