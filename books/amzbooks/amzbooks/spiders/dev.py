# -*- coding: utf-8 -*-
import re
from scrapy.spiders import XMLFeedSpider
from ..items import DevBookItem


class XelSpider(XMLFeedSpider):
    name = 'xel'
    #set the namespaces
    namespaces = [('atom', 'http://www.w3.org/2005/Atom'),
                  ('dc','http://purl.org/dc/elements/1.1/'),
                  ('prism','http://prismstandard.org/namespaces/basic/2.0/'),
                  ('opensearch','http://a9.com/-/spec/opensearch/1.1/')]

    start_urls = ['https://api.elsevier.com/content/search/scopus?query=webcrawling&apiKey=7f59af901d2d86f78a1fd60c1bf9426a']

    #set the main tag for the node parsing
    itertag = 'atom:entry'
    iterator = 'xml'

    #method to parse each node
    def parse_node(self, response, node):

        #set DevBookItem from class items.py
        item = DevBookItem()

        #selectors for every node
        book_link = node.xpath('./atom:link[3]/@href').extract()
        abstract_url = node.xpath('./prism:url/text()').extract()

        idcode = node.xpath('./prism:issn/text()').extract()
        isbn_code = node.xpath('./prism:isbn/text()').extract()
        title = node.xpath('./dc:title/text()').extract()
        authors = node.xpath('./dc:creator/text()').extract()
        publication_name = node.xpath('./prism:publicationName/text()').extract()
        tags = node.xpath('./atom:subtypeDescription/text()').extract()
        category = node.xpath('./prism:aggregationType/text()').extract()
        load_date = node.xpath('./prism:coverDate/text()').extract()
        cited_by = node.xpath('./atom:citedby-count/text()').extract()
        affiliation_n = ','.join(node.xpath('./atom:affiliation/atom:affilname/text()').extract())
        affiliation_city = ','.join(node.xpath('./atom:affiliation/atom:affiliation-city/text()').extract())
        affiliation_country = ','.join(node.xpath('./atom:affiliation/atom:affiliation-country/text()').extract())
        #setting the response of each selector as item
        item['links'] = book_link
        item['abstract_url'] = abstract_url
        #some books dont have issn or isbn code
        if not idcode:
            item['issn_code'] = 'doc has only isbn code'
        else:
            item['issn_code'] = idcode
        if not isbn_code:
            item['isbn_code'] = 'doc has only issn code'
        else:
            item['isbn_code'] = isbn_code

        item['title'] = title
        item['author_names'] = authors
        item['p_name'] = publication_name
        item['description'] = tags
        item['category'] = category
        item['load_date'] = load_date
        item['cited_by'] = cited_by
        item['affil_university'] = affiliation_n
        item['affil_city'] = affiliation_city
        item['affil_country'] = affiliation_country

        #show all items
        yield item

