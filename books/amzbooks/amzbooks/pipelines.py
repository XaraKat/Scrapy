# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3

class AmzbooksPipeline:
    def __init__(self):
        self.create_conn()
        self.create_table()
    def create_conn(self):
        self.conn = sqlite3.connect("documents.db")

        #we call cursor
        self.curr= self.conn.cursor()

    def create_table(self):
        #from cursor we call method execute to do these queries
        self.curr.execute("""DROP TABLE IF EXISTS docs_tb""")
        self.curr.execute("""create table docs_tb(Title text,Authors text,Cited_by text,description text)""")

    def process_item(self, item, spider):
        #store only items from  spider named info
        #else return item
        if spider.name not in ['info']:
            return item
        else:
            self.store_db(item)
            return item

    def store_db(self,item):
        #insert title,author,citation,page source into db
        self.curr.execute("""insert into docs_tb values (?,?,?,?)""",(
            item['title'][0],

            #take all authors on the same line
            [item['author']][0],
            item['cited_by'][0],
            item['file'][0]
        ))
        self.conn.commit()

