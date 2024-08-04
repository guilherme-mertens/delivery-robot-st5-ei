from setuptools import setup, find_packages

setup(
    name='autonomous_delivery_robot',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List dependencies here
    ],
    entry_points={
        'console_scripts': [
            'main=src.main:main',
        ],
    },
)