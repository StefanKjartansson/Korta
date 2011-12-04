#!/usr/bin/env python
# -*- coding: utf-8 -


from .datastructures import AttributeDict


KORTA = AttributeDict({
    'acceptor_ident': 'd42',
    'acceptor_term_id': 'd41',
    'action_code': 'd39',
    'action_code_echo': 'o39',
    'action_code_text': 'd39text',
    'amount': 'd4',
    'amount_echo': 'o4',
    'approval_code': 'd38',
    'approval_code_echo': 'o38',
    'card_acceptor_id': 'd42',
    'card_acceptor_identity': 'd41',
    'card_brand_name': 'd2brand',
    'cardholder_name': 'd2name',
    'cc_expire': 'd14',
    'cc_number': 'd2',
    'cc_verify_code': 'd47',
    'charge_reference': 'daskauthorise',
    'client_ip': 'cip',
    'client_lang': 'clang',
    'code_authorization_approved': '000',
    'code_authorization_declined': '100',
    'code_system_failure_error': '909',
    'code_system_failure_retry': '946',
    'currency_code': 'd49',
    'currency_exponent': 'de4',
    'current_date': 'd12',
    'current_date_echo': 'o12',
    'date_format': '%y%m%d%H%M%S',
    'error_code': 'error',
    'error_text': 'errortext',
    'function_identifier': 'do',
    'korta_reference': 'dask',
    'mask_cc': 'd2dsp',
    'merchant_lang': 'mlang',
    'original_data_element': 'd56',
    'password': 'pwd',
    'reference': 'daskm',
    'reference_id': 'd31',
    'settlement_reference_number': 'd37',
    'shipping_address': 'd2saddr',
    'shipping_city': 'd2scity',
    'shipping_country': 'd2sctr',
    'shipping_zip': 'd2szip',
    'site': 'site',
    'storage_duration': 'daskd',
    'sub_function_identifier': 'dos',
    'total_response': 'totalResponse',
    'unknown': 'd3',
    'user': 'user',
})


CURRENCY_CODES = AttributeDict({
    'DDK': 208,
    'EUR': 978,
    'GBP': 826,
    'ISK': 352,
    'NOK': 578,
    'SEK': 752,
    'USD': 840,
})
