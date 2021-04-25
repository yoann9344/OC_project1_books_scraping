from setuptools import setup

setup(
    name='getbooks',
    version='0.1',
    py_modules=['getbooks'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        getbooks=getbooks:cli
    ''',
)
