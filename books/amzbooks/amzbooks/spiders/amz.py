# -*- coding: utf-8 -*-

from scrapy.http.request import Request
import scrapy
from ..items import AmzbooksItem
import os.path

class AmzSpider(scrapy.Spider):
    name = 'amz'

    #start request for each author
    def start_requests(self):

        #to get relative path
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath,"b_authors.txt")

        #open file
        with open(filepath) as f:
            author_names = list(f)

        #for every name listed set the url
        for title in author_names:
            search_url = f'https://www.skroutz.gr/books/search.html?from=latest_keyphrases&keyphrase={title.strip()}'

            #Request url
            yield scrapy.Request(url=search_url, callback=self.parse)


    def parse(self, response):
        items = AmzbooksItem()
        #selector for every book
        whole = response.css('.card')

        for res in whole:
            page = res.css('h2 a::attr(href)').get()
            book_page = 'https://www.skroutz.gr/' + page

            #visit every book page and get info
            yield Request(url = book_page,callback =self.parse_details,meta= {'items' :items})

    def parse_details(self,response):
        items = response.meta['items']
        whole =response.css('.js-product-card')
        title = response.css('.page-title::text').extract()
        author = response.css('#sku-details li:nth-child(1) a::text').extract()
        for res in whole:
            price = res.css('.product-link::text').extract()

            items['product_price'] = price
            items['title'] = title
            items['product_author'] = author

            yield items
