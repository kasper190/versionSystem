import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='VersionSystem',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Version System',
    author='Krystian Kasperski',
    install_requires=[
        'django',
        'django-bootstrap-pagination'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11.3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)