import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from csv import DictWriter
import os
from urllib.parse import urlencode
import time 

class AmzBookScraper(scrapy.Spider):
    
    name = 'amz_book_spider'
    start_urls = [
        'https://www.amazon.co.uk/s?k=machine+learning&',
        ]
    allowed_domains = [
        'amazon.co.uk',
        ]
    
    headers = {
        
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.3; rv:99.0) Gecko/20100101 Firefox/99.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'referer': 'https://www.amazon.com/s?k=machine+learning&ref=nb_sb_noss',
        'upgrade-insecure-requests': '1',
        'cache-control': 'no-cache',
        'connection': 'keep-alive',
        'pragma': 'no-cache',
        'accept-encoding': 'gzip, deflate, br',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetcg-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
        
        }
    
    params = {
        'page': 1,
        #'qid':'1649321666',
        #'ref':'sr_pg_'
        }
    
    custom_settings = {
        
        'DOWNLOAD_DELAY': 10,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'CONCURRENT_REQUESTS': 1,
        'HTTPCACHE_ENABLED': False,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
                
    }
    
    starting_page = 1
    
    def __init__(self):
        
        # makes the directory and csv file to store the data into
        try:
            print("[+]Creating Directory...[+] ")
            directory_name = 'MLBooks'
            os.mkdir(directory_name)
            time.sleep(1)
            print("[+]Directory successfully created![+]")
            
            try:
                print('[+]Creating csv file...[+]')
                with open('MLBooks/ml_books.csv', 'w') as csv_file:
                    csv_file.write('Title,Ratings,Book_format,Price,Cover\n')
                    print('[+]csv successfully created![+]')
                    time.sleep(1)
            except FileExistsError as e:
                print(f"[-]This file already exist![-] -> {e}")
                time.sleep(1)
                
        except FileExistsError as e:
            print(f"[-]This directory already exist![-] -> {e}")
            time.sleep(1)
        
    # spider's entry point
    def start_request(self):
        yield Request(
            url=self.start_urls[0], 
            headers=self.headers, 
            callback=self.parse
            )
    
    def parse(self, response):            
        
        print('\n****PARSING!****\n')
        self.logger.info('Parse function called on %s', response.url)
        
        books = response.xpath(".//div[@class='s-card-container s-overflow-hidden aok-relative s-include-content-margin s-latency-cf-section s-card-border']")
        
        # features xpath
        for book in books:
            title = book.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()
            ratings = book.xpath(".//span[@class='a-icon-alt']/text()").get()
            book_format = book.xpath(".//a[@class='a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold']/text()").get()
            price = book.xpath(".//span[@class='a-offscreen']/text()").get()
            cover = book.xpath(".//img[@class='s-image']/@src").get()
            
            yield Request(
                url=self.start_urls[0],
                headers=self.headers, 
                callback=self.parse             
                )
                  
            # features we want to write into csv format
            items = {
                'title': title,
                'ratings': ratings,
                'book_format': book_format,
                'price': price,
                'cover': cover
            }    
                                
            # write the data into the csv file           
            with open('MLBooks/ml_books.csv', 'a') as csv_file:
                    csv_writer = DictWriter(csv_file, fieldnames=items.keys())
                    csv_writer.writerow(items)   
                
        # Go to next page if next page exists
        next_url = f"{self.start_urls[0]}{urlencode(self.params)}"
        if self.params['page'] <= 20:
            self.params['page'] += AmzBookScraper.starting_page
            yield response.follow(url=next_url, callback=self.parse)
        
# main driver    
if __name__ == '__main__':
    
    process = CrawlerProcess()
    process.crawl(AmzBookScraper)
    process.start()