import json

from setuptools import setup, find_packages

versionData = json.loads(open('version.json', 'r').read())

setup(
    name=versionData['name'],

    version='{major}.{minor}.{bugfix}'.format(**versionData['version']['number']),

    description='OpenC2 Message Translator & Validator',
    # long_description="The Server for NetVamp, that provides the REST API, controllers, and database.",

    # author='G2-Inc. Solutions',
    # author_email='solutions@g2-inc.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security :: Translation :: Validation'
    ],

    packages=find_packages(),

    install_requires=[d.replace('\n', '') for d in open('requirements.txt', 'r').readlines()],

    # Python 2.7, 3.6+ but not 4
    python_requires='>=2.7, !=3.[1-5], <4',

    package_data={
        'OpenC2': [
            './{}/*'.format(versionData['pkg_name']),
        ]
    }
)
