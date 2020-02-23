import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="busybee-TODO", # TODO: REPLACE!
    version="0.0.1",
    author="Daniel Hugenroth",
    description="Simple and interactive multi-processing for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lambdapioneer/busybee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
