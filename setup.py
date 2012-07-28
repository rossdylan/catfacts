from setuptools import setup

requires = [
        "twilio",
        "pyyaml",
        "shove"]

setup(
        name="catfacts",
        version="0.1.0",
        author="Ross Delinger",
        author_email="rdelinger@helixoide.com",
        install_requires=requires,
        )
