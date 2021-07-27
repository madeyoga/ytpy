from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name="ytpy",
    version="2021.7.27",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        "asyncio",
        "aiohttp",
        "urllib3"
        ],

    package_data={
        
    },

    # metadata to display on PyPI
    author="yeogaa",
    author_email="yeogaa02@gmail.com",
    description="Python asynchronous wrapper to get youtube data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="youtube-api-v3 python youtube-search asynchronous",
    url="https://github.com/madeyoga/ytpy",
)
