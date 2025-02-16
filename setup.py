from setuptools import setup, find_packages

setup(
    name='telext',
    version='1.0.0',
    url='https://github.com/sergzach/telext.git',
    author='Sergey Zakharov',
    author_email='sergzach@gmail.com',
    description='',
    packages=find_packages(include=['telext']),
    install_requires=[
        'aiohttp',
    ],
)