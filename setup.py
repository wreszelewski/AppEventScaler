#!/usr/bin/env python

from setuptools import setup

setup(name='vm_agent',
      version='1.0',
      description='AppEventScaler vm_agent',
      author='Wojceich Reszelewski',
      author_email='photografia@op.pl',
      packages=['app_scaler'],
      scripts=['vm_agent'],
      data_files=[('/etc/init.d', ['aesc_minion']),
                  ('/usr/sbin', ['vm_agent']),
                  ('/etc', ['aesc_minion.conf'])],
      install_requires=['tornado', 'boto3']
     )
