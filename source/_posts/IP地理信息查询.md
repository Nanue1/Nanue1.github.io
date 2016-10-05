title: IP 地理信息查询接口
date: 2016-09-10 17:49:58
tags: api_tools
---

   在采用 IP2Location 离线库查询 IP 地理信息的时候,发现中国国内的 IP 信息很多都是空缺的
国内的 IPIP 数据需要花钱购买,这里把每次从 IPIP 查询到的信息保留到 Mongodb 中,方便下次从本
地查询
    IPIP 查询到的信息全是中文的地理信息,使用 pypinyin 这个开源的库将中国大陆地名转为拼音,
效果还不错,对于国外的国家名,收集整理了一个 excel,python 中用 pandas 可以很方便的将 excel
转为 dict

```python
   import pandas as pd
   import json
   my_dic = pd.read_excel('e_c.xlsx', index_col=0).to_dict()
   with open ("dict.txt","w") as fp:
       fp.write(json.dumps(my_dic))
```
  在将一个这么大的字典一行写入文件内的时候,vim 居然卡住了,只能将这么大的 dict 按格式排列了.
  ![](http://7xpyfe.com1.z0.glb.clouddn.com/ipip_info.png)
  <!--more-->
  IP地理信息查询接口代码:
```python
#!/usr/bin/python
# coding: utf-8
import os
import sys
import urllib2
import traceback
import socket
import IP2Location
import json
import os.path as OP
from pypinyin import pinyin, lazy_pinyin
import pdb
import pymongo
IP_LIB = "/tmp/IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE.BIN"
EN2CN_DICT={
"不丹":"Bhutan",
"东萨摩亚":"Samoa,Eastern",
"中华人民共和国":"P.R.C.",
"中国":"China",
"中途岛":"Midway I.",
"中非":"Central Africa",
"丹麦":"Denmark",
"乌克兰":"Ukraine",
"乌兹别克斯坦":"Uzbekistan",
"乌干达":"Uganda",
"乌拉圭":"Uruguay",
"乍得":"Chad",
"也门":"Yemen",
"亚美尼亚":"Armenia",
"以色列":"Israel",
"伊拉克":"Iraq",
"伊郎":"Iran",
"伯利兹":"Belize",
"佛得角":"Cape Verde",
"俄罗斯":"Russia",
"保加利亚":"Bulgaria",
"克罗地亚":"Croatian",
"关岛":"Guam",
"冈比亚":"Gambia",
"冰岛":"Iceland",
"几内亚":"Guinea",
"几内亚比绍":"Guinea-bissau",
"列支敦士登":"Liechtenstein",
"刚果":"Congo",
"利比亚":"Libya",
"利比里亚":"Liberia",
"加拿大":"Canada",
"加纳":"Ghana",
"加蓬":"Gabon",
"加那利群岛":"Canaries Is.",
"匈牙利":"HunGary",
"南斯拉夫":"Yugoslavia",
"南非":"South Africa",
"博茨瓦纳":"Botswana",
"卡塔尔":"Qatar",
"卢旺达":"Rwanda",
"卢森堡":"Luxembourg",
"印度":"India",
"印度尼西亚":"Indonesia",
"危地马拉":"Guatemala",
"厄瓜多尔":"Ecuador",
"厄立特里亚":"Eritrea",
"叙利亚":"Syria",
"古巴":"Cuba",
"吉尔吉斯斯坦":"Kyrgyzstan",
"吉布提":"Djibouti",
"哈萨克斯坦":"Kazakhstan",
"哥伦比亚":"Colombia",
"哥斯达黎加":"Costa Rica",
"喀麦隆":"Cameroon",
"图瓦卢":"Tuvalu",
"土库曼斯坦":"Turkmenistan",
"土耳其":"Turkey",
"圣克里斯托弗和尼维斯":"St.Christopher and Nevis",
"圣卢西亚":"St.Lucia",
"圣多美和普林西比":"San.Tome And Principe",
"圣文森特岛":"St.Vincent I.",
"圣皮埃尔岛及密克隆岛":"San.Pierre And Miquelon I.",
"圣诞岛":"Christmas I.",
"圣赫勒拿":"St.Helena",
"圣马力诺":"San.Marino",
"圭亚那":"Guyana",
"坦桑尼亚":"Tanzania",
"埃及":"Egypt",
"埃塞俄比亚":"Ethiopia",
"基里巴斯":"Kiribati",
"塔吉克斯坦":"Tajikistan",
"塞内加尔":"Senegal",
"塞浦路斯":"Cyprus",
"塞舌尔":"Seychelles",
"墨西哥":"Mexico",
"夏威夷":"Hawaii",
"多哥":"Togo",
"多米尼克国":"Commonwealth of dominica",
"多米尼加共和国":"Dominican Rep.",
"奥地利":"Austria",
"委内瑞拉":"Venezuela",
"威克岛":"Wake I.",
"孟加拉国":"Bangladesh",
"安哥拉":"Angola",
"安圭拉岛":"Anguilla I.",
"安提瓜和巴布达":"Antigua and Barbuda",
"安道尔":"Andorra",
"密克罗尼西亚":"Micronesia",
"尼加拉瓜":"Nicaragua",
"尼日利亚":"Nigeria",
"尼日尔":"Niger",
"尼泊尔":"Nepal",
"巴哈马国":"Commonwealth of The Bahamas",
"巴基斯坦":"Pskistan",
"巴巴多斯":"Barbados",
"巴布亚新几内亚":"Papua New Guinea",
"巴拉圭":"Paraguay",
"巴拿马":"Panama",
"巴林":"Bahrain",
"巴西":"Brazil",
"布基纳法索":"Burkinafaso",
"布隆迪":"Burundi",
"希腊":"Greece",
"帕劳":"Palau",
"开曼群岛":"Cayman Is.",
"德国":"Germany",
"意大利":"Italy",
"所罗门群岛":"Solomon Is.",
"扎伊尔":"Zaire",
"托克劳群岛":"Tokelau Is.",
"拉脱维亚":"Latvia",
"挪威":"Norway",
"捷克":"Czech",
"摩尔多瓦":"Moldova",
"摩洛哥":"Morocco",
"摩纳哥":"Monaco",
"斐济":"Fiji",
"斯威士兰":"Swaziland",
"斯洛伐克":"Slovak",
"斯洛文尼亚":"Slovenia",
"斯里兰卡":"Sri Lanka",
"新加坡":"Singapore",
"新喀里多尼亚群岛":"New Caledonia Is.",
"新西兰":"New Zealand",
"日本":"Japan",
"智利":"Chile",
"朝鲜":"Korea(dpr of)",
"柬埔塞":"Kampuchea",
"格林纳达":"Grenada",
"格陵兰岛":"Greenland",
"格鲁吉亚":"Georgia",
"桑给巴尔":"Zanzibar",
"梵蒂冈":"Vatican",
"比利时":"Belgium",
"毛里塔尼亚":"Mauritania",
"毛里求斯":"Mauritius",
"汤加":"Tonga",
"沙特阿拉伯":"Saudi Arabia",
"法国":"France",
"法属圭亚那":"French Guiana",
"法属波里尼西亚":"French Polynesia",
"法罗群岛":"Faroe Is.",
"波兰":"Poland",
"波多黎各":"Puerto Rico",
"波斯尼亚和黑塞哥维那":"Bosnia And Herzegovina",
"泰国":"Thailand",
"津巴布韦":"Zimbabwe",
"洪都拉斯":"Honduras",
"海地":"Haiti",
"澳大利亚":"Australia",
"爱尔兰":"Ireland",
"爱沙尼亚":"Estonia",
"牙买加":"Jamaica",
"特克斯和凯科斯群岛":"Turks and Caicos Is.",
"特立尼达和多巴哥":"Trinidad and Tobago",
"玻利维亚":"Bolivia",
"瑙鲁":"Nauru",
"瑞典":"Sweden",
"瑞士":"Switzerland",
"瓜德罗普岛":"Guadeloupe I.",
"瓦努阿图":"Vanuatu",
"瓦里斯和富士那群岛":"Wallis And Futuna Is.",
"留尼汪岛":"Reunion I.",
"白俄罗斯":"Belarus",
"百慕大群岛":"Bermuda Is.",
"直布罗陀":"Gibraltar",
"福克兰群岛":"Falkland Is.",
"科克群岛":"Cook IS.",
"科威特":"Kuwait",
"科摩罗":"Comoro",
"科特迪瓦":"Ivory Coast",
"科科斯岛":"Cocos I.",
"秘鲁":"Peru",
"突尼斯":"Tunisia",
"立陶宛":"Lithuania",
"索马里":"Somali",
"约旦":"Jordan",
"纳米比亚":"Namibia",
"纽埃岛":"Niue I.",
"维尔京群岛":"Virgin Is.",
"维尔京群岛和圣罗克伊":"Virgin Is. and St.Croix I.",
"缅甸":"Myanmar",
"罗马尼亚":"Rumania",
"美国":"U.S.A",
"老挝":"Laos",
"肯尼亚":"Kenya",
"芬兰":"Finland",
"苏丹":"Sudan",
"苏里南":"Suriname",
"英国":"United Kingdom",
"荷兰":"Netherlands",
"荷属安的列斯群岛":"Netherlandsantilles Is.",
"莫桑比克":"Mozambique",
"莱索托":"Lesotho",
"菲律宾":"Philippines",
"萨尔瓦多":"El Salvador",
"葡萄牙":"Portugal",
"蒙古":"Mongolia",
"蒙特塞拉特岛":"Montserrat I.",
"西撒哈拉":"Western sahara",
"西班牙":"Spain",
"西萨摩亚":"Samoa,Western",
"诺福克岛":"Norfolk I,",
"贝宁":"Benin",
"赞比亚":"Zambia",
"赤道几内亚":"Equatorial Guinea",
"越南":"Vietnam",
"迪戈加西亚岛":"Diego Garcia I.",
"阿塞拜疆":"Azerbaijan",
"阿富汗":"Afghanistan",
"阿尔及利亚":"Algeria",
"阿尔巴尼亚":"Albania",
"阿拉伯联合酋长国":"The United Arab Emirates",
"阿拉斯加":"Alaska(U.S.A)",
"阿曼":"Oman",
"阿根廷":"Argentina",
"阿森松":"Ascension",
"阿鲁巴岛":"Aruba I.",
"韩国":"Korea",
"马其顿":"Macedonia",
"马尔代夫":"Maldive",
"马拉维":"Malawi",
"马提尼克":"Martinique",
"马来西亚":"Malaysia",
"马约特岛":"Mayotte I.",
"马绍尔群岛":"Marshall Is.",
"马耳他":"Malta",
"马达加斯加":"Madagascar",
"马里":"Mali",
"马里亚纳群岛":"Mariana Is.",
"黎巴嫩":"Lebanon"
}

client = pymongo.MongoClient('10.24.84.55', 27017)
db = client["ipinfo_data"]
tables = db["ipip"]
reload(sys)
sys.setdefaultencoding('utf-8') 

def query_local(ipstr):
	ret=tables.find_one({"ip":ipstr})
	return ret
def save_local(ip,res):
		res.update({"ip":ip})
		tables.insert(res)
		print "save mongo %s" %ip

#def is_chinese(uchar):
#	if uchar >= u'/u4e00' and uchar<=u'/u9fa5':
#		return True
#	else:
#		return False

def cn2pinyin(uchar):
	if uchar in EN2CN_DICT.keys():
		return EN2CN_DICT[uchar.encode()]
	else :
		pinyin_list = lazy_pinyin(uchar)
		list_tmp=[]
		for x in xrange(len(pinyin_list)):
			list_tmp.append(pinyin_list[x])
		pinyin_str = ''.join(list_tmp)
		if pinyin_str == "zhongguo":
			return "China"
		else:
			return pinyin_str.capitalize()
	
def ip2Location(ipstr):	
	ipdb=IP2Location.IP2Location()
	ipdb.open(IP_LIB)
	try:
		socket.inet_aton(ipstr)
	except:
		print ipstr + "FORMAT ERROR!"
	else:	
		return ipdb.get_all(ipstr)

def ipip_info(ipstr):
	try:
		res = query_local(ipstr)
		if res:
			print "search local %s" %ipstr
			return res 
		else:
			request = urllib2.Request(
			   "http://ipapi.ipip.net/find?addr="+ipstr,
			   None,
			   {'Token':'a20dce839e2b3caeabf45b823074dd403ea53bd0'}
			)
			response = urllib2.urlopen(request,timeout=30)
			res =response.read()
			ret =json.loads(res) 
			if ret["ret"]=="ok":
				ret["data"][0]=cn2pinyin(ret["data"][0])
				ret["data"][1]=cn2pinyin(ret["data"][1])
				ret["data"][2]=cn2pinyin(ret["data"][2])
				ret["data"][4]=cn2pinyin(ret["data"][4])
				#res_pinyin=json.dumps(ret)
#				print res_pinyin
				save_local(ipstr, ret)
				return ret
			else:
				print "over limit 10000"
	except:
		print traceback.print_exc()
		return 'None'


def query_main(ipstr):
	ipmsg =ip2Location(ipstr)
	# {'city_name': u'Dezhou', 'raw_location': '37.448608,116.292503', 'province_name': u'Shandong', 'country_code': u'CN', 'country_name': u'China'}
	try:
		if ipmsg.country_short=="CN" or ipmsg.region=="-":
			info=ipip_info(ipstr)
			if not info:
					d = {"city_name":ipmsg.city,"raw_location":"%f,%f"%(ipmsg.latitude,ipmsg.longitude),"country_code":ipmsg.country_short,"country_name":ipmsg.country_long,"province_name":ipmsg.region}
			else:
					data=info["data"]
					d = {"city_name":data[2],"raw_location":"%f,%f"%(float(data[5]),float(data[6])),"country_code":data[11],"country_name":data[0],"province_name":data[1]}
#print  d
			return  d
		else:
			d = {"city_name":ipmsg.city,"raw_location":"%f,%f"%(ipmsg.latitude,ipmsg.longitude),"country_code":ipmsg.country_short,"country_name":ipmsg.country_long,"province_name":ipmsg.region}
		return d
	except :
		d = {"city_name":ipmsg.city,"raw_location":"%f,%f"%(ipmsg.latitude,ipmsg.longitude),"country_code":ipmsg.country_short,"country_name":ipmsg.country_long,"province_name":ipmsg.region}
		return d


if __name__ == '__main__':
	#IP_ADDR='103.215.210.3'
#IP_ADDR='123.58.224.35'
	IP_ADDR='105.235.111.102'
	query_main(IP_ADDR)
```
<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="http://music.163.com/outchain/player?type=2&id=28378127&auto=1&height=66"></iframe>

