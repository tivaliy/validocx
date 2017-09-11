from os import path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Information Technology',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Text Processing :: General',
]

setup(
    name='validocx',
    version='0.0.1',
    description='An implementation of MS Word docx-file content validator',
    long_description=long_description,
    url='https://github.com/tivaliy/docx-validator',
    author='Vitalii Kulanov',
    author_email='vitaliy@kulanov.org.ua',
    license='MIT',
    classifiers=classifiers,
    keywords='MS-Word docx validator',
    packages=['validocx'],
    entry_points={
        'console_scripts': [
            'validocx = validocx.cli:main',
        ],
    },
)
