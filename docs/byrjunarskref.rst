.. _byrjunarskref:

=============
Byrjunarskref
=============

Forkröfur
=========

Aðgangsupplýsingar frá Kortaþjónustunni þar með talin SSL skilríki.

Notkun
======

Eftirfarandi bútur setur 100.kr færslu á kort. Athugið að upphæð er samansett
úr heiltölu og vísi, 10000 með exponent 2 er því 100.00 kr.

.. code-block:: python

    >>> from korta.client import Client, CreditCard, Order, korta_reference
    >>> c = Client('/path/to/my/pem', '/path/to/my/crt',
    ...    'user_id', 'password', 'site_id', 'acceptor_id',
    ...    'acceptor_terminal')
    >>> ref = korta_reference()
    >>> result = c.one_off(Order(ref, 10000, exponent=2), CreditCard(number, month, year, ccv))
    >>> print('100.kr richer' if result else 'Error')
