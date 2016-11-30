# !/usr/bin/bash
#

echo "test start here ..." > ./test.log
cnt=5
while [[ $cnt > 0 ]]
do
    echo $cnt >> ./test.log
    #python ./hehe.py
    python ./run.py
    echo "before sleep ..." >> ./test.log
    sleep 60
    echo "after sleep ..." >> ./test.log
    ((cnt-=1))
done

echo "finish here" >> ./test.log
exit 0

