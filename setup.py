from setuptools import setup

requires = [
        "twilio",
        "pyyaml",
        "shove",
        "flask",
        'requests',]

setup(
        name="catfacts",
        version="0.1.0",
        author="Ross Delinger",
        author_email="rdelinger@helixoide.com",
        install_requires=requires,
        entry_points="""
        [console_scripts]
        catfacts = catfacts:main
        """
        )
