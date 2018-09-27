# -*- coding: utf-8 -*-


from elasticsearch import Elasticsearch
import requests,json,time
import geoip2.database
import numpy as np
import pandas as pd
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby #itertool还包含有其他很多函数，比如将多个list联合起来。。
false = False
true  = True
reader = geoip2.database.Reader('GeoLite2/GeoLite2-City.mmdb')
es = Elasticsearch(['192.168.0.122'], port=9222)

def printRecord(tgt):
  rec = gi.record_by_addr(tgt)
  city = rec['city']
  region = rec['region_code']
  country = rec['country_name']
  long = rec['longitude']
  lat = rec['latitude']
  print '[*] 主机: ' + tgt + ' Geo-located.'
  print '[+] ' + str(city) + ', ' + str(region) + ', ' + str(country)
  print '[+] 经度: ' + str(lat) + ', 维度: ' + str(long)
# for sip in sip_list:
#     try:
#
#         url = 'https://ip.awk.sh/api.php?ip=' + str(sip)
#         r = requests.get(url)
#         geo_list.append(r.content)
#     except:
#         print ('error')

def getdip(index,gte,lte):
	search_option = {
	  "size": 0,
	  "query": {
		"bool": {
		  "must": [
			{
			  "query_string": {
				"query": "NOT dip:[192.168.0.0 TO 192.168.255.255]",
				"analyze_wildcard": true
			  }
			},
			{
			  "range": {
				"@timestamp": {
				  "gte": gte,
				  "lte": lte,
				  "format": "epoch_millis"
				}
			  }
			}
		  ],
		  "must_not": []
		}
	  },
	  "_source": {
		"excludes": []
	  },
	  "aggs": {
		"2": {
		  "terms": {
			"field": "dip",
			"size": 1000000,
			"order": {
			  "_count": "desc"
			}
		  }
		}
	  }
	}
	json_sip = es.search(index=index, body=search_option)
	clear_result = json_sip['aggregations']['2']['buckets']
	sip_list = []
	for sip_key in clear_result:
		sip_list.append(sip_key['key'])
	return sip_list

def getgeo(sip_list):
	count = 0
	geo_list = []
	for sip in sip_list:
		try:
			res = reader.city(sip)
			dict = {}
			dict['geo_code'] = res.country.iso_code
			dict['name'] = res.country.names['zh-CN']
			dict['sip'] = sip
			dict['province'] = res.subdivisions.most_specific.name
			#dict['city'] = res.city.name
			# dict['postal_code'] = res.postal.code
			# dict['location'] = res.location.latitude
			geo_list.append(dict)
		except Exception,e:
			print e
	return geo_list

def main(interval):
	pot1 = time.clock()
	now = time.time()
	sec_now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(now))
	time_list = []
	sec_now_split = sec_now.split('-')
	for key in sec_now_split:
		time_list.append(key)
	tcp_index = 'tcp-' + time_list[0] + '-' + time_list[1] + '-' + time_list[2]
	gte = int(round(now - 60 * interval) * 1000)
	lte = int(round(now) * 1000)
	print tcp_index,gte,lte
	sip_list = getdip(tcp_index,gte,lte)
	geo_list = getgeo(sip_list)
	data = pd.DataFrame(geo_list)
	print data
	print len(geo_list)

	# combine = data['sip'].groupby(data['geo_code'])
	# print combine.mean()

	# geo_list.sort(key = itemgetter('geo_code'))
	# list_goup = groupby(geo_list,itemgetter('geo_code'))

	# for key,group in list_goup:
	# 	if (key != 'CN'):
	# 		print key
	# 		sip_list2 = []
	# 		for g in group:
	# 			sip_list2.append(g['sip'])
	# 		print ("访问 %s 的数据一共有： %s 个:    "%(str(key),str(len(sip_list2))))
	# 		print sip_list2

	pot2 = time.clock()
	print (pot2 - pot1)


if __name__ == '__main__':
    interval = input("你想获得多久的数据(从当前时间往前按分钟计算）： ")
    main(interval)