#!/usr/bin/env python
""" Setup file for Simimg package """


from distutils.core import setup

setup(
    name='life_sms',
    version='0.1',
    description='life_sms package',
    long_description="Life Bulk Messaging Solution library",
    author='Gantsov Konstantin',
    author_email='k.gantsov@gmail.com',
    packages=['life_sms'],

    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
    ),
    license="GPL-2"
)
