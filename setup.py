from setuptools import setup, find_packages

setup(name='bitly',
        version='20100126.1',
        description='A thin wrapper for the bit.ly REST api',
        author='Lars Kellogg-Stedman',
        author_email='lars@oddbit.com',
        packages=['bitly'],
        scripts=['scripts/bitly',]
        )
