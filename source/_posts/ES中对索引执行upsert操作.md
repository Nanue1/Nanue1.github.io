
title: ES中对索引执行upsert操作 
date: 2016-10-04 18:49:58
tags: elasticsearch 
---
``
elasticsearch 中 [bulk-update](https://www.elastic.co/guide/en/elasticsearch/reference/2.4/docs-bulk.html#bulk-update)操作,官方文档有详细介绍,在这里只需要构造一下类型的json bulk提交即可,其中两个字典之间需要'\n'连接
```json
{
    "update":{"_index":"threat_ip3","_type":"ipv4","_id":"1756060854","_retry_on_conflict":3}

}
{
    "script": {"inline": "ctx._source.activity += act;ctx._source.updated = up", "params": {"up": "2016-10-05T13:41:05", "act": [{"update_time": "2016-09-24T18:15:01", "from": "nta", "threat": "DDos", "level": "3"}]}},

    "upsert": {"province": "Pennsylvania", "city": "Bala Cynwyd", "updated": "2016-10-05T13:41:05", "ip": "104.171.92.182", "activity": [{"update_time": "2016-09-24T18:15:01", "from": "nta", "threat": "DDos", "level": "3"}], "location": "40.013821,-75.228661", "country_code": "US", "country": "United States"}
}
```
<!--more-->

### 代码区

```python
#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import sys
import pycurl
import logging
import StringIO
import urllib
import time
import json
import urllib2
import datetime
import os
import traceback
import requests
action = """{"update":{"_index":"%s","_type":"%s","_id":"%d","_retry_on_conflict":3}}\n"""
threat_type=["Unknown","DDos","Exploits","Spam Sources","Web Attacks","Scanners","Botnets","malware","phishing","proxy","suspicious","TECHCGI","OVERFLOW","FORCE","RESDEPLETE","ODD","TROJAN","SCAN","LAN","TECHMISC","EVTMON","IMP2P","VIRUS"]

actions = []
SERVER_IP = '10.24.45.95'
ES_URL = "http://%s:9200/_bulk"%SERVER_IP
PATH_DIR= "/home/lixuchun/ip_history/data_bak"

num_bulk_submit = 1000
num_submit = 0

def ip2int(ipstr):
    return reduce(lambda x,y:(x<<8)+y,map(int,ipstr.split('.')))

def init_log(log_xpath):
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y %b %d %H:%M:%S',
                filename=log_xpath,
                filemode='a')

def trans_line_time(line):
	final_line = {"activity":[]}
	tmp_dic={}
	line_split = line.split('\t')
	final_line["ip"] = line_split[0]
	last_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%S")
	final_line.update({"updated":last_time})

	ip_info = json.loads(line_split[5])
	final_line["country"]=ip_info["country_name"]
	final_line["country_code"]=ip_info["country_code"]
	final_line["province"]=ip_info["province_name"]
	final_line["city"]=ip_info["city_name"]
	final_line["location"]=ip_info["raw_location"]

	date_time = datetime.datetime.utcfromtimestamp(int(line_split[1])).strftime("%Y-%m-%dT%H:%M:%S") 
	tmp_dic["update_time"]=date_time   
	tmp_dic["level"]= line_split[2].strip()
	tmp_dic["threat"]=threat_type[int(line_split[3].strip())]
	tmp_dic["from"]=line_split[4].strip() 
    #final_line["activity"]=tmp_dic
	final_line.update({"activity":[tmp_dic]})
	return final_line

def main(data_xpath,log_xpath):
    session = requests.Session()
    init_log(log_xpath)
    put_count = 0
    line_count = 0
    num_submit = 0
    data_count = 0
    num = 0
    newline={}
    with open(data_xpath, "r") as f:
        for line in f:
                num = num +1 
                print num 
                line_count += 1
                try:
                    newline = trans_line_time(line)
                except:
                    traceback.print_exc()
                ip =newline["ip"].strip()
                ip_int= ip2int(str(ip))
                data_count += 1
                actions.append(action % ("threat_ip3", "ipv4",ip_int))
            	out_sec = {"script":{"inline":"ctx._source.activity += act;ctx._source.updated = up","params":{"act":newline['activity'],"up":newline['updated']}},"upsert":newline}
                actions.append(json.dumps(out_sec) + '\n')
                num_submit += 1
                if num_submit == num_bulk_submit:
                    source = "".join(actions)
                    session.post(ES_URL, data=source)
                    logging.debug("data_count=%d put_count:%d importing ES" % (data_count,put_count))
                    put_count += 1
                    num_submit = 0
                    del actions[:]
        
        if 0 < num_submit < num_bulk_submit:
            source = "".join(actions)
#         print source
            try:
                session.post(ES_URL, data=source)
            except Exception,e:
                print e
            logging.debug("data_count=%d put_count:%d start importing ES" % (data_count,put_count))
            num_submit = 0
            del actions[:]

    logging.debug("OVER !!!  data_count=%d put_count:%d end importing ES!! " % (data_count,put_count))
  
if '__main__'==__name__:
    print "start"
    date_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    os.chdir(PATH_DIR)
    path_file = '%s' %date_str
    if not os.path.exists(path_file):
        print path_file , 'not exist!!!'
        sys.exit(1)
    print date_str
    log_xpath = "ip_upsert.log"
    main(str(path_file),str(log_xpath))

```
