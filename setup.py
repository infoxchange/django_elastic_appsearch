#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django_elastic_appsearch/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("django_elastic_appsearch", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst', encoding='utf-8').read()
history = open('HISTORY.rst', encoding='utf-8').read().replace('.. :changelog:', '')

setup(
    name='django_elastic_appsearch',
    version='2.1.0',
    description="""Integrate your Django Project with Elastic App Search with ease.""",
    long_description=readme + '\n\n' + history,
    author='Infoxchange',
    author_email='devs@infoxchange.org',
    url='https://github.com/infoxchange/django_elastic_appsearch',
    packages=[
        'django_elastic_appsearch',
    ],
    include_package_data=True,
    install_requires=[
        'elastic-enterprise-search>=7.15.0',
        'serpy',
    ],
    license="MIT",
    zip_safe=False,
    keywords='django_elastic_appsearch',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
