from elasticsearch import Elasticsearch
import IPy
from IPy import IP
import time
import json
import datetime, sys
import os
es = Elasticsearch(['192.168.10.102'], port=9200)
pot1 = time.clock()


def get_dns(index,gte,lte,querystr):
    search_option1 ={
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": querystr,
                            "analyze_wildcard": True
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
                "must_not": [ ]
            }
        },
        "_source": {
            "excludes": [ ]
        },
        "aggs": {
            "2": {
                "terms": {
                    "field": "dip",
                    "size": 10000,
                    "order": {
                        "_count": "desc"
                    }
                },
                "aggs": {
                    "3": {
                        "terms": {
                            "field": "answer",
                            "size": 10000,
                            "order": {
                                "_count": "desc"
                            }
                        }
                    }
                }
            }
        }
    }
    dns_result = es.search(index=index, body=search_option1)
    clean_dns_result = dns_result['aggregations']['2']['buckets']
    dns_list = []
    for dict_buckets in clean_dns_result:
        answer_list = dict_buckets['3']['buckets']
        dip = dict_buckets['key']
        for answer_key in answer_list:
            dns_dict = {}
            dns_dict['sip'] = dip
            dns_dict['dip'] = answer_key['key']
            # dns_dict['sum_flow']  = answer_key['doc_count']
            dns_list.append(dns_dict)
    return dns_list

def get_tcp(index,gte,lte,querystr):
    search_option2 = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": querystr,
                            "analyze_wildcard": True
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
                    "field": "sip",
                    "size": 100,
                    "order": {
                        "_count": "desc"
                    }
                },
                "aggs": {
                    "3": {
                        "terms": {
                            "field": "dip",
                            "size": 100,
                            "order": {
                                "_count": "desc"
                            }
                        }
                    }
                }
            }
        }
    }
    tcp_result = es.search(index=index, body=search_option2)
    clean_tcp_result = tcp_result['aggregations']['2']['buckets']
    tcp_list = []
    for dict_buckets in clean_tcp_result:
        answer_list = dict_buckets['3']['buckets']
        dip = dict_buckets['key']
        for answer_key in answer_list:
            tcp_dict = {}
            tcp_dict['sip'] = dip
            tcp_dict['dip'] = answer_key['key']
            # tcp_dict['sum_flow']  = answer_key['doc_count']
            tcp_list.append(tcp_dict)
    return tcp_list

__ustc_sip__ = [
        '192.168.0.0 TO 192.168.255.255',
        '114.214.160.0 TO 114.214.191.255',
        '114.214.192.0 TO 114.214.255.255',
        '202.38.64.0 TO 202.38.95.255',
        '210.45.64.0 TO 210.45.79.255',
        '210.45.112.0 TO 210.45.127.255',
        '211.86.144.0 TO 211.86.159.255',
        '222.195.64.0 TO 222.195.95.255',
        '210.72.22.0 TO 210.72.22.255',
        '202.111.192.24 TO 202.111.192.31',
        '202.141.160.0 TO 202.141.175.255',
        '218.22.21.0 TO 218.22.21.31',
        '218.22.22.160 TO 218.22.22.191',
        '218.104.71.160 TO 218.104.71.175',
        '218.104.71.96 TO 218.104.71.111',
        '202.141.176.0 TO 202.141.191.255',
        '121.255.0.0 TO 121.255.255.255',
        '202.38.140.112 TO 202.38.140.119',
        '58.200.29.0 TO 58.200.29.255',
        '202.127.237.0 TO 202.127.237.127',
        '61.190.7.69 TO 61.190.7.73',
        '36.33.32.8 TO 36.33.32.12',
        '202.127.200.0 TO 255.255.248.0',
        '210.73.16.0 TO 255.255.240.0'
    ];
