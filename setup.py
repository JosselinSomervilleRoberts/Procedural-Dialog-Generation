# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 18:53:38 2020

@author: josse
"""

from setuptools import setup

setup(name='psclib',
      version='0.1',
      description='Librairie pour le PSC',
      author='Josselin Somerville',
      author_email='josselin.somerville@gmail.com',
      license='MIT',
      packages=['psclib'],
      install_requires=[
          'verbecc',
          'google_trans_new',
          'random',
          'numpy',
          're',
          'sys',
      ],
      zip_safe=False)