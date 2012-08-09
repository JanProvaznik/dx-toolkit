#!/usr/bin/env python

import os, sys, glob
from setuptools import setup, find_packages

# Grab all the scripts from dxpy/scripts and install them without their .py extension.
# Replace underscores with dashes.
# See Readme.md for details.
scripts = []
for module in os.listdir('dxpy/scripts'):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    module = module[:-3]
    script = module.replace('_', '-')
    scripts.append("{s} = dxpy.scripts.{m}:main".format(s=script, m=module))

setup(
    name='dxpy',
    version='0.1',
    description='DNAnexus Platform API bindings for Python',
    author='Katherine Lai, Andrey Kislyuk',
    author_email='klai@dnanexus.com, akislyuk@dnanexus.com',
    url='https://github.com/dnanexus/nucleus_client',
    license='as-is',
    packages = find_packages(),
    #scripts = glob.glob('scripts/*.py'),
    entry_points = {
        "console_scripts": scripts,
    },
    install_requires = ['requests==0.12.1',
                        'futures==2.1.2',
                        'ctypes-snappy==1.02',
                        'ws4py==0.2.2'],
)
