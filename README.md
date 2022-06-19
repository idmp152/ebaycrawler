![Logo](https://media.discordapp.net/attachments/955362477137362954/969693707450323055/project_logo.png?width=1394&height=416)
## 
[![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-383/)
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)
[![GitHub stars](https://badgen.net/github/stars/ov3rwrite/ebaycrawler)](https://GitHub.com/ov3rwrite/ebaycrawler/stargazers/)
[![GitHub issues](https://badgen.net/github/issues/ov3rwrite/ebaycrawler)](https://GitHub.com/ov3rwrite/ebaycrawler/issues/)
![Maintenance](https://img.shields.io/maintenance/yes/2022)
![PyPi](https://img.shields.io/pypi/v/ebaycrawler)
![Commits](https://img.shields.io/github/commit-activity/m/ov3rwrite/ebaycrawler)

EbayCrawler is a crawler that parses eBay and writes the data in a file. This project is just an experiment and should better not be used in a real situation. eBay has a public API to use instead (see https://developer.ebay.com/api-docs/developer/static/developer-landing.html) and this project is made to learn such libraries as aiohttp or bs4 and to practice my software developing skills.

## Installation

```cmd
pip install ebaycrawler
```

## Usage
```cmd
ebaycrawler [-h] --urls URLS [URLS ...] --mode {list} [--file-path [FILE_PATH]]
```
`--urls` or `-u` - a required argument that represents the urls that have to be parsed, e.g.
```
--urls https://www.ebay.ca/b/Cars-Trucks/6001/bn_1865117 https://www.ebay.ca/b/adidas/bn_21818843
```
`--mode` or `-m` - a required argument that represents the mode in which the provided urls should be parsed e.g.
```
--mode=list
```
or
```
-m=card
```
`--file-path` or `-fp` - an optional argument that represents the path where the table with parsed items should be saved (./saved_documents/<current_datetime> by default) e.g.
```
--file-path=./my_folder/test.xlsx
```
Supported file formats:
- `xlsx`
