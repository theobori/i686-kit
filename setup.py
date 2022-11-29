import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="i686tools",
    version="0.0.1",
    author="Théo Bori",
    author_email="theo1.bori@epitech.eu",
    description="Bunch of tools you prefer to have",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theobori/i686-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
