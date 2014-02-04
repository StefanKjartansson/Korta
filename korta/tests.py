#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
korta.tests
~~~~~~~~~~~
"""
from __future__ import absolute_import

import os
import unittest

from .compat import configparser
from . import (Client, Customer,
    CreditCard, Order, korta_reference)


class KortaTestCase(unittest.TestCase):

    def setUp(self):
        root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
        config = configparser.RawConfigParser(allow_no_value=True)
        config.readfp(open(os.path.join(root_dir, 'userconfig.ini')))

        try:
            self.client = Client.init_from_url(config.get('korta', 'url'))
        except configparser.NoOptionError:
            self.client = Client(
                config.get('korta', 'user'),
                config.get('korta', 'password'),
                config.get('korta', 'host'),
                config.get('korta', 'port'),
                site_id=config.get('korta', 'site_id'),
                card_acceptor_id=config.get('korta', 'card_acceptor_id'),
                card_acceptor_identity=config.get('korta',
                    'card_acceptor_identity'),
                pem=config.get('korta', 'pem'),
                currency=config.get('korta', 'currency'),
            )

    def test_charge_reference(self):
        unique_reference = korta_reference()
        self.client.save_account(Customer(
            unique_reference,
            CreditCard(
                os.getenv('KORTA_TEST_NUMBER'),
                5, 14, 123),
        ))
        order_ref = korta_reference()
        auth = self.client.request_authorization(
            Order(order_ref, 1000),
            reference=unique_reference)
        cap = self.client.request_capture(auth)
        self.assertEqual(cap.action_code, '000')

    def test_one_off(self):
        x = korta_reference()
        c = CreditCard(os.getenv('KORTA_TEST_NUMBER'), 5, 14, 123)
        o = Order(x, 2000)
        self.assertEqual(self.client.one_off(o, c), True)
