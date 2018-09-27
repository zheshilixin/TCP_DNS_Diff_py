# -*- coding: utf-8 -*-
import os
from elasticsearch import Elasticsearch
import time,datetime
import re
false = False
true  = True
#注：查询es信息使用curl，插入es使用json
pot1 = time.clock()
es = '192.168.0.122:9222'
es2 = '192.168.10.65:9200'
es_client1 = Elasticsearch(['192.168.0.122'], port=9222)
es_client2 = Elasticsearch(['192.168.10.65'], port=9200)

#不同告警的阈值。由于存在不同节点的磁盘空间大小不一样，有两种告警方式
#若某个node的disk.percent超过70% info，某个node超过90%，warning
#若计算平均可用磁盘容量不足以存放七天的数据，warning
info_per = 70
warn_per = 90
info_last_days = 14
warn_last_days = 7

#获取平均几天的数据？
day_len = 7

index = ['tcp','udp','http','dns','link','traffic','status','alert']

# 查询节点信息命令，包括disk及ram信息，暂时只使用disk信息
disk_cmd = "curl -X GET \"" + es +"/_cat/allocation?v&\" -s"
ram_cmd  = "curl -X GET \"" + es + "/_cat/nodes?v\" -s "

def get_info():
    result_disk = os.popen(disk_cmd).read()
    result_ram  = os.popen(ram_cmd).read()
    disk_info = []
    ram_info  = []
    for i in range(1,len(result_disk.splitlines())):
        est = result_disk.splitlines()[i].split()
        dict = {}
        dict['shards']          = est[0]
        dict['disk.indices']    = est[1]
        #dict['disk.used']       = est[2]
        dict['disk.avail']      = est[3]
        #dict['disk.total']      = est[4]
        dict['disk.percent']    = est[5]
        dict['host']            = est[6]
        dict['ip']              = est[7]
        dict['node']            = est[8]
        disk_info.append(dict)

    for i in range(1,len(result_ram.splitlines())):
        est = result_ram.splitlines()[i].split()
        dict = {}
        dict['ip']  = est[0]
        dict['heap.percent'] = est[0]
        dict['heap.percent'] = est[1]
        dict['ram.percent']  = est[2]
        dict['cpu']          = est[3]
        #dict['load_1m']      = est[4]
        #dict['load_5m']      = est[5]
        #dict['load_15m']     = est[6]
        dict['node.role']    = est[7]
        dict['master']       = est[8]
        dict['name']         = est[9]
        ram_info.append(dict)

    return disk_info,ram_info

def insert_es_alert(es,doc):
    result = es.index(
        index='alert-{}'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
        doc_type='netflow_v9',
        body=doc
    )
    return result

def insert_sample1(es,dict,level):
    disk_percent = dict['disk.percent']
    disk_ip = dict['ip']
    # discard = getCheckDeltatime()
    # startTime = datetime.datetime.strptime(discard, '%Y-%m-%d %H:%M:%S')
    # if (time.daylight == 0):  # 1:dst;
    #     time_zone = "%+03d:%02d" % (-(time.timezone / 3600), time.timezone % 3600 / 3600.0 * 60)
    # else:
    #     time_zone = "%+03d:%02d" % (-(time.altzone / 3600), time.altzone % 3600 / 3600.0 * 60)
    # timestamp = (startTime).strftime('%Y-%m-%dT%H:%M:%S.%f') + time_zone
    time_zone_CST = "%+03d:%02d" % (-(time.timezone / 3600), time.timezone % 3600 / 3600.0 * 60)
    insert_time = datetime.datetime.now()
    timestamp = (insert_time).strftime('%Y-%m-%dT%H:%M:%S.%f') + time_zone_CST
    doc = {}
    doc['type'] = 'sys'
    doc['subtype'] = 'the disk has used over ' + str(disk_percent) +'% in ' + str(disk_ip)
    doc['desc_type'] = '[sys] the disk should be repalced'
    doc['@timestamp'] = timestamp
    doc['index'] = 'tcp-*'
    doc['level'] = level
    print doc
    result = insert_es_alert(es=es,doc=doc)
    return result

def insert_sample2(es,last_days,level):
    time_zone_CST = "%+03d:%02d" % (-(time.timezone / 3600), time.timezone % 3600 / 3600.0 * 60)
    insert_time = datetime.datetime.now()
    timestamp = (insert_time).strftime('%Y-%m-%dT%H:%M:%S.%f') + time_zone_CST
    doc = {}
    doc['type'] = 'sys'
    doc['subtype'] = 'the last disk would use '+str(last_days) +' days'
    doc['desc_type'] = '[sys] the disk should be repalced'
    doc['@timestamp'] = timestamp
    doc['index'] = 'tcp-*'
    doc['level'] = level
    print doc
    result = insert_es_alert(es,doc)
    return result

def get_date(days=7):
    day_list = []
    for i in range(1,days+1):
        intime = datetime.datetime.now() - datetime.timedelta(days=i)
        day_list.append(intime.strftime('%Y-%m-%d'))
    return day_list

def get_avg_size(es,index,day_list):
    index_inform = []
    for index_key in index:
        for date_key in day_list:
            all_index = index_key + '-'+ date_key
            cmd = 'curl -X GET \"' + es + '/' + all_index + '/_stats' + '\"'
            try:
                result = os.popen(cmd)
                output = eval(result.read())
                #print output
                shards_size = output['_all']['primaries']['store']['size_in_bytes']
                shards_docs = output['_all']['primaries']['docs']['count']
                disk_size   = output['_all']['total']['store']['size_in_bytes']
                dict = {}
                dict['index'] = all_index
                dict['size'] = shards_size
                dict['docs'] = shards_docs
                dict['disk_used'] = disk_size
                index_inform.append(dict)
                #print dict
            except:
                print cmd
    size = 0
    for index in index_inform:
        size += index['disk_used']
    #获取最近七天里的平均每天的索引大小(从byte转换为gb)
    day_len = float((len(day_list)))
    size_gib = round((size/1073741824.0)/day_len,3)
    return size_gib

disk_info,ram_info = get_info()
day_list = get_date(days=day_len)
avg_size = get_avg_size(es=es,index=index,day_list=day_list)
print avg_size
#任意node的磁盘占用比超过阈值都报警
for key in disk_info:
    percent = int(key['disk.percent'])
    print percent
    if (percent >=info_per and percent <= warn_per):
        insert_sample1(es_client2,key,'info')
    elif(percent >= warn_per):
        insert_sample1(es_client2,key,'warn')

#为所有node所剩余的容量总和(以gb计算)还能使用的天数少于阈值，报警。
disk_avail_all = 0
for disk_key in disk_info:
    #由于disk.avail信息为带单位的，需要转换为固定的，目前暂停使用gb
    disk_list = re.findall(r'\d+\.*\d*|[a-z]+',disk_key['disk.avail'])
    if (disk_list[1] == 'tb'):
        #磁盘厂商进制为1000，但os认为是1024，为了方便采取1024计算
        disk_avail = float(disk_list[0]) * 1024
    else:
        disk_avail = float(disk_list[0])
    disk_avail_all += disk_avail
print disk_avail_all
last_days = int(disk_avail_all/avg_size)
print last_days

if (last_days >= warn_last_days and last_days <= info_last_days):
    insert_sample2(es_client2,last_days,'info')
elif(last_days <= warn_last_days):
    insert_sample2(es_client2,last_days,'warn')

pot2 = time.clock()
print (pot2 - pot1)
