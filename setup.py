# Copyright 2018-2019 Rene Rivera
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or http://www.boost.org/LICENSE_1_0.txt)

from setuptools import setup

setup(
    name='bls',
    description='''
        Utilities to inspect Boost C++ Libraries and generate relevant
        information and statistics.
        ''',
    version='0.2',
    url='https://github.com/grafikrobot/boost_lib_stats',
    author='Rene Rivera',
    author_email='grafikrobot@gmail.com',
    license='BSL 1.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Boost Software License 1.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
    ],
    keywords='boost statistics build',
    package_dir={'': 'src'},
    packages=['bls'],
    package_data={'..': ['LICENSE.txt']},
    install_requires=[])
