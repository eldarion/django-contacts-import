from distutils.core import setup
from setuptools import find_packages


setup(
    name = "django-contacts-import",
    version = "0.1.dev4",
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "contact importing for Django",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/django-contacts-import",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
