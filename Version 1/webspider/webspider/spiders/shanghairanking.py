# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from scrapy.selector import Selector

import xlwt


class ShanghairankingSpider(CrawlSpider):
    name = "Shanghairanking"

    def __init__(self, rule, worksheet, logging):
        CrawlSpider.__init__(self)
        # use any browser you wish
        self.browser = webdriver.Firefox()
        self.logging = logging
        self.rule = rule
        self.name = self.rule["ranking_name"]
        self.logging.info("==============================")
        self.logging.info("self.rule[start_urls]: %s" % self.rule["start_urls"])
        self.start_urls = self.rule["start_urls"]
        # slef.next_page is a defined array.
        self.next_page = self.rule["next_page"] \
                            if ("next_page" in self.rule) else ["NONE"]
        self.logging.info("#### self.next_page %s" % self.next_page)
        self.flag = self.rule["flag"] \
                            if ("flag" in self.rule) else ["NONE"]
        self.logging.info("#### self.flag %s" % self.flag)
        self.worksheet = worksheet
        self.logging.info("Finish the __init__ method ... ")

    def parse(self, response):

        self.logging.info("begin the logic of parse method ... ")

        self.browser.get(response.url)
        browser_response = Selector(text = self.browser.page_source)
        self.logging.info("type(browser_response): %s" % type(browser_response))

        # for the title of the table
        row_index = 0
        for col in self.rule["columns"]:
            data = browser_response.xpath(self.rule["columns"][col]["title"]).extract()
            self.worksheet.write(row_index, int(col)-1, data)

        # for the content of the table
        row_index = 1
        for select in browser_response.xpath(self.rule["table_tag"]):
            self.logging.info("select: %s" % select)
            self.logging.info("self.rule[\"columns\"]: %s" % self.rule["columns"])

            for col in self.rule["columns"]:
                data = select.xpath(self.rule["columns"][col]["content"]).extract()
                #self.logging.info("data: %s" % data)
                self.worksheet.write(row_index, int(col)-1, data)
            row_index += 1


        self.logging.info("Finish the logic of parse method ... ")
