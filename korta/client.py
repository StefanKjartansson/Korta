#!/usr/bin/env python
# -*- coding: utf-8 -

import datetime
import itertools
import logging
import random
import string
import sys

if sys.version_info >= (3, 0):
    from urllib.parse import unquote_plus, urlencode
else:
    from urllib import unquote_plus, urlencode

from .datastructures import AttributeDict
from .defaults import KORTA, CURRENCY_CODES
from .sslclient import SSLClient


RKORTA = dict(((v, k) for (k, v)
    in list(KORTA.items())))


RCURRENCY_CODES = dict(((v, k) for (k, v)
    in list(CURRENCY_CODES.items())))


def korta_reference():
    return ''.join([random.choice(string.letters)
        for i in range(19)])


class CreditCard(object):
    """
    Simple data class representing a credit card.

    .. note::

        Will be moved into a separate module
    """

    def __init__(self, number, expiration_month, expiration_year, ccv):
        self.number = number
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.ccv = ccv

    @property
    def expiration_date(self):
        y = str(self.expiration_year)
        m = self.expiration_month
        if len(y) == 2:
            y = '20' + y
        return datetime.date(int(y), int(m), 1)

    @property
    def expires(self):
        return self.expiration_date.strftime('%y%m')


class Customer(object):
    """
    Simple data class representing a customer

    .. note::

        Will be moved into a separate module
    """

    def __init__(self, reference, credit_card, duration=2):
        self.credit_card = credit_card
        self.reference = reference
        self.duration = duration


class Order(object):
    """
    Simple data class representing an order

    .. note::

        Will be moved into a separate module
    """

    def __init__(self, reference, amount, currency='ISK',
            currency_exponent=2):
        self.reference = reference
        self.amount = amount
        self._currency = currency
        self.currency_exponent = currency_exponent

    @property
    def currency(self):
        return CURRENCY_CODES[self._currency]


class Client(object):
    """
    Encapsulates the logic needed to interface with korta through
    an instance of the SSLClient.
    """

    def __init__(self, key_file, ca_file, user, password, site_id,
            card_acceptor_id, card_acceptor_identity,
            host, port=8443, currency='USD'):

        self.connection = SSLClient(host, port)
        self.connection.set_cert(key_file, ca_file,
            passwd_cb=password)
        self.connection.set_user(user, password)

        self.user = user
        self.password = password
        self.site_id = site_id
        self.card_acceptor_id = card_acceptor_id
        self.card_acceptor_identity = card_acceptor_identity
        self.default_currency = currency
        self.log = logging.getLogger(__name__)

    def parse_response(self, response):
        """
        Maps back to korta values and returns the dictionary
        """
        def _format(k, v):
            return (RKORTA.get(k), v)

        return AttributeDict([_format(k, unquote_plus(v))
                for (k, v) in itertools.chain([i.split('=')
                    for i in response.split('&')])])

    def do_request(self, path, params):
        """
        Calls the path with the urlencoded params
        """
        self.log.debug('Calling %s, params: %s' % (path, repr(params)))
        r = self.parse_response(
            self.connection.request('GET', '%s?%s' % (path,
                urlencode(params))))
        if r.action_code != '000':
            self.log.error('Error: %s' % r.error_text)
        return r

    def get_defaults(self):
        """
        Returns defaults needed for most requests
        """
        return  {
            KORTA.user: self.user,
            KORTA.password: self.password,
            KORTA.site: self.site_id,
            KORTA.card_acceptor_id: self.card_acceptor_id,
            KORTA.card_acceptor_identity: self.card_acceptor_identity
        }

    def get_default_currency(self):
        """
        Only used for account registration
        """
        return CURRENCY_CODES.get(self.default_currency)

    def account_action(self, customer, add=True, path='/rpc/RequestData'):
        """
        Performs either an add or delete action for a korta account
        """
        params = self.get_defaults()
        params.update({
            KORTA.function_identifier: 1,
            KORTA.sub_function_identifier: 'A' if add else 'D',
            KORTA.reference: customer.reference,
        })
        if add:
            params.update({
                KORTA.charge_reference: 1,
                KORTA.amount: 100,
                KORTA.currency_exponent: 2,
                KORTA.currency_code: self.get_default_currency(),
                KORTA.storage_duration: customer.duration,
                KORTA.cc_number: customer.credit_card.number,
                KORTA.cc_verify_code: customer.credit_card.ccv,
                KORTA.cc_expire: customer.credit_card.expires})

        return self.do_request(path, params)

    def request_authorization(self, order, dt=None, reference=None, cc=None,
            ccv=None, cc_expire=None, path='/rpc/RequestAuthorisation'):
        """
        Requests authorization for a transaction
        """
        dt = (dt or datetime.datetime.now()).strftime(
            KORTA.date_format)

        params = self.get_defaults()
        params.update({
            KORTA.amount: order.amount,
            KORTA.currency_code: order.currency,
            KORTA.currency_exponent: order.currency_exponent,
            KORTA.current_date: dt,
            KORTA.reference_id: order.reference,
        })

        if reference:
            params.update({
                KORTA.reference: reference,
                KORTA.charge_reference: 1})

        if all((cc, ccv, cc_expire)):
            params.update({
                KORTA.cc_number: cc,
                KORTA.cc_verify_code: ccv,
                KORTA.cc_expire: cc_expire})
        return self.do_request(path, params)

    def one_off_req(self, order, credit_card, dt=None):
        return self.request_authorization(order, cc=credit_card.number,
            ccv=credit_card.ccv, cc_expire=credit_card.expires, dt=dt)

    def one_off(self, order, credit_card, dt=None):
        """
        Does a one off
        """
        r = self.one_off_req(order, credit_card, dt=dt)
        if r.action_code != '000':
            self.log.error('Response error: %s' % r.error_text)
            return False
        return (self.request_capture(r).action_code == '000')

    def request_capture(self, _params, path='/rpc/RequestCapture'):
        """
        You should only be calling this function with the result dictionary
        of a request_authorization call.
        """

        drop = ['MASK_CC',
            'ACTION_CODE_TEXT',
            'ERROR_TEXT',
            'ERROR_CODE',
            'CARD_BRAND_NAME',
            'UNKNOWN',
        ]

        params = dict([(KORTA.get(k, k), v)
            for (k, v) in list(_params.items())
                if k not in drop])

        for i in ['12', '39', '38']:
            params['o%s' % i] = params['d%s' % i]

        params.update({
            KORTA.user: self.user,
            KORTA.password: self.password})

        return self.do_request(path, params)

    def save_account(self, customer):
        """
        Saves an instance of a customer
        """
        return (self.account_action(customer).action_code == '000')

    def delete_account(self, customer):
        """
        Deletes an instance of a customer

        """
        return (self.account_action(customer,
            add=False).action_code == '000')
