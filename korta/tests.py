#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import unittest

from client import (Client, Customer,
    CreditCard, Order, korta_reference)


_path = lambda *x: os.path.join(os.path.abspath(
        os.path.dirname(__file__)), *x)


config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(open('userconfig.ini'))


class KortaTestCase(unittest.TestCase):

    def setUp(self):

        self.client = Client(
            _path(config.get('korta', 'pem_path')),
            _path(config.get('korta', 'ca_path')),
            config.get('korta', 'user'),
            config.get('korta', 'password'),
            config.get('korta', 'site_id'),
            config.get('korta', 'card_acceptor_id'),
            config.get('korta', 'card_acceptor_identity'),
            config.get('korta', 'host'),
        )

    def test_charge_reference(self):
        unique_reference = korta_reference()
        self.client.save_account(Customer(
            unique_reference,
            CreditCard(
                '4571999400007492',
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
        c = CreditCard('4571999400007492', 5, 14, 123)
        o = Order(x, 2000)
        self.assertEqual(self.client.one_off(o, c), True)
