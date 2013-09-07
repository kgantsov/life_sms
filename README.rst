life_sms
========

.. image:: https://travis-ci.org/kgantsov/life_sms.png?branch=master
    :target: https://travis-ci.org/kgantsov/life_sms

Life Bulk Messaging Solution library

Install
=======

    python setup.py install


Requirements
============

* `Python <http://www.python.org/>`_ 2.7 or 3.3
* `Requests <http://docs.python-requests.org/>`_
* `lxml <http://lxml.de/>`_ 


Usage:
======

Sending single message

    from life_sms import LifeSms

    sms = LifeSms('login', 'password', 'AlphaName')

    status = sms.send(u'Message test', '0981112233')


Send bulk messages:

    status = sms.send_bulk(
        self.message, ['0981233232', '0671234343'], uniq_key='12345'
    )


Send individual messages:

    status = sms.send_individual(
        ['Hello Fill', 'Hello Jhon', 'Hello Kevin'],
        ['0981233232', '0671234343', '0671239898'],
        uniq_key='123456'
    )


Get status of sent message by its id:

    status = sms.status('8072382')

