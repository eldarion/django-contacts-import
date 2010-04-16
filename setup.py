from distutils.core import setup


setup(
    name = "django-contacts-import",
    version = "0.1.dev3",
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "contact importing for Django",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/django-contacts-import",
    packages = [
        "contacts_import",
        "contacts_import.backends",
        "contacts_import.templatetags",
    ],
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
