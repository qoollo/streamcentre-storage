# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='StreamCentre Storage',
    version='0.2.0.0',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    setup_requires=['Flask'],
    install_requires=['Flask', 'SQLAlchemy', 'Flask-Script']
)
