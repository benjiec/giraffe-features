#!/usr/bin/env python

from setuptools import setup

setup(name='giraffe_features',
      version='3.0',
      description='Giraffe compatible biological feature description',
      author='Benjie Chen',
      author_email='benjie@alum.mit.edu',
      packages=['giraffe_features'],
      package_dir={"giraffe_features": "."},
      install_requires=[])
