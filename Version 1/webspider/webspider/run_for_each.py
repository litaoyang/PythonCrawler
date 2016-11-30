from spiders.shanghairanking import ShanghairankingSpider
from spiders.fudanranking import FudanmedSpider
from spiders.qsranking import QSrankingSpider
from spiders.webometricsranking import WOrankingSpider
from spiders.cuaaranking import CUAArankingSpider
from spiders.usnewsranking import USNEWSrankingSpider
from spiders.timesranking import TIMESrankingSpider

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import json
import xlwt
import time
import logging

ISOTIMEFORMAT='%Y%m%d%H%M%S'


#xls_filename = "./excels/SHANGHAIRanking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/shanghairanking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_shanghai = file("./config/config_shanghairanking_v2.json")
#config_rules_shanghai = json.load(json_file_shanghai)
#json_file_shanghai.close()

xls_filename = "./excels/FUDANMEDRanking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
log_filename = "./log/fudanmedranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
json_file_fudan = file("./config/config_fudanmed_v2.json")
config_rules_fudan = json.load(json_file_fudan)
json_file_fudan.close()

#xls_filename = "./excels/QSRanking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/qsranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_qs = file("./config/config_qs_v2.json")
#config_rules_qs = json.load(json_file_qs)
#json_file_qs.close()

#xls_filename = "./excels/WORanking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/woranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_webometrics = file("./config/config_webometrics_v2.json")
#config_rules_webometrics = json.load(json_file_webometrics)
#json_file_webometrics.close()

#xls_filename = "./excels/CUAA2015Ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/cuaac2015ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_cuaa_2015 = file("./config/config_cuaa_2015_v2.json")
#config_rules_cuaa_2015 = json.load(json_file_cuaa_2015)
#json_file_cuaa_2015.close()

#xls_filename = "./excels/CUAA2016Ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/cuaac2016ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_cuaa_2016 = file("./config/config_cuaa_2016_v2.json")
#config_rules_cuaa_2016 = json.load(json_file_cuaa_2016)
#json_file_cuaa_2016.close()

#xls_filename = "./excels/NSEAC2015Ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/nseac2015ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_nseac_2015 = file("./config/config_nseac_2015_v2.json")
#config_rules_nseac_2015 = json.load(json_file_nseac_2015)
#json_file_nseac_2015.close()

#xls_filename = "./excels/NSEAC2016Ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/nseac2016ranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_nseac_2016 = file("./config/config_nseac_2016_v2.json")
#config_rules_nseac_2016 = json.load(json_file_nseac_2016)
#json_file_nseac_2016.close()

#xls_filename = "./excels/USNEWSRanking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/usnewsranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_usnews = file("./config/config_usnews_v2.json")
#config_rules_usnews = json.load(json_file_usnews)
#json_file_usnews.close()

#xls_filename = "./excels/TIMESRanking_" + str(time.strftime(ISOTIMEFORMAT)) + ".xls"
#log_filename = "./log/timesranking_" + str(time.strftime(ISOTIMEFORMAT)) + ".log"
#json_file_times = file("./config/config_times_v2.json")
#config_rules_times = json.load(json_file_times)
#json_file_times.close()



logging.basicConfig(level=logging.INFO, filename=log_filename)
logging.info("=============================================================")
logging.info("logging begin here ...")
logging.info("=============================================================")




# open Workbook
workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)

settings = Settings()

process = CrawlerProcess(settings)

logging.info("process: %s " % process)

#for ranking_name in config_rules_nseac:
#for ranking_name in config_rules_times:
#for ranking_name in config_rules_usnews:
#for ranking_name in config_rules_cuaa_2015:
#for ranking_name in config_rules_cuaa_2016:
#for ranking_name in config_rules_nseac_2015:
#for ranking_name in config_rules_nseac_2016:
#for ranking_name in config_rules_webometrics:
#for ranking_name in config_rules_qs:
#for ranking_name in config_rules_shanghai:
for ranking_name in config_rules_fudan:
    if ranking_name != "XLS_FILENAME":
        logging.info("ranking_name: %s " % ranking_name)
        worksheet = workbook.add_sheet(ranking_name)
        process.crawl(FudanmedSpider, \
                config_rules_fudan[ranking_name], worksheet, logging)
        #process.crawl(ShanghairankingSpider, \
        #        config_rules_shanghai[ranking_name], worksheet, logging)
        #process.crawl(QSrankingSpider, \
        #        config_rules_qs[ranking_name], worksheet, logging)
        #process.crawl(WOrankingSpider, \
        #        config_rules_webometrics[ranking_name], worksheet, logging)

        # cuaa & nseac should share the same spider named CUAArankingSpider
        #process.crawl(CUAArankingSpider, \
        #        config_rules_cuaa_2015[ranking_name], worksheet, logging)
        #process.crawl(CUAArankingSpider, \
        #        config_rules_cuaa_2016[ranking_name], worksheet, logging)
        #process.crawl(CUAArankingSpider, config_rules_nseac_2015[ranking_name],
        #        worksheet, logging)
        #process.crawl(CUAArankingSpider, config_rules_nseac_2016[ranking_name],
        #        worksheet, logging)

        #process.crawl(USNEWSrankingSpider, config_rules_usnews[ranking_name], worksheet, logging)
        #process.crawl(TIMESrankingSpider, config_rules_times[ranking_name], worksheet, logging)

logging.info("process.start() here ...")
process.start() # the script will block here until the crawling is finished


# save workboot
logging.info("before save workbook ...")
workbook.save(xls_filename)
logging.info("after save workbook ...")
