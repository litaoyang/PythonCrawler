# GraduationProject_PythonCrawler
#This is my Graduation Project.
#A configurable spider about serveral university ranking lists.

#################################################
Files Locaiton:
    INPUT Part:
        ./webspider/webspider/config/:
                config files using in run.py and run_for_each.py.
    LOGICAL Part:
        ./webspider/webspider/spiders/:
                spiders invoked by run.py and run_for_each.py.
        ./webspider/webspider/run.py
                run this file and will get the final results,
                change the comment line in it can control the websites which will be crawled.
        ./webspider/webspider/run_for_each.py
                run this file and will get part of the results,
                change the comment line in it can control the websites which will be crawled.
    OUTPUT Part:
        ./webspider/webspider/excels/:
                xls fiels that will be generated finally.
        ./webspider/webspider/excels/:
                log files for this running time.


#################################################
How to run this project?

cd ./webspider/webspider/
python ./run.py

then xls files will generate in ./webspider/webspider/excels/



#################################################
ANY QUSTIONS ?
CONTACT ME by xxwjoy@hotmail.com
