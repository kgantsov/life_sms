#! /usr/bin/env python
# encoding: utf-8

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

from lxml import etree

import life_sms_exceptions as exceptions

SMS_BASE_URL = 'http://api.life.com.ua'
SMS_STATUS_URL = 'https://api.life.com.ua/ip2sms-request/'
SMS_SEND_URL = 'https://api.life.com.ua/ip2sms/'


class LifeSms(object):
    """docstring for LifeSms"""
    def __init__(self, login, password, alpha_name):
        super(LifeSms, self).__init__()
        self.login = login
        self.password = password
        self.alpha_name = alpha_name

    def send(self, message, phone, start=None, validity=None):
        """Send single message to phone
        """

        sms_data = self.__build_sms_data(
            'single', [message], [phone], start=start, validity=validity
        )
        return etree.tostring(sms_data)
        response = self.__request(SMS_SEND_URL, etree.tostring(sms_data))
        status = self.parse_status_response(response.content)
        return status

    def send_bulk(
        self, message, phones, uniq_key, desc=None, start=None, validity=None
    ):
        """Send message to severals phones at the same time
        """

        sms_data = self.__build_sms_data(
            'bulk',
            [message],
            phones,
            uniq_key=uniq_key,
            start=start,
            validity=validity
        )
        return etree.tostring(sms_data)
        response = self.__request(SMS_SEND_URL, etree.tostring(sms_data))
        status = self.parse_status_response(response.content)
        return status

    def send_individual(
        self, messages, phones, uniq_key, desc=None, start=None, validity=None
    ):
        """Send individual messages to severals phones at the same time
        """

        sms_data = self.__build_sms_data(
            'individual',
            messages,
            phones,
            uniq_key=uniq_key,
            start=start,
            validity=validity
        )
        return etree.tostring(sms_data)
        response = self.__request(SMS_SEND_URL, etree.tostring(sms_data))
        status = self.parse_status_response(response.content)
        return status

    def __build_sms_data(
        self,
        mode,
        messages,
        phones,
        uniq_key=None,
        desc=None,
        start=None,
        validity=None,
    ):
        """Build data XML for sending for sending this data to server.
        """

        xml_root = etree.Element('message')
        xml_service = etree.SubElement(xml_root, 'service')
        xml_service.set('id', mode)
        xml_service.set('source', self.alpha_name)

        if desc:
            xml_service.set('desc', desc)

        if uniq_key:
            xml_service.set('uniq_key', uniq_key)

        if start:
            xml_service.set('start', start)

        if validity:
            xml_service.set('validity', validity)

        if mode == 'individual':
            for phone, message in zip(phones, messages):
                xml_phone = etree.SubElement(xml_root, 'to')
                xml_phone.text = phone

                xml_body = etree.SubElement(xml_root, 'body')
                xml_body.set('content-type', 'text/plain')
                xml_body.text = message
        else:
            for phone in phones:
                xml_phone = etree.SubElement(xml_root, 'to')
                xml_phone.text = phone

            for message in messages:
                xml_body = etree.SubElement(xml_root, 'body')
                xml_body.set('content-type', 'text/plain')
                xml_body.text = message

        return xml_root

    def status(self, message_id):
        """Get status of sent message by its id
        """

        status_request = etree.Element('request')
        status_request.set('id', message_id)
        status_request.text = 'status'

        response = self.__request(
            SMS_STATUS_URL, etree.tostring(status_request)
        )
        status = self.parse_status_response(response.content)
        return status

    def parse_status_response(self, mode='single', response_content=''):
        """Parse the returned XML from life sms server.
        """

        status = {}
        response_xml = etree.XML(response_content)

        if mode == 'single':
            if 'id' in response_xml.attrib:
                status['id'] = response_xml.attrib['id']
                status['status'] = response_xml[0].text

            if 'error' in response_xml[0].attrib:
                status['error'] = response_xml[0].attrib['error']

        elif mode == 'bulk':
            if 'groupid' in response_xml.attrib:
                status['groupid'] = response_xml.attrib['groupid']

                ids = []
                statuses = []
                errors = []
                for item in response_xml:
                    if item.tag == 'id':
                        ids.append(item.text)
                    elif item.tag == 'state':
                        errors.append(item.attrib.get('error', None))
                        statuses.append(item.text)
                status['statuses'] = zip(ids, statuses, errors)
        elif mode == 'individual':
            for item in response_xml:
                status[item.tag] = item.text

        status['date'] = response_xml.attrib['date']

        return status

    def __request(self, url, xml):
        """Make a http request to life sms server, using the XML.
        If there is a problem with the http connection a HttpException is
        raised.
        """

        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        try:
            response = requests.post(
                url,
                xml,
                headers=headers,
                auth=HTTPBasicAuth(self.login, self.password)
            )
        except RequestException as error:
            raise exceptions.HttpException(
                "Error connecting to life sms server: %s" % error
            )

        return response
