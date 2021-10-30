![Logo](https://github.com/ov3rwrite/ebaycrawler/raw/main/readme/project_logo.png)
***
## Description
EbayCrawler is a crawler that parses eBay and writes the data in a file. This project is just an experiment and should better not be used in a real situation. eBay has a public API to use instead (see https://developer.ebay.com/api-docs/developer/static/developer-landing.html) and this project is made to learn such libraries as aiohttp or bs4 and to practice my software developing skills.

## Usage
```cmd
main.py [-h] --urls URLS [URLS ...] --mode {list} [--file-path [FILE_PATH]]
```
`--urls` or `-u` - required argument that represents urls that have to be passed, e.g.
```
--urls https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117 https://www.ebay.com/b/adidas/bn_21818843
```
`--mode` or `-m` - required argument that represents the mode in which the provided urls should be parsed e.g.
```
--mode=list
```
or
```
-m=card
```
`--file-path` or `-fp` - optional argument that represents the path where the table with parsed items is saved (./saved_documents/<current_datetime> by default) e.g.
```
--file-path=./my_folder/test.xlsx
```
Supported file formats:
<li>xlsx</li>

## Requirements
<li>bs4</li>
<li>asyncio</li>
<li>aiohttp</li>
<li>requests</li>
<li>pandas</li>
See requirements.txt for quick install. 

## Documentation

### Class
```python
class fileio.writers.TableWriter(rows: Iterable[Iterable])
```
Abstract class that details common operations on table-type files like .xlsx or .csv

***

### Class
```python
class fileio.writers.ExcelWriter(rows: Iterable[Iterable])
```
Class that implements `fileio.writers.TableWriter` and details writing operations on the .xlsx format.

#### Methods
```python
def write_to_file(self, file_path: str = <default file path>, header: Iterable[str] = None)
```
Writes the given rows to an .xlsx file with the specified path and header row.

```python
def set_rows(rows: Iterable[Iterable])
```
Updates the inner rows field that is used in the `write_to_file` method.

#### Fields
```python
DEFAULT_FILE_PATH = f"./saved_documents/{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.xlsx"
```
Default path to save `write_to_file` files.

***

### Class
```python
class parsing.requesters.Requester(urls: Iterable[str])
```
Abstract class that details common requesting operations.

***
### Class
```python
class parsing.requesters.SynchronousRequester(urls: Iterable[str])
```

Class that implements `parsing.requesters.Requester` and details synchronous requesting operations.

#### Methods
```python
def parse_urls() -> List[str]
```
Parses the given urls and returns a list of responses.

```python
def set_urls(urls: Iterable[str])
```
Updates the inner urls field that is used in the `parse_urls` method.

***
### Class
```python
class parsing.requesters.AsynchronousRequester(urls: Iterable[str])
```
Class that implements `parsing.requesters.Requester` and details asynchronous requesting operations.

#### Methods
```python
def parse_urls() -> List[str]
```
Parses the given urls and returns a list of responses.

```python
def set_urls(urls: Iterable[str])
```
Updates the inner urls field that is used in the `parse_urls` method.
***
### Class
```python
class parsing.parsers.EbayParser(requester: Requester)
```
Class that details item parsing operations on the eBay site.

#### Methods
```python
def parse_items_from_list_pages() -> List[Item]
```
Parses items from the given Requester.

```python
def set_requester(requester: Requester)
```
Updates the inner requester field that is used in the parsing methods.
#### Fields
```python
Item = namedtuple("Item", ["name", "price"])
```
Namedtuple that represents the eBay item type.
***
### Class
```python
class ParsingModes
```
Enum that represents eBay parsing modes e.g. ParsingModes.LIST.

#### Methods
```python
@staticmethod
def get_mode_by_string(string: str)
```
Method that returns ParsingModes enum value depending on the given string.

#### Fields
```python
LIST_PAGE = auto()
```
```python
UNKNOWN = auto()
```
