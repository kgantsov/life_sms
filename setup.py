#!/usr/bin/env python
""" Setup file for Simimg package """


from setuptools import setup

tests_require = [
    'nose==1.2.1',
    'mock==1.0.1',
    'coveralls',
]

setup(
    name='life_sms',
    version='0.1',
    description='life_sms package',
    long_description="Life Bulk Messaging Solution library",
    author='Gantsov Konstantin',
    author_email='k.gantsov@gmail.com',
    packages=['life_sms'],

    install_requires=[
        "lxml==3.2.3",
    ],
    tests_require=tests_require,
    test_suite="nose.collector",
    extras_require={'test': tests_require},
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ),
    license="GPL-2"
)
