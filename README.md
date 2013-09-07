life_sms
========

Life Bulk Messaging Solution library


Requirements
============

* `Python <http://www.python.org/>`_ 2.7
* `Requests <http://docs.python-requests.org/>`


Usage:
======
Import:

    from life_sms import LifeSms

Initialize:

    sms = LifeSms('login', 'password', 'AlphaName')


Send one message:

    status = sms.send(u'Message test', '0981112233')
  

Send bulk messages:

    status = sms.send_bulk(
        self.message, ['0981233232', '0671234343'], uniq_key='12345'
    )


Send individual messages:

    status = sms.send_individual(
        ['Hello Fill', 'Hello Jhon', 'Hello Kevin'],
        ['0981233232', '0671234343'],
        uniq_key='123456'
    )


Get status of sent message by its id:

    status = sms.status('8072382')

