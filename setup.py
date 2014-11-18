# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='XXX Storage',
    version='1.0',
    long_description=__doc__,
    packages=['storageapp'],
    include_package_data=True,
    zip_safe=False,
    setup_requires=['Flask'],
    install_requires=['Flask', 'SQLAlchemy', 'Flask-Script']
)
