# Amazon-book-scraper
Amazon spider made by using Scrapy framework

## Run Locally
Clone the project

```bash
  git clone https://github.com/maxcohen31/Amazon-book-scraper.git
```
## Directory Structure
```bash
amazonscraper/
|-- amazonscraper
|   |-- __init__.py
|   |-- items.py
|   |-- middlewares.py
|   |-- MLBooks
|   |   `-- ml_books.csv
|   |-- pipelines.py
|   |-- __pycache__
|   |   |-- __init__.cpython-39.pyc
|   |   `-- settings.cpython-39.pyc
|   |-- settings.py
|   `-- spiders
|       |-- amazon_book_scraper.py
|       |-- __init__.py
|       `-- __pycache__
|           |-- amazon_book_scraper.cpython-39.pyc
|           `-- __init__.cpython-39.pyc
`-- scrapy.cfg
```
## Setup a virtual enviroment
```bash
virtualenv amazonscraper ; source bin/activate
pip install scrapy
```

## Go to the project directory

```bash
  cd Amazon-book-scraper
  cd amazonscraper/amazonscraper/spiders/
```

## Run the crawler
```bash
  python3 amazon_book_scraper.py
```
  
