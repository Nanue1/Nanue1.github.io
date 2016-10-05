
title: ES查询Django接口
date: 2016-10-01 17:49:58
tags: elasticsearch 
---
从elasticsearch中取数据, from elasticsearch import Elasticsearch中提供了helpers.scan()
    > elasticsearch.helpers.scan(client, query=None, scroll=u'5m',size=1000, request_timeout=None)

在Django 中使用的时候 总是报timeout请求超时,找了好久原因,后来发现是Elasticsearch创建连接的时候timeout设置的默认10,修改为30便解决了这个问题
    > client=Elasticsearch(['http://10.24.xx.95:9200'],timeout=30,max_retries=10,retry_on_timeout=True)

Django urls 设置:
    > urlpatterns = [ url(r'^ipasset4/query', 'api.task.ipasset4_query')]

<!-- more -->

ES查询语句构造:
  ```json
  {"query":
      {"bool":
          {"must":[
              {"match":{"servers.banner":{"query":"openssl","operator":"and"}}},
              {"match":{"city":{"query":"Beijin","operator":"and"}}}
              ]
          }
      }
  } 
  ```

## 代码区

```python

@csrf_exempt 
def ipasset4_query(request): 
    ALL_FILED_KEY=["banner","city","port"] 
    IN_SERVICES_FILED_KEY=["banner"] 
    QUERY_KEY={"banner":"services.banner","port":"services.layer.transport.port","city":"city"} 
    QUERY_DIC = {"query": {"bool": {"must":[]}}} 
    QUERY_LIST=QUERY_DIC['query']['bool']['must'] 
    send_data=[]
    arg_dic= json.loads(json.dumps(request.POST)) 
    #arg_dic= request.POST 
    try:
        if type(arg_dic)==dict:
            tmp_dic={}
            for arg_key,arg_value in arg_dic.items():
                if arg_key in ALL_FILED_KEY:
                        query_key= QUERY_KEY[arg_key]
                else: 
                        print "don't suport this query"
                if type(arg_value)==list:
                        for singal_value in arg_value :
                                tmp_dic["match"]={query_key:{"query":singal_value, "operator":"and"}}
                                QUERY_LIST.append(tmp_dic)
                                tmp_dic={}
                else:
                        tmp_dic["match"]={query_key:{"query":arg_value, "operator":"and"}}
                        QUERY_LIST.append(tmp_dic)
                        tmp_dic={}
        else:
                print "arg_dic not dict " 
    except Exception,e:
            logger.error('scan error: %s ' % (e,)) 
            response = {}
            response['state'] = -1
            response['msg'] = "arg_dic example {'banner':['DVRDVS-Webs','APP-Webs'],'port':'23'}"
            return JsonResponse(response,safe=False)
    dst_es = Elasticsearch(['http://10.24.xx.95:9200'],timeout=30, max_retries=10, retry_on_timeout=True )
    scanRepo = helpers.scan(dst_es, query=QUERY_DIC, index='ipasset_seer4', scroll='5m', request_timeout=1000)
    for resp in scanRepo:
        src  = resp['_source']
        ip = src['ip']
        services = src['services']
        port_set = set()
        for service in services:
            for arg_key,arg_value in arg_dic.items():
                if arg_key in IN_SERVICES_FILED_KEY:
                    for singal_value in arg_value :
                        if str(singal_value) in service[arg_key] :
                            port = service['layer']['transport']['port']
                            port_set.add(str(port))
                else:
                    port = service['layer']['transport']['port']
                    port_set.add(str(port))
        ports = list(port_set)
        if not ports:
            continue
        json_s= ':'.join([ip, ','.join(ports)]) 
        send_data.append(json_s)
    return JsonResponse(send_data,safe=False)
```
