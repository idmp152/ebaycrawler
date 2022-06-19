from setuptools import setup, find_packages

requirements = [
    "bs4 ~= 0.0.1",
    "asyncio ~= 3.4.3",
    "aiohttp ~= 3.7.4.post0",
    "requests ~= 2.26.0",
    "pandas ~= 1.3.4",
    "openpyxl ~= 3.0.10",
    "colorama ~= 0.4.4"
]


setup(
    name="ebaycrawler",
    version="0.1.12",
    packages=find_packages("src"),
    package_dir={'': "src"},
    author="ov3rwrite",
    author_email="ilyabelykh123@gmail.com",
    install_requires = requirements,
    url="https://github.com/ov3rwrite/ebaycrawler",
    license="WTFPL",
    entry_points = {
        'console_scripts': [
            'ebaycrawler = ebaycrawler.main:main',
        ],
    }
)
