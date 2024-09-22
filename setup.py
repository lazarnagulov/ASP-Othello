from setuptools import setup, find_packages

setup(
    name='Othello',
    version='2.0',
    author="Lazar Nagulov",
    description="Implementation of Othello game.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
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
)