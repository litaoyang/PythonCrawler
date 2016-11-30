#!/usr/bin/python
# -*- coding: UTF-8 -*-
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



class RankingSpider(CrawlSpider):
    name = "ranking"

    def __init__(self, rule, worksheet, logging, report_fp):
        CrawlSpider.__init__(self)
        # use any browser you wish
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
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
        self.report_fp = report_fp
        self.logging.info("Finish the __init__ method ... ")

    def __del__(self):
        self.logging.info("===================================================")
        self.logging.info("logging end here ...")
        self.logging.info("===================================================")
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


        ###########################################
        # using browser to get url again ...


        # For TIMES only:
        #   get url from start_urls
        #   & click ALL option, then all rows in one page
        #   IN CONFIG:
        #       "next_page": ["XPATH_CLICK", [xpath_to_click]],
        if self.next_page[0] == "XPATH_CLICK":
            self.browser.get(self.start_urls[0])
            self.logging.info("#### CLICK ALL for TIMES ...")
            js="var q=document.documentElement.scrollTop=6690"
            if (self.next_page[2][0]):
                js1="var q=document.documentElement.scrollTop=300"
                self.browser.execute_script(js1)
                #time.sleep(3)
                self.browser.find_element_by_xpath(self.next_page[2][0]).click()
                js1="var q=document.documentElement.scrollTop=0"
                self.browser.execute_script(js1)
                #time.sleep(3)
            if (self.next_page[1]) == "1":
                js1="var q=document.documentElement.scrollTop=7800"
                self.browser.execute_script(js1)
                #time.sleep(3)
            if (self.next_page[1]) == "2":
                js1="var q=document.documentElement.scrollTop=7190"
                self.browser.execute_script(js1)
                #time.sleep(3)
            if (self.next_page[1]) == "3":
                js1="var q=document.documentElement.scrollTop=3000"
                self.browser.execute_script(js1)
                #time.sleep(3)    
            if(self.next_page[2][1]):
                self.browser.find_element_by_xpath(self.next_page[2][1]).click()
            self.browser.find_element_by_xpath(self.next_page[2][2]).click()
        else:
            self.browser.get(response.url)

        # after get url by broswer
        # check if it's right, avoid 111
        retry_times = 5
        while(retry_times):
            try:
                content = self.browser.find_element_by_xpath(self.rule["table_tag"])
                self.logging.info("SPECIAL: content in try here, content: %s" \
                                % content)
                self.logging.info("########## break while ...")
                break
            except Exception,e:
                self.logging.info("SPECIAL: in Exception here ...")
                self.logging.info("########## errorhere: %s" % e)
                self.logging.info("########## need refresh page ...")
                self.logging.info("########## response.url %s" % response.url)
                time.sleep(10)
                self.browser.refresh()
                retry_times -= 1

        # still failed to get right data of this page
        if retry_times == 0:
            self.logging.info("****Need retry for url: %s" % response.url)
            self.report_fp.write("in ranking " + self.name + \
                    " -> " + response.url + "\n")

        self.logging.info("#### got url with browser ...")
        #self.browser.close()


        # For QS only
        self.logging.info("#### before click_showmore_QS() ...")
        if self.next_page[0] == "SHOWMORE_CLICK":
            self.click_showmore_QS()
        self.logging.info("#### after click_showmore_QS() ...")


        browser_response = Selector(text = self.browser.page_source)
        logging.info("type(browser_response): %s" % type(browser_response))

        # broswer is ready now ...
        self.logging.info("begin the logic of parse method ... ")


        ###########################################
        # crawl data of this page
        # start here
        logging.info("start crawling data of this page ...")

        row_index = start_row
                    
        # for the title of the table
        if write_title:
            for col in self.rule["columns"]:
                if self.rule["columns"][col]["title"] != "None":
                    data = browser_response.xpath(\
                            self.rule["columns"][col]["title"]).extract()
                    #logging.info("self.rule[\"columns\"]: %s" \
                    #                % self.rule["columns"])
                    #logging.info("data: %s" % data)
                    self.worksheet.write(row_index, int(col)-1, data)
            row_index += 1

        # for the content of the table

        # if the table still empty, that means had after 5 times retry
        # so we add the missing page's url in EXCEL file
        if len(browser_response.xpath(self.rule["table_tag"])) == 0:
            self.logging.info("SPECIAL: select is none here, url: %s" \
                        % response.url)
            data = "This url need reget : " + response.url
            self.worksheet.write(row_index, 0, data)
            row_index += 1
            #self.report_fp.write("This url need reget: " + response.url + "\n")
        # the table unempty status
        if self.flag[0] != "NONE": # has special cell to reget in flag
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
                    self.worksheet.write(row_index, int(col)-1, data)
                row_index += 1
        else: # self.flag[0] is "NONE"
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

        crawld_pages += 1
        logging.info("finished crawling data of this page ...")
        #self.browser.close()
        ###########################################
        ###########################################
        # next_page need to be crawl ...

        # For WO only:
        #   find url by xpath, and loop total_num times
        #   IN CONFIG:
        #       "next_page": [
        #           "XPATH_URL",
        #           ["xpath_url", "total_num"]
        #       ],
        if self.next_page[0] == "XPATH_URL":
            if crawld_pages < int(self.next_page[1][1]):
                href = response.xpath(self.next_page[1][0])
                logging.info("##### href: %s" % href)
                logging.info("##### type(href): %s" % type(href))
                if href:
                    next_url = response.urljoin(href[0].extract())
                    request = scrapy.Request(next_url, callback=self.parse)
                    request.meta['write_title'] = False
                    request.meta['start_row'] = row_index
                    request.meta['crawld_pages'] = crawld_pages
                    return request
                else:
                    logging.info("No more next_page to crawl ...")
                    logging.info("I will quit my parse here ... Thanks ...")
        #self.browser.close()
        # For CUAA & NSEAC:
        #   for each in url_list, go get it.
        #   IN CONFIG:
        #       "next_page": [
        #           "URL_LIST",
        #           ["url_1", "url_2", "url_n", ...]
        #       ],
        if self.next_page[0] == "URL_LIST":
            if len(self.next_page[1]) > crawld_pages-1:
                next_url = self.next_page[1][crawld_pages-1]
                request = scrapy.Request(next_url, callback=self.parse)
                request.meta['write_title'] = False
                request.meta['start_row'] = row_index
                request.meta['crawld_pages'] = crawld_pages
                return request
            else:
                logging.info("No more next_page to crawl ...")
                logging.info("I will quit my parse here ... Thanks ...")
        #self.browser.close()
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
                request = scrapy.Request(next_url, callback=self.parse)
                request.meta['write_title'] = False
                request.meta['start_row'] = row_index
                request.meta['crawld_pages'] = crawld_pages
                return request
            else:
                logging.info("No more next_page to crawl ...")
                logging.info("I will quit my parse here ... Thanks ...")

        self.logging.info("Finish the logic of parse method ... ")
        

    def click_showmore_QS(self):
        ###########################################
        # keep on click the "show more button",
        # until we get the whole table in broswer.
        ###########################################
        count_click_loops = 0
        count1 = 0
        i = 4000
        while(count1<8):
            try:
                if count1 == 0:
                    js1="var q=document.documentElement.scrollTop = 4000"
                    self.browser.execute_script(js1)
                    time.sleep(3)
                if count1 == 1:
                    js1="var q=document.documentElement.scrollTop = 7500"
                    self.browser.execute_script(js1)
                    time.sleep(3)
                if count1 == 2:
                    js1="var q=document.documentElement.scrollTop = 11000"
                    self.browser.execute_script(js1)
                    time.sleep(3)
                if count1 == 3:
                    js1="var q=document.documentElement.scrollTop = 14500"
                    self.browser.execute_script(js1)
                    time.sleep(3)
                if count1 == 4:
                    js1="var q=document.documentElement.scrollTop = 18000"
                    self.browser.execute_script(js1)
                    time.sleep(3)
                if count1 == 5:
                    js1="var q=document.documentElement.scrollTop = 21500"
                    self.browser.execute_script(js1)
                    time.sleep(3)
                if count1 == 6:
                    js1="var q=document.documentElement.scrollTop = 25000"
                    self.browser.execute_script(js1)
                    time.sleep(3)
                if count1 == 7:
                    js1="var q=document.documentElement.scrollTop = 28500"
                    self.browser.execute_script(js1)
                    time.sleep(3)    
                wait = WebDriverWait(self.browser, 20)
                element = wait.until(EC.element_to_be_clickable(( \
                            By.XPATH, '//*[@id="ranking-wp"]/p/a')))
                count_click_loops += 1
                count1+=1
                self.logging.info("count_click_loops : %s" %  count_click_loops)
                self.logging.info("A new click begin here ...")
            except TimeoutException, e:
                self.logging.info("wait error here ...")
                self.logging.info("e: ", e)
                self.logging.info("we will break the top while here,")
                self.logging.info("hope no more to click then...")
                break
            logging.info("############# after wait ... ")

            # a loop to wait for clickable of "show more" button.
            count_fail_click = 0
            while(1):
                try:
                    element.click()
                    self.logging.info("########## gona break, hey ...")
                    self.logging.info("########## count_fail_click: %d" \
                                        % count_fail_click)
                    break
                except WebDriverException, e:
                    self.logging.info("########## e: %s" % e)
                    self.logging.info("bad luck this time,")
                    self.logging.info("try again later ...")
                    count_fail_click += 1
                    time.sleep(1)

        self.logging.info("after click() ...")
        self.logging.info("total of count_click_loops: %d" % count_click_loops)
        ###########################################
        # finish CLICKing showmore button function here.
        ###########################################

