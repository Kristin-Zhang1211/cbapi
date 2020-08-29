#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 22:09:06 2020

@author: kristinquality
"""

from setuptools import setup

setup(
      name='cbapi',
      version='1.0.0',
      author='ting zhang',
      url='https://github.com/Kristin-Zhang1211/cbapi',
      description='a package to get the info of organizations and people on CrunchbaseAPI',
      long_description=open('README.md').read(),
      install_requires=['pandas', 'requests'],
      packages=['cbapi'],
      )
