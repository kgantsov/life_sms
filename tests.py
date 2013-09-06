import unittest
from life_sms import life_sms
from life_sms import life_sms_exceptions as exceptions

LOGIN = 'login'
PASSWORD = 'password'
ALPHA_NAME = 'MyBestCompany'


class LifeSmsTests(unittest.TestCase):

    def test_parse_status_response(self):
        """Sending a single SMS with the minimum detail and no errors should
        work.
        """
        sms = life_sms.LifeSms(
            LOGIN, PASSWORD, ALPHA_NAME
        )
        response_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <status id="8072817" date="Fri, 06 Sep 2013 19:11:16 +0300">
            <state>Accepted</state>
        </status>
        '''
        status = sms.parse_status_response(
            mode='single', response_content=response_content
        )
        self.assertEqual(status['id'], '8072817')

        response_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <status date="Fri, 06 Sep 2013 19:11:16 +0300">
            <state error="Invalid message">Accepted</state>
        </status>
        '''
        status = sms.parse_status_response(
            mode='single', response_content=response_content
        )
        self.assertFalse('id' in status)
        self.assertTrue('error' in status)
        self.assertEqual(status['error'], 'Invalid message')

        response_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <status groupid="593589" date="Fri, 06 Sep 2013 22:11:05 +0300">
            <id>8076414</id>
            <id>8076415</id>
            <state>Accepted</state>
            <state>Accepted</state>
        </status>'''
        status = sms.parse_status_response(
            mode='bulk', response_content=response_content
        )
        self.assertFalse('id' in status)
        self.assertTrue('groupid' in status)
        self.assertEqual(status['groupid'], '593589')
        self.assertEqual(
            status['statuses'],
            [('8076414', 'Accepted', None), ('8076415', 'Accepted', None)]
        )

        response_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <status groupid="593598" date="Fri, 06 Sep 2013 22:50:17 +0300">
            <state>sent</state>
            <total>2</total>
            <queued>0</queued>
            <accepted>0</accepted>
            <enroute>-2</enroute>
            <delivered>2</delivered>
            <expired>0</expired>
            <undeliverable>0</undeliverable>
            <unknown>0</unknown>
        </status>'''
        status = sms.parse_status_response(
            mode='individual', response_content=response_content
        )
        self.assertFalse('id' in status)
        self.assertTrue('groupid' in status)
        self.assertEqual(status['groupid'], '593598')
        self.assertEqual(status['total'], '2')
        self.assertEqual(status['queued'], '0')
        self.assertEqual(status['enroute'], '-2')
        self.assertEqual(status['undeliverable'], '0')

        self.assertRaises(
            exceptions.XMLException,
            sms.parse_status_response,
            {response_content: ''}
        )

if __name__ == "__main__":
    unittest.main()
