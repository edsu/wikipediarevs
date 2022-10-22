from setuptools import setup

__version__ = "0.0.1"

def load_requirements(filename):
    with open(filename, "rt") as fh:
        return fh.read().rstrip().split("\n")

def long_description():
    with open("README.md") as f:
        return f.read()

setup(
    name="wikipediarevs",
    version=__version__,
    author="Ed Summers",
    author_email="ehs@pobox.com",
    license="MIT",
    py_modules=["wikipediarevs"],
    url="https://github.com/edsu/wikipediarevs",
    description="Download all the revisions for a set of Wikipedia articles",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    install_requires=load_requirements("requirements.txt"),
    zip_safe=True,
    setup_requires=["pytest-runner"],
    entry_points="""
        [console_scripts]
        wikipediarevs = wikipediarevs:main
    """,
)
