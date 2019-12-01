from setuptools import setup

setup(
    name='OrderBook',
    version='0.1.2',
    author='Michael Nguyen',
    author_email='dyn4mik3@gmail.com',
    packages=['orderbook'],
    url='http://pypi.python.org/pypi/OrderBook/',
    license='LICENSE.txt',
    description='Limit Order Book Matching Engine',
    install_requires=[
        'sortedcontainers >= 2'
        ],
    scripts=['bin/algosim.py']
    )
