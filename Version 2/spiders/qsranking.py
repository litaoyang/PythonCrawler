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



class QSrankingSpider(CrawlSpider):
    name = "QSranking"

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
        self.browser.get(response.url)
        self.logging.info("#### got url ...")
        #time.sleep(30)
        #self.browser.implicitly_wait(10) # seconds
        self.logging.info("#### after wait...")
        self.logging.info("#### response: %s" % response)


        ###########################################
        # keep on click the "show more button",
        # until we get the whole table in broswer.
        ###########################################
        count_click_loops = 0
        while(1):

            try:
                wait = WebDriverWait(self.browser, 20)
                element = \
                     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ranking-wp"]/p/a')))
                count_click_loops += 1
                self.logging.info("######## count_click_loops : %s" %  count_click_loops)
                self.logging.info("######## A new click begin here ...")
            except TimeoutException, e:
                self.logging.info("######## wait error here ...")
                self.logging.info("######## e: ", e)
                self.logging.info("######## we will break the top while here,")
                self.logging.info("######## hope no more to click then...")
                break
            #print "#################after wait ... "

            # a loop to wait for clickable of "show more" button.
            count_fail_click = 0
            while(1):
                try:
                    element.click()
                    self.logging.info("########## gona break, hey ...")
                    self.logging.info("########## count_fail_click: %d" % count_fail_click)
                    break
                except WebDriverException, e:
                    self.logging.info("########## e: %s" % e)
                    self.logging.info("bad luck this time,")
                    self.logging.info("try again later ...")
                    count_fail_click += 1
                    time.sleep(5)

        self.logging.info("#### after click() ...")
        self.logging.info("#### total of count_click_loops: %d" % count_click_loops)
        ###########################################
        # finish this function here.
        ###########################################


        self.logging.info("begin the logic of parse method ... ")


        browser_response = Selector(text = self.browser.page_source)
        logging.info("type(browser_response): %s" % type(browser_response))

        # for the title of the table
        row_index = 0
        for col in self.rule["columns"]:
            data = browser_response.xpath(self.rule["columns"][col]["title"]).extract()
            #print "data: ", data
            self.worksheet.write(row_index, int(col)-1, data)
        row_index += 1

        # for the content of the table
        if self.flag[0] != "NONE": # has special cell to reget in flag
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
                    # for QS and FUDAN:
                    #   reget data for special content
                    if "content_special" in self.flag[1] and data == [] \
                            and col in self.flag[1]["content_special"][0]:
                        data = select.xpath(self.rule["columns"]\
                                [col]["content_for_special"]).extract()
                        #logging.info("data: %s" % data)
                    # for QS only:
                    #   count stars for each star cell
                    if self.flag[0] == "for_QS" \
                            and "count_stars" in self.flag[1] and data != [] \
                            and col in self.flag[1]["count_stars"][0]:
                        #logging.info("star col data: %s" % data)
                        if "plus" in data[-1]:
                            data = [ str(len(data)-1), "+"]
                        else:
                            data = [ str(len(data)), ]
                        #logging.info("star col data: %s" % data)
                    # store data to sheet
                    if self.rule["columns"][col]  
                        data = select.xpath(self.rule["columns"][col]["content1"]).extract()
                            if data == ""
                                data = select.xpath(self.rule["columns"][col]["content2"]).extract()
                                    if data == ""
                                        data = select.xpath(self.rule["columns"][col]["content3"]).extract()
                                        if data == ""
                                            data = select.xpath(self.rule["columns"][col]["content4"]).extract()
                                        else
                                            data = '4'
                                    else
                                        data = '5'
                            else
                                data = '6'    
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