__ustc_sip2__ = [
        '[192.168.0.0 TO 192.168.255.255]',
        '[114.214.160.0 TO 114.214.191.255]',
        '[114.214.192.0 TO 114.214.255.255]',
        '[202.38.64.0 TO 202.38.95.255]',
        '[210.45.64.0 TO 210.45.79.255]',
        '[210.45.112.0 TO 210.45.127.255]',
        '[211.86.144.0 TO 211.86.159.255]',
        '[222.195.64.0 TO 222.195.95.255]',
        '[210.72.22.0 TO 210.72.22.255]',
        '[202.111.192.24 TO 202.111.192.31]',
        '[202.141.160.0 TO 202.141.175.255]',
        '[218.22.21.0 TO 218.22.21.31]',
        '[218.22.22.160 TO 218.22.22.191]',
        '[218.104.71.160 TO 218.104.71.175]',
        '[218.104.71.96 TO 218.104.71.111]',
        '[202.141.176.0 TO 202.141.191.255]',
        '[121.255.0.0 TO 121.255.255.255]',
        '[202.38.140.112 TO 202.38.140.119]',
        '[58.200.29.0 TO 58.200.29.255]',
        '[202.127.237.0 TO 202.127.237.127]',
        '[61.190.7.69 TO 61.190.7.73]',
        '[36.33.32.8 TO 36.33.32.12]',
        '[02.127.200.0 TO 255.255.248.0]',
        '[210.73.16.0 TO 255.255.240.0]'
    ];
dns_list_all = []
tcp_list_all = []
lost_tcp = []
for key in __ustc_sip2__:
    tcp_gte = 1536066300000
    dns_gte = 1536066000000
    lte = 1536066600000
    try:
        dns_query_str = "isresponse:1 AND answer:[0.0.0.0 TO 255.255.255.255] AND dip:" + key
        tcp_query_str = "(dport:80 OR dport:443) AND timeout_state_num:8 AND unknown_conn:0 AND sip:" + key
        dns_list2 = get_dns(index='dns-2018-09-10', gte=dns_gte,lte=lte,querystr=dns_query_str)
        tcp_list2 = get_tcp(index='tcp-2018-09-10', gte=tcp_gte,lte=lte,querystr=tcp_query_str)
        for key in dns_list2:
            dns_list_all.append(key)
        for key in tcp_list2:
            tcp_list_all.append(key)
            if key not in dns_list2:
                lost_tcp.append(key)
        # print dns_query_str
        # print tcp_query_str
    except:
        print "null"


print len(dns_list_all)
print len(tcp_list_all)
print len(lost_tcp)

pot2 = time.clock()
print (pot2 - pot1)


# # Define config
# host = "192.168.10.102"
# port = 9200
# timeout = 1000
# index = "dns-2018-09-10"
# doc_type = "type"
# size = 1000000
# body = {}
#
# # Init Elasticsearch instance
# es = Elasticsearch(
#     [
#         {
#             'host': host,
#             'port': port
#         }
#     ],
#     timeout=timeout
# )
#
#
# # Process hits here
# def process_hits(hits):
#     for item in hits:
#         print(json.dumps(item, indent=2))
#
#
# # Check index exists
# if not es.indices.exists(index=index):
#     print("Index " + index + " not exists")
#     exit()
#
# # Init scroll by search
# data = es.search(
#     index=index,
#     doc_type=doc_type,
#     scroll='2m',
#     size=size,
#     body=body
# )
#
# # Get the scroll ID
# sid = data['_scroll_id']
# scroll_size = len(data['hits']['hits'])
#
# # Before scroll, process current batch of hits
# process_hits(data['hits']['hits'])
#
# while scroll_size > 0:
#     "Scrolling..."
#     data = es.scroll(scroll_id=sid, scroll='2m')
#
#     # Process current batch of hits
#     process_hits(data['hits']['hits'])
#
#     # Update the scroll ID
#     sid = data['_scroll_id']
#
#     # Get the number of results that returned in the last scroll
#     scroll_size = len(data['hits']['hits'])