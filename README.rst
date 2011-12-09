Korta
=====

Python client fyrir Kortaþjónustuna. Mjög minimal og mjög beta í augnablikinu.


Notkun
------

Af því gefnu að þú sért með aðgangsupplýsingar frá kortu: ::

    >>> from korta.client import Client, CreditCard, Order, korta_reference
    >>> c = Client('/path/to/my/pem', '/path/to/my/crt',
    ...    'user_id', 'password', 'site_id', 'acceptor_id',
    ...    'acceptor_terminal')
    >>> ref = korta_reference()
    >>> c.one_off(Order(ref, 2000), CreditCard(number, month, year, ccv))


Uppsetning
----------

Til að setja upp þarf að keyra: ::

    $ python setup.py install


Prófanir
--------

*Af því gefnu að þú sért með aðgangsupplýsingar frá kortu.*

1. Búðu til userconfig.ini á sama leveli og setup.py með eftirfarandi gildum: ::

    [korta]
    user = user
    password = password
    site_id = number_from_korta
    card_acceptor_id = number_from_korta
    card_acceptor_identity = number_from_korta
    host = test.kortathjonustan.is
    pem_path = certs/test.rpcs.kortathjonustan.is.crt.pem
    ca_path = certs/ca-bundle.crt

2. Setja upp nose: ::

    $ pip install nose

3. Keyra: ::

    $ nosetests


Athugasemdir
------------

* Þarfnast pycurl, hef því ekki hugmynd hvort það virki á Windows.
* Default ssl pakkinn í Python styður ekki password callbackið úr openssl, ástæðan fyrir pycurl


Böggar og patchar
=================

Þróun fer fram á github: http://github.com/StefanKjartansson/Korta
