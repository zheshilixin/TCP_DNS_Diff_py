# -*- coding: utf-8 -*-

import csv
import geoip2.database
import time
import requests
import socket,struct
reader = geoip2.database.Reader('GeoLite2/GeoLite2-City.mmdb')

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
			# dict['province'] = res.subdivisions.most_specific.name
			dict['city'] = res.city.name
			# dict['postal_code'] = res.postal.code
			# dict['location'] = res.location.latitude
			geo_list.append(dict)
		except Exception,e:
			print e
	return geo_list

# def getgeo(sip_list):
# 	geo_list = []
# 	for sip in sip_list:
# 		try:
# 			url = 'https://ip.awk.sh/api.php?ip=' + str(sip)
# 			r = requests.get(url)
# 			geo_list.append(r.content)
# 			time.sleep(0.5)
# 		except Exception,e:
# 			print e
# 	return geo_list


def addr2dec(addr):
	"将点分十进制IP地址转换成十进制整数"
	items = [int(x) for x in addr.split(".")]
	return sum([items[i] << [24, 16, 8, 0][i] for i in range(4)])


def dec2addr(dec):
	"将十进制整数IP转换成点分十进制的字符串IP地址"
	return ".".join([str(dec >> x & 0xff) for x in [24, 16, 8, 0]])



with open('new.csv') as f:
	reader = csv.reader(f)
	rows = [row[0] for row in reader][1:]
	sip_list = []
	for key in rows:
		sip = dec2addr(addr2dec(key))
		sip_list.append(sip.decode())
	#sip_list = [u'180.97.33.107', u'180.109.37.236', u'23.92.24.244', u'74.125.204.100', u'74.125.204.101', u'180.97.33.108', u'74.125.204.102', u'36.110.170.33', u'58.215.118.31', u'58.222.38.25', u'74.125.204.113', u'183.60.92.202', u'220.181.72.229', u'52.230.85.180', u'58.221.63.4', u'74.125.204.138', u'180.97.33.138', u'180.97.36.45', u'14.17.42.43', u'14.18.245.239', u'52.230.84.217', u'59.46.38.18', u'65.52.171.231', u'101.89.15.101', u'101.226.76.166', u'117.48.124.214', u'121.227.7.33', u'121.227.7.48', u'172.217.24.196', u'180.97.93.48', u'180.101.212.35', u'180.163.32.152', u'203.100.93.112', u'1.82.233.76', u'1.192.194.153', u'14.215.177.221', u'36.110.171.36', u'40.73.97.80', u'42.62.94.95', u'49.4.44.144', u'52.175.23.79', u'52.230.84.0', u'58.20.238.75', u'58.216.55.34', u'59.111.0.76', u'61.129.7.39', u'61.129.48.139', u'61.129.129.205', u'61.183.164.37', u'64.71.168.217', u'74.125.23.113', u'74.125.204.139', u'101.89.15.105', u'101.89.224.57', u'104.17.83.18', u'106.2.69.113', u'106.11.186.25', u'110.75.138.1', u'111.206.223.249', u'117.48.116.19', u'117.157.174.3', u'118.26.252.90', u'118.26.252.202', u'119.123.45.89', u'123.58.182.251', u'123.150.94.98', u'124.74.249.197', u'130.211.38.145', u'139.219.98.160', u'140.206.78.23', u'172.217.25.10', u'172.217.31.234', u'180.97.66.48', u'180.97.146.148', u'180.101.153.16', u'180.149.135.236', u'180.149.138.174', u'180.149.153.11', u'180.163.237.29', u'180.163.238.166', u'180.169.119.23', u'183.3.235.67', u'183.36.108.32', u'210.45.64.37', u'213.227.186.139', u'216.58.199.106', u'216.58.220.202', u'218.15.136.26', u'220.181.163.77', u'223.73.235.227']
	# geo_ip = getgeo(sip_list)
	# print geo_ip