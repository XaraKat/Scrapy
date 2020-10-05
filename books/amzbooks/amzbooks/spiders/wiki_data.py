# -*- coding: utf-8 -*-
import scrapy


class DataSpider(scrapy.Spider):
    name = 'data'

    start_urls = ['https://el.wikipedia.org/wiki/%CE%9A%CE%B1%CF%84%CE%AC%CE%BB%CE%BF%CE%B3%CE%BF%CF%82_%CE%BD%CE%BF%CF%83%CE%BF%CE%BA%CE%BF%CE%BC%CE%B5%CE%AF%CF%89%CE%BD_%CF%84%CE%B7%CF%82_%CE%95%CE%BB%CE%BB%CE%AC%CE%B4%CE%B1%CF%82']

    def parse(self, response):
        table = response.css('td:nth-child(1)')

        #for each row  of the table
        for res in table:
            hospital_name = res.css('td:nth-child(1) a::text').extract()
            location = res.css('td+ td a::text').extract()
            yield { 'hospital' : hospital_name ,
                    'location' : location}
