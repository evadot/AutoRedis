"""
AutoRedis installation script
"""

import os

from setuptools import setup

def get_long_description():
    """ Retrieve the long description from DESCRIPTION.rst """
    here = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as description:
        return description.read()

def get_version():
    """ Retrieve version information from the package """
    return __import__('autoredis').__version__
    
setup(
    name='AutoRedis',
    version=get_version(),
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
    ],
    keywords='redis hiredis autoredis',
)
