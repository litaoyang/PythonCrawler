# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from scrapy.selector import Selector

import xlwt


class FudanmedSpider(CrawlSpider):
    name = "fudanmed"

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

        row_index = 1
        # for the content of the table
        if self.flag[0] != "NONE": # has special cell to reget in flag
            if len(browser_response.xpath(self.rule["table_tag"])) == 0:
                self.logging.info("SPECIAL: select is none here, url: %s" \
                            % response.url)
            for select in browser_response.xpath(self.rule["table_tag"]):
                #logging.info("select: %s" % select)
                #logging.info("self.rule[\"columns\"]: %s" \
                #            % self.rule["columns"])
                for col in self.rule["columns"]:
                    data = select.xpath(\
                            self.rule["columns"][col]["content"]).extract()
                    # for QS and FUDAN:
                    #   reget data for special content
                    if "content_special" in self.flag[1] and data == [] \
                            and col in self.flag[1]["content_special"][0]:
                        data = select.xpath(self.rule["columns"]\
                                [col]["content_for_special"]).extract()
                        #logging.info("data: %s" % data)
                    # store data to sheet
                    self.worksheet.write(row_index, int(col)-1, data)
                row_index += 1
        else: # self.flag[0] is "NONE"
            if len(browser_response.xpath(self.rule["table_tag"])) == 0:
                logging.info("SPECIAL: select is none here, url: %s" \
                            % response.url)
            for select in browser_response.xpath(self.rule["table_tag"]):
                #logging.info("select: %s" % select)
                #logging.info("self.rule[\"columns\"]: %s" \
                #            % self.rule["columns"])
                for col in self.rule["columns"]:
                    data = select.xpath(\
                            self.rule["columns"][col]["content"]).extract()
                    #logging.info("data: %s" % data)
                    self.worksheet.write(row_index, int(col)-1, data)
                row_index += 1

        self.logging.info("Finish the logic of parse method ... ")
