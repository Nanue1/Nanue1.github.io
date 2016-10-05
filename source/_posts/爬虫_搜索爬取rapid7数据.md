title: 爬虫_搜索爬取rapid7数据
date: 2016-10-05 17:49:58
tags: spider
---

rapid7官网提供的exp需要通过搜索获得具体的信息

 ![](http://7xpyfe.com1.z0.glb.clouddn.com/rapid7.png)


请求的URL中居然有对勾,在构造搜索请求的时候,忽略了\& 的转译,导致数据总是查的和浏览器访问的有差别,获取到页面后,bs4 module能够很方便的解析HTML文件
构造的搜素请求:

    ```
    curl -s -L -A "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0" -H "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3" -o ./spider_data/CVE-1999-0003  https://www.rapid7.com/db/search?utf8=%E2%9C%93\&q=CVE-1999-0003\&t=a
    ```
    
    
### 代码区

```python

import os
from bs4 import BeautifulSoup
import sys
import traceback
import os.path as OP
import time
import pdb

ARRS_SPAN_CLASS=['greyTag']

def parser_poc():
    path_bak="./data_bak"
    if not OP.exists(path_bak):
        os.mkdir(path_bak)
    files_list= os.listdir('spider_data')
    for file_name in files_list:
        path= 'spider_data/'+file_name
        soup = BeautifulSoup(open(path,'r'),'html5lib')
        for tag_span in soup.find_all('span'):
            arrs_class = tag_span.get('class')
            if  arrs_class == ARRS_SPAN_CLASS:
                    unicode_str=str(unicode(tag_span.string))
                    if unicode_str=="Exploit": 
 	#	        pdb.set_trace()
    			if  OP.exists(path):
                            cmd0='mv spider_data/%s  data_bak/' % file_name
                            os.system(cmd0)
			    return "ture"
    	if OP.exists(path):
	    cmd1='mv spider_data/%s  data_bak/' % file_name
	    os.system(cmd1)
	    return "false"

def spider_poc(query):
	try:
            query_str = query
            path_month = './spider_data/'
            if not OP.exists(path_month):
                os.mkdir(path_month)
            file_name = path_month + query_str
            #url = ' https://www.rapid7.com/db/search?'+ 'q=%s&t=a'% query_str
            url = ' https://www.rapid7.com/db/search?utf8=%E2%9C%93\&'+ 'q=%s\&t=a'% query_str
	    cmd = ["/usr/bin/curl", "-s", "-L",
                   "-A", '"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0"',
                   "-H", '"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"',
                   "-o", file_name, url ]
            cmdline = ' '.join(cmd)
	    print cmdline
            os.system(cmdline)
        except:
            traceback.print_exc()

def get_poc_from_rapid7(query):
	try:
	    spider_poc(query)
	    time.sleep(6)
	    ret =  parser_poc()
	    return ret		
	except :
	    traceback.print_exc()

```
