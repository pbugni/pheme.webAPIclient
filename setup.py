#!/usr/bin/env python

import os
from setuptools import setup

docs_require = ['Sphinx']
tests_require = ['nose', 'coverage']

try:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst')) as r:
        README = r.read()
except IOError:
    README = ''

setup(name='pheme.webAPIclient',
      version='13.7',
      description="Client interface to the PHEME Web API",
      long_description=README,
      license="BSD-3 Clause",
      namespace_packages=['pheme'],
      packages=['pheme.webAPIclient', ],
      include_package_data=True,
      install_requires=['setuptools', 'pheme.util', 'requests'],
      setup_requires=['nose'],
      tests_require=tests_require,
      test_suite="nose.collector",
      extras_require = {'test': tests_require,
                        'docs': docs_require,
                        },
      entry_points=("""
                    [console_scripts]
                    """),
)
