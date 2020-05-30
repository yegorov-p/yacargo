# -*- coding: utf-8 -*-
USER_AGENT = 'yacargo'

VERSION = '0.0.3'

PROTOCOL = 'https'

DOMAIN = 'b2b.taxi.yandex.net'
DOMAIN_TEST = 'b2b.taxi.tst.yandex.net'

RESOURCES = [
    'v2/claims/create',
    'v2/claims/edit',
    'v2/claims/info',
    'v2/claims/search',
    'v2/claims/search/active',
    'v2/claims/bulk_info',
    'v1/claims/accept',
    'v1/driver-voiceforwarding',
    'v1/claims/journal',
    'v1/claims/document',
    'v1/claims/cancel',
    'v1/claims/performer-position'
]

VAT_CODE = (1, 2, 3, 4, 5, 6)

PAYMENT_SUBJECT = ['commodity', 'excise', 'service', 'job', 'gambling_bet', 'gambling_prize', 'lottery',
                   'lottery_prize', 'intellectual_activity', 'payment', 'agent_commission', 'property_right',
                   'non_operating_gain', 'insurance_premium', 'sales_tax', 'resort_fee', 'composite', 'another']

PAYMENT_MODE = ['full_prepayment', 'partial_prepayment', 'advance', 'full_payment', 'partial_payment', 'credit', 'credit_payment']

COUNTRY_OF_ORIGIN_CODE = ['AB', 'AU', 'AT', 'AZ', 'AL', 'DZ', 'AS', 'AI', 'AO', 'AD', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AF', 'BS', 'BD', 'BB', 'BH', 'BY', 'BZ', 'BE', 'BJ', 'BM', 'BG', 'BO', 'BQ', 'BA',
                          'BW', 'BR', 'IO', 'BN', 'BF', 'BI', 'BT', 'VU', 'HU', 'VE', 'VG', 'VI', 'VN', 'GA', 'HT', 'GY', 'GM', 'GH', 'GP', 'GT', 'GN', 'GW', 'DE', 'GG', 'GI', 'HN', 'HK', 'GD', 'GL',
                          'GR', 'GE', 'GU', 'DK', 'JE', 'DJ', 'DM', 'DO', 'EG', 'ZM', 'EH', 'ZW', 'IL', 'IN', 'ID', 'JO', 'IQ', 'IR', 'IE', 'IS', 'ES', 'IT', 'YE', 'CV', 'KZ', 'KH', 'CM', 'CA', 'QA',
                          'KE', 'CY', 'KG', 'KI', 'CN', 'CC', 'CO', 'KM', 'CG', 'CD', 'KP', 'KR', 'CR', 'CI', 'CU', 'KW', 'CW', 'LA', 'LV', 'LS', 'LR', 'LB', 'LY', 'LT', 'LI', 'LU', 'MU', 'MR', 'MG',
                          'YT', 'MO', 'MK', 'MW', 'MY', 'ML', 'UM', 'MV', 'MT', 'MA', 'MQ', 'MH', 'MX', 'FM', 'MZ', 'MD', 'MC', 'MN', 'MS', 'MM', 'NA', 'NR', 'NP', 'NE', 'NG', 'NL', 'NI', 'NU', 'NZ',
                          'NC', 'NO', 'AE', 'OM', 'KY', 'CK', 'TC', 'BV', 'IM', 'NF', 'CX', 'HM', 'PK', 'PW', 'PS', 'PA', 'VA', 'PG', 'PY', 'PE', 'PN', 'PL', 'PT', 'PR', 'RE', 'RU', 'RW', 'RO', 'WS',
                          'SM', 'ST', 'SA', 'SZ', 'SH', 'MP', 'SC', 'BL', 'MF', 'SX', 'SN', 'VC', 'KN', 'LC', 'PM', 'RS', 'SG', 'SY', 'SK', 'SI', 'GB', 'US', 'SB', 'SO', 'SD', 'SR', 'SL', 'TJ', 'TH',
                          'TW', 'TZ', 'TL', 'TG', 'TK', 'TO', 'TT', 'TV', 'TN', 'TM', 'TR', 'UG', 'UZ', 'UA', 'WF', 'UY', 'FO', 'FJ', 'PH', 'FI', 'FK', 'FR', 'GF', 'PF', 'TF', 'HR', 'CF', 'TD', 'ME',
                          'CZ', 'CL', 'CH', 'SE', 'SJ', 'LK', 'EC', 'GQ', 'AX', 'SV', 'ER', 'EE', 'ET', 'ZA', 'GS', 'OS', 'SS', 'JM', 'JP']

TAX_SYSTEM_CODE = (1, 2, 3, 4, 5, 6)

TAXI_CLASS = ['express', 'courier', 'cargo']

CARGO_TYPE = ['van', 'lcv_m', 'lcv_l']
