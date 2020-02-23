import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="busybee",
    version="0.1.0",
    author="Daniel H",
    author_email="not_provided@example.org",
    description="Simple and interactive multi-processing for Python and notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lambdapioneer/busybee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)
