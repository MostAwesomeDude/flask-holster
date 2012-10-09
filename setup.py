#!/usr/bin/env python

from setuptools import setup

setup(
    name="Flask-Holster",
    version="0.1.2",
    url="http://github.com/MostAwesomeDude/flask-holster",
    license="MIT",
    author="Corbin Simpson",
    author_email="cds@corbinsimpson.com",
    description="Rigid MVC content negotiation for Flask",
    long_description=open("README.rst").read(),
    packages=["flask_holster"],
    test_suite="flask_holster.test",
    zip_safe=False,
    platforms="any",
    install_requires=[
        "Flask",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
