from setuptools import setup, find_packages
setup(
    name="ytpy",
    version="18.09.2020",
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
    author="madeyoga",
    author_email="yeogaa02@gmail.com",
    description="Python asynchronous wrapper for youtube data api v3.",
    keywords="youtube-api-v3 python youtube-search asynchronous",
    url="https://github.com/madeyoga/ytpy",
)
