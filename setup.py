from setuptools import setup, find_packages

setup(
    name='Othello',
    version='1.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5',
    ],
    extras_require={
        'dev': [
            'mypy',
        ],
    },
    entry_points={
        'console_scripts': [
            'run=main:main',  
        ],
    },
)