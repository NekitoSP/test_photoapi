from setuptools import setup, find_packages
import pathlib

root = pathlib.Path(__file__).parent.parent.resolve()

setup(
    name='photoapi',
    version='0.0.1',
    url='https://github.com/NekitoSP/test_photoapi',
    author='Nikita Permin',
    author_email='nekitosp@gmail.com',
    packages=find_packages(),
    python_requires='>=3.8, <4',
    install_requires=[
        'Django==3.2.4',
        'Pillow==8.2.0',
        'djangorestframework==3.12.4',
        'drf-yasg==1.20.0',
    ],
    extras_require={
        'dev': [],
        'test': [],
    },
    project_urls={
        'Bug Reports': 'https://github.com/NekitoSP/test_photoapi/issues',
        'Source': 'https://github.com/NekitoSP/test_photoapi',
    },
)