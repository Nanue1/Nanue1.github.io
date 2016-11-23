
title: Mongodb中实现Upsert操作
date: 2016-10-04 19:49:58
tags: mongodb 
---
需要将一个相当大的文件内数据导入到Mongodb中,单线程导入会非常慢,这里采用将大文件切割成小文件,然后用多进程来操作这些小文件.在每条数据upsert更新操作的时候,也需要检查,更新的数据,在原本的list中是否存在,如果存在则不更新数据.

Mongodb upsert 命令构造:
update({查询条件},{$push,$set语句},upsert=True)
```
coll.update({"ip":ret_dict["ip"]},{"$push":{"history":ret_dict["activity"]},"$set":{"updated":ret_dict["updated"]}},upsert=True)
```
<!--more-->
### 代码区

```python 
#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import sys
import logging
import time
import json
import datetime
import os
import traceback
from pymongo import UpdateOne
import pymongo
import pdb
from multiprocessing import Process

PATH_DIR="/home/lixuchun/ip_history/data/"
num_bulk_submit=50
conn=pymongo.MongoClient('10.24.84.55',27017)
db=conn["threat_ip"]
coll=db["reputation"]
def get_file_lines(thefilepath):
	count = 0
	thefile = open(thefilepath, 'rb')
	while True:
		buffer = thefile.read(8192*1024)
		if not buffer:
			break
		count += buffer.count('\n')
		thefile.close()
		return count

def init_log(log_xpath):
	logging.basicConfig(level=logging.DEBUG,
				format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
				datefmt='%Y %b %d %H:%M:%S',
				filename=log_xpath,
				filemode='a')

def check_dict(line):
	ip=line.split('\t')[0]
	update_int=int(line.split('\t')[1])

	ret_d=coll.find({"ip":ip})
	if ret_d:
		for doc in ret_d:
			for dict_one in doc["history"]:
				update = int(time.mktime(datetime.datetime.strptime(dict_one["update_time"],"%Y-%m-%dT%H:%M:%S").timetuple()))
				if update_int==update:
					return False
		return True 

def trans_line_time(line):
	final_line = {}
	tmp_dic={}
	line_split = line.split('\t')
	final_line["ip"] = line_split[0]
	last_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%S")
	final_line.update({"updated":last_time})
	date_time = datetime.datetime.fromtimestamp(int(line_split[1])).strftime("%Y-%m-%dT%H:%M:%S") 
	tmp_dic["update_time"]=date_time   
	tmp_dic["reputation"]= line_split[2].strip()
	final_line.update({"activity":tmp_dic})
	return final_line

def import2mongo(data_xpath):
	with open(data_xpath,"r") as f:
		for line in f:
			try:
				ret_t =check_dict(line)
				if ret_t:
					ret_dict=trans_line_time(line)
					print ret_dict
					coll.update({"ip":ret_dict["ip"]},{"$push":{"history":ret_dict["activity"]},"$set":{"updated":ret_dict["updated"]}},upsert=True)
			except:
				traceback.print_exc()
def main(file_path,step=50):

	os.chdir("/home/lixuchun/ip_history/")
	if not os.path.exists("log"):
		os.mkdir("log")
	tmp_log="log/mutil_reputation.log"
	init_log(tmp_log)
	count = get_file_lines(file_path)
	splitfile_lines = count/step + 1
	if splitfile_lines < 1:
		splitfile_lines = 1

	if not os.path.exists("split_file"):
		os.mkdir("split_file")

	os.system("split -%d %s split_file/url."%(splitfile_lines, file_path))
	
	filenames = os.listdir("split_file")
	filenames.sort()
	file_nums = len(filenames)
	logging.info("num=%d, fs=%s", file_nums, filenames)
		
	start = 0
	end = step
	if end > file_nums:
		end = file_nums
	while start < end <= file_nums:
		logging.info("start=%d end=%d", start, end)
		ps = [Process(target=import2mongo, args=(start+i, filename)) for i, filename in enumerate(filenames[start:end])]
		for p in ps:
			p.start()
		logging.debug("### wait ps return ###")
		for p in ps:
			p.join()
			logging.debug("### one ps end ###")
		start = end
		end += step
		if end > file_nums:
			end = file_nums

if __name__ in '__main__':
	date_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
	os.chdir(PATH_DIR)
#	path_file = '%s' %date_str
	path_file = '/home/lixuchun/ip_history/data/2016-09-20'
	if not os.path.exists(path_file):
		print path_file , 'not exist!!!'
		sys.exit(1)
	main(str(path_file))

```
