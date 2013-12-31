from distutils.core import setup

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
        "bintrees >= 2.0.1"
        ],
    )
