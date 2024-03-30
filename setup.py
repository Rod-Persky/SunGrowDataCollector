from setuptools import find_packages, setup
import os

# Get GitVersion_MajorMinorPatch from environment
gitversion = os.environ.get('GitVersion_MajorMinorPatch', '0.0.0')

setup(
    name='SunGrowDataCollector',
    version=gitversion,

    url='https://github.com/Rod-Persky/SunGrowDataCollector',
    author='Rod Persky',
    author_email='rodney.persky@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    packages=find_packages(),
    
    install_requires=[
        'aiohttp>=3.9.3'
    ],
    
    entry_points={
        'console_scripts': [
            'sungrowdatacollector=SunGrowDataCollector.main:startup',
        ],
    },
    
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
