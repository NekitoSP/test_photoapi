from setuptools import setup, find_packages
import pathlib

root = pathlib.Path(__file__).parent.resolve()

long_description = (root / 'README.md').read_text(encoding='utf-8')

setup(
    name='photoapi',
    version='0.0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NekitoSP/test_photoapi',
    author='Nikita Permin',
    author_email='nekitosp@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8, <4',
    install_requires=[
        'Django==3.2.4',
        'Pillow==8.2.0',
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