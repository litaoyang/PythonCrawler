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



class TIMESrankingSpider(CrawlSpider):
    name = "timesranking"

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

    def __del__(self):
        self.logging.info("=============================================================")
        self.logging.info("logging end here ...")
        self.logging.info("=============================================================")
        self.browser.quit()

    def parse(self, response):

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
        logging.info("****SPECIAL INFO: the url which browser get is %s" % response.url)
        # NOW, change the response.url to self.start_urls[0]
        #   get url from start_urls
        #   & click ALL option, then all rows in one page
        #   IN CONFIG:
        #       "next_page": ["XPATH_CLICK", [xpath_to_click]],
        if self.next_page[0] == "XPATH_CLICK":
            self.browser.get(self.start_urls[0])
            self.logging.info("#### CLICK ALL for TIMES ...")
            js="var q=document.documentElement.scrollTop=7190"
            self.browser.execute_script(js)
            time.sleep(3)
            if (self.next_page[1][0]):
                self.browser.find_element_by_xpath(self.next_page[1][0]).click()
            self.browser.find_element_by_xpath(self.next_page[1][1]).click()
        else:
            self.browser.get(response.url)

        self.logging.info("#### got url ...")
        self.logging.info("#### response: %s" % response)


        browser_response = Selector(text = self.browser.page_source)
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

        self.logging.info("Finish the logic of parse method ... ")

