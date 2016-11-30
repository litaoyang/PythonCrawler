from spiders.shanghairanking import ShanghairankingSpider
from spiders.qsranking import QSrankingSpider
from spiders.webometricsranking import WOrankingSpider
from spiders.cuaaranking import CUAArankingSpider
from spiders.usnewsranking import USNEWSrankingSpider
from spiders.timesranking import TIMESrankingSpider
from spiders.rankingspider import RankingSpider

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import json
import xlwt
import time
import logging

ISOTIMEFORMAT='%Y%m%d%H%M%S'

report_filename = "./report/report.txt"
report_fp = open(report_filename, "a+")
report_fp.write("These are urls that had tryed five times in process but still need reget:\n")

log_filename = "./log/rankingspider.log"

logging.basicConfig(level=logging.INFO, filename=log_filename)
logging.info("=============================================================")
logging.info("logging begin here ...")
logging.info("=============================================================")

json_file_shanghai = file("./config/config_shanghairanking_v2.json")
json_file_qs = file("./config/config_qs_v2.json")
json_file_webometrics = file("./config/config_webometrics_v2.json")
json_file_cuaa_2015 = file("./config/config_cuaa_2015_v2.json")
json_file_cuaa_2016 = file("./config/config_cuaa_2016_v2.json")
json_file_nseac_2015 = file("./config/config_nseac_2015_v2.json")
json_file_nseac_2016 = file("./config/config_nseac_2016_v2.json")
json_file_usnews = file("./config/config_usnews_v2.json")
json_file_times = file("./config/config_times_v2.json")
json_file_fudanmed = file("./config/config_fudanmed_v2.json")

config_rules_shanghai = json.load(json_file_shanghai)
config_rules_qs = json.load(json_file_qs)
config_rules_webometrics = json.load(json_file_webometrics)
config_rules_cuaa_2015 = json.load(json_file_cuaa_2015)
config_rules_cuaa_2016 = json.load(json_file_cuaa_2016)
config_rules_nseac_2015 = json.load(json_file_nseac_2015)
config_rules_nseac_2016 = json.load(json_file_nseac_2016)
config_rules_usnews = json.load(json_file_usnews)
config_rules_times = json.load(json_file_times)
config_rules_fudanmed = json.load(json_file_fudanmed)

json_file_shanghai.close()
json_file_qs.close()
json_file_webometrics.close()
json_file_cuaa_2015.close()
json_file_cuaa_2016.close()
json_file_nseac_2015.close()
json_file_nseac_2016.close()
json_file_usnews.close()
json_file_times.close()
json_file_fudanmed.close()

config_rules_all = {}
#config_rules_all[ config_rules_times["XLS_FILENAME"] ] = config_rules_times
#config_rules_all[ config_rules_usnews["XLS_FILENAME"] ] = config_rules_usnews
#config_rules_all[ config_rules_cuaa_2015["XLS_FILENAME"] ] = config_rules_cuaa_2015
#config_rules_all[ config_rules_cuaa_2016["XLS_FILENAME"] ] = config_rules_cuaa_2016
config_rules_all[ config_rules_nseac_2015["XLS_FILENAME"] ] = config_rules_nseac_2015
#config_rules_all[ config_rules_nseac_2016["XLS_FILENAME"] ] = config_rules_nseac_2016
config_rules_all[ config_rules_webometrics["XLS_FILENAME"] ] = config_rules_webometrics
#config_rules_all[ config_rules_qs["XLS_FILENAME"] ] = config_rules_qs
#config_rules_all[ config_rules_fudanmed["XLS_FILENAME"] ] = config_rules_fudanmed
#config_rules_all[ config_rules_shanghai["XLS_FILENAME"] ] = config_rules_shanghai

# storing workbooks for all website
WorkBooks = {}

# setting for this process
settings = Settings()
settings.set('DOWNLOAD_DELAY', 3)
settings.set('RETRY_TIMES', 5)
logging.info("Settings['DOWNLOAD_DELAY']: %s" % settings['DOWNLOAD_DELAY'])
logging.info("Settings['RETRY_TIMES']: %s" % settings['RETRY_TIMES'])


process = CrawlerProcess(settings)

logging.info("process: %s " % process)


for website_name in config_rules_all:
    # open Workbook for each website
    WorkBooks[website_name] = xlwt.Workbook(encoding='utf-8', style_compression=0)
    logging.info("WorkBooks: %s" % WorkBooks)
    for ranking_name in config_rules_all[website_name]:
        if ranking_name != "XLS_FILENAME":
            logging.info("ranking_name: %s", ranking_name)
            worksheet = WorkBooks[website_name].add_sheet(ranking_name)
            process.crawl( RankingSpider,\
                            config_rules_all[website_name][ranking_name],\
                            worksheet, logging, report_fp )

logging.info("process.start() here ...")
process.start() # the script will block here until the crawling is finished


# save workboot
logging.info("before save workbook ...")
#workbook.save("ShanghaiRanking.xls")
for workbook in WorkBooks:
    xls_filename = "./excels/" + workbook + "ranking.xls"
    WorkBooks[workbook].save(xls_filename)
    logging.info("WorkBooks saving in %s" % xls_filename)
logging.info("after save workbook ...")
logging.info("Logging messages saving in %s" % log_filename)

# closing report file
report_fp.write("Report stop here ...\n")
report_fp.close()
logging.info("Process running report in %s" % report_filename)
