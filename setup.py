from distutils.core import setup

setup(
    name='OrderBook',
    version='0.1',
    author='Michael Nguyen',
    author_email='dyn4mik3@gmail.com',
    packages=['orderbook'],
    url='http://pypi.python.org/pypi/OrderBook/',
    license='LICENSE.txt',
    description='Limit Order Book Trading Engine',
    long_description=open('README.txt').read(),
    install_requires=[
        "bintrees >= 2.0.1"
        ],
    )
