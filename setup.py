from setuptools import setup, find_packages

# PLEASE DO NOT EDIT THIS, MANAGED FOR CI PURPOSES
__QUALIFIER__ = ""

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="microcosm_connexion",
    version="0.1.0" + __QUALIFIER__,
    description="A python library that exposes microcosm factories for connexions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Srikalyan Swayampakula",
    author_email="",
    url="https://github.com/srikalyan/microcosm-connexion",
    packages=find_packages(exclude=["*.tests"]),
    test_suite="microcosm_connexion.tests",
    setup_requires=[
        "pytest-runner",
    ],
    install_requires=[
        "connexion>=2.4.0,<3",
        "inflection>=0.3.1,<1",
        "microcosm>=2,<3",
        "microcosm-flask>=2.2.0,<3",
    ],
    extras_require={
        "postgres": [
            "microcosm-postgres>=1.17.0,<2.0.0",
        ]
    },
    tests_require=[
        "mock",
        "pyhamcrest",
        "pytest",
        "pytest-cov",
    ],
    entry_points={
        "console_scripts": [],
        "microcosm.factories": [
            "connexion = microcosm_connexion.factories:configure_connexion",
        ],
    },
)
