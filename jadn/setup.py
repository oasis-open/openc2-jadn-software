from setuptools import setup, find_packages

setup(
    name='oc2',

    version='0.0.1',

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

    install_requires=open('requirements.txt', 'r').readlines(),

    # Python 2.7 up but not 4
    python_requires='>=2.7, !=3.1, !=3.2, !=3.3, !=3.4, !=3.5, <4',

    package_data={
        'oc2': [
            'libs/*',
        ]
    }
)
