# -*- coding: utf-8 -*-
import scrapy
from ..items import GscholarItem
import os.path

class InfoSpider(scrapy.Spider):
    #spidername
    name = 'info'
    counter_page = 1

    #start request for each author
    def start_requests(self):

        #to get relative path
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath,"authors.txt")

        #open file
        with open(filepath) as f:
            author_names = list(f)

        #for every name listed set the url
        for title in author_names:
            search_url = f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={title.strip()}'

            #Request url
            yield scrapy.Request(url=search_url, callback=self.parse)

    def parse(self, response):
        items = GscholarItem()

        # to get all the information we need from a tag field we find a tag that contains all
        doc_title = response.xpath('//div[@class="gs_r gs_or gs_scl"]')
        for r in doc_title:

            title = r.css('.gs_ri .gs_rt a::text').extract()

            #because info  returns many authors we have to join all the values together in order to pass them
            #to db
            author = ','.join(r.css('.gs_a a').css('::text').extract())
            cit_by = r.css('.gs_or_cit+ a').css('::text').extract()

            # h1 a:not(span)::text
            # to get only the name of doc
            file = ''.join(r.css('.gs_or_ggsm a:not(span)::text').extract())
            link = r.css('.gs_ri .gs_rt a::attr(href)').extract()

            if file == "" :
                items['file'] = 'dont have source'
            else:
                items['file'] = [file]
                yield items
            items['title'] = title
            items['author'] = author
            items['cited_by'] = cit_by

