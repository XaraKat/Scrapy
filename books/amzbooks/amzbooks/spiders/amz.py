# -*- coding: utf-8 -*-

from scrapy.http.request import Request
import scrapy
from ..items import AmzbooksItem

class AmzSpider(scrapy.Spider):
    name = 'amz'

    start_urls = ['https://www.skroutz.gr/books/search.html?from=latest_keyphrases&keyphrase=stephen+king']

    def parse(self, response):
        items = AmzbooksItem()
        whole = response.css('.card')
        for res in whole:

            page = res.css('h2 a::attr(href)').get()
            book_page = 'https://www.skroutz.gr/' + page
            yield Request(url = book_page,callback =self.parse_details,meta= {'items' :items})

    def parse_details(self,response):
        items = response.meta['items']
        whole =response.css('.js-product-card')
        title = response.css('.page-title::text').extract()
        author = response.css('#sku-details li:nth-child(1) a::text').extract()
        for res in whole:
            price = res.css('.product-link::text').extract()

            items['product_price1'] = price


            items['title'] = title
            items['product_author1'] = author

            yield items
