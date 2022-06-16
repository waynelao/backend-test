"""
Idex python package configuration.

Yejun Lao
"""

from setuptools import setup

setup(
    name='index',
    version='0.1.0',
    packages=['index'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
        'selenium',
    ],
    python_requires='>=3.6',
)