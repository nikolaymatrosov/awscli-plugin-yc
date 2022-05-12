#!/usr/bin/env python
from setuptools import setup

requires = ['awscli>=1.11.0', 'yandexcloud']

setup(
    name='awscli-plugin-yc',
    packages=['awscli_plugin_yc'],
    version='0.1',
    description='Yandex Cloud plugin for AWS CLI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nikolay Matrosov',
    author_email='nikolay.matrosov@gmail.com',
    url='https://github.com/nikolaymatrosov/awscli-plugin-yc',
    download_url='https://github.com/nikolaymatrosov/awscli-plugin-yc/tarball/0.1',
    keywords=['awscli', 'plugin', 'yandex cloud'],
    install_requires=requires,
    classifiers=[]
)
