#! /usr/bin/env python
# encoding: utf-8


class HttpException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AuthException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APIException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
