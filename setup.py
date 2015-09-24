"""
AutoRedis installation script
"""

import os
from codecs import open as copen
from setuptools import setup

def get_long_description():
    """ Retrieve the long description from DESCRIPTION.rst """
    here = os.path.abspath(os.path.dirname(__file__))

    with copen(os.path.join(here, 'README.rst'), encoding='utf-8') as description:
        return description.read()
    
setup(
    name='AutoRedis',
    version='0.2.1',
    description='AutoRedis - Balance your Redis commands accross your master/slaves',
    long_description=get_long_description(),
    author='Emmanuel Vadot',
    author_email='manu@bidouilliste.com',
    url='https://github.com/evadot/AutoRedis',
    license='MIT',
    packages=['autoredis'],
    install_requires=['redis'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database :: Front-Ends',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='redis hiredis autoredis',
)
