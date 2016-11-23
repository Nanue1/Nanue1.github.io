
title: ES单条数据替换 
date: 2016-10-04 17:49:58
tags: elasticsearch
---
``
    需要从开发环境的es中导出几条数据,替换掉生产环境的数据,几十条这个量还是写个脚本操作
    单条插入数据,构造curl
      ```
      curl -XPUT 'http://10.6.109.100:9200/index/type/ID' -d @data_json
      ```
    问题:通过session.get() 获取数据存入到文件data_json的时候,文件没有关闭,导致读取json的时候读取到的是不完整的json数据
    
<!--more-->

### 代码区

```python

import os
import requests
import json
import sys

server_ip = "10.24.45.94"
def ip2int(ipstr):
	    return reduce(lambda x,y:(x<<8)+y,map(int,ipstr.split('.')))

def main(s,ip):
	ret = s.get("http://%s:9200/%s/_search?pretty&q=ip:%s" % (server_ip, 'ipasset_seer4', ip))
	ip_int=ip2int(ip)
	print ip_int
	j = json.loads(ret.content)
	src=j['hits']['hits']
	fp=open("mapin","w")
	if src:
		source=src[0]["_source"]
		fp.write(json.dumps(source)+'\n')
		fp.close()
		cmd="curl -XPUT 'http://10.6.109.100:9200/ipasset_seer_new/asset_from_seer/%d' -d @mapin "% ip_int
		os.system(cmd)
if __name__ == '__main__':
	sess = requests.Session()
	with open ("ip_2","r") as f:
		for line in f:
			main(sess,line)
#main(sess,"175.138.82.123")
```
