import setuptools


def _requires_from_file(filename):
    return open(filename).read().splitlines()

print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

setuptools.setup(
    name="mypackage",
    version="0.0.1",
    author="masayan",
    author_email="masayan@example.com",
    description="mypackage is my own python package",
    long_description="The halloween party has gone over...",
    long_description_content_type="text/markdown",
    url="https://??????",
    packages=setuptools.find_packages(),
    #install_requires=_requires_from_file('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)