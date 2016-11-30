# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
import time

import xlwt
import logging



class USNEWSrankingSpider(CrawlSpider):
    name = "usnewsranking"

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
        logging.info("***********************************")
        #yield Request(self.start_urls,headers={'User-Agent':"Windows;U;Windows NT 6.1;en-US;rv;1.9.1.6"})
        logging.info("***********************************")
    def start_request(self):
        logging.info("***********************************")
        yield Request(self.start_urls,headers={'User-Agent':"Windows;U;Windows NT 6.1;en-US;rv;1.9.1.6"})
    def __del__(self):
        self.logging.info("=============================================================")
        self.logging.info("logging end here ...")
        self.logging.info("=============================================================")
        self.browser.quit()

    def parse(self, response):
        logging.info("***********************************")
        # these two vals are for callback args
        #   that we passed in Request(next_page_url)
        write_title = ( response.meta['write_title'] \
                        if ('write_title' in response.meta) else True )
        start_row = ( response.meta['start_row'] \
                        if ('start_row' in response.meta) else 0 )
        crawld_pages = ( response.meta['crawld_pages'] \
                        if ('crawld_pages' in response.meta) else 0 )
        logging.info("write_title: %s" % write_title)
        logging.info("start_row %s" % start_row)
        logging.info("crawld_pages %s" % crawld_pages)

        # using browser to get url again ...
        logging.info("***********************************")
        yield Request(response.url,headers={'User-Agent':""})
        self.browser.get(response.url)
        self.logging.info("#### got url ...")
        self.logging.info("#### response: %s" % response)


        browser_response = Selector(text = self.browser.page_source)
        #browser_response = response
        logging.info("type(browser_response): %s" % type(browser_response))

        # broswer is ready now ...
        self.logging.info("begin the logic of parse method ... ")


        # crawl data of this page
        # start here
        logging.info("start crawling data of this page ...")

        row_index = start_row

        # for the title of the table
        if write_title:
            for col in self.rule["columns"]:
                if self.rule["columns"][col]["title"] != "None":
                    data = browser_response.xpath(self.rule["columns"][col]["title"]).extract()
                    #print "data: ", data
                    self.worksheet.write(row_index, int(col)-1, data)
            row_index += 1

        # for the content of the table
        for select in browser_response.xpath(self.rule["table_tag"]):
            #logging.info("select: %s" % select)
            #logging.info("self.rule[\"columns\"]: %s" % self.rule["columns"])
            for col in self.rule["columns"]:
                data = select.xpath(self.rule["columns"][col]["content"]).extract()
                #logging.info("data: %s" % data)
                self.worksheet.write(row_index, int(col)-1, data)
            row_index += 1

        crawld_pages += 1
        logging.info("finished crawling data of this page ...")

        # next_page need to be crawl ...
        # then do it

        # For USNEWS only:
        #   show start and end page number in url to replace NUM
        #   IN CONFIG:
        #       "next_page": [
        #           "URL_PATTERN",
        #           ["url_pattern", "start_page", "end_page"]
        #       ],
        if self.next_page[0] == "URL_PATTERN":
            if self.next_page[1] and (crawld_pages < int(self.next_page[1][2])):
                # replace NUM in url_pattern with page_number in range
                # AND assume that NUM in url_pattern here
                next_url = self.next_page[1][0].replace(\
                                                "NUM", str(crawld_pages+1))
                request = yield scrapy.Request(next_url, callback=self.parse,headers={'User-Agent':"Windows;U;Windows NT 6.1;en-US;rv;1.9.1.6"})
                request.meta['write_title'] = False
                request.meta['start_row'] = row_index
                request.meta['crawld_pages'] = crawld_pages
                #return request
            else:
                logging.info("No more next_page to crawl ...")
                logging.info("I will quit my parse here ... Thanks ...")

        self.logging.info("Finish the logic of parse method ... ")

