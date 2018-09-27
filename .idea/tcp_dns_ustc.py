# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from elasticsearch import Elasticsearch
import IPy
from IPy import IP
import time
import json
import datetime, sys
import os

#浏览器默认DNS缓存时间：5min
dns_cache = 5

# es = Elasticsearch(['192.168.10.102'], port=9200)
es = Elasticsearch(['192.168.10.102'], port=9200)

dns_query_str = "isresponse:1 AND answer:[0.0.0.0 TO 255.255.255.255] AND dip:[222.195.64.0 TO 222.195.95.255]"
dns_query_all = "isresponse:1 AND answer:[0.0.0.0 TO 255.255.255.255]"
tcp_query_str = "(dport:80 OR dport:443) AND timeout_state_num:8 AND sip:[222.195.64.0 TO 222.195.95.255] AND unknown_conn:0"

# dns_query_str = "isresponse:1 AND answer:[0.0.0.0 TO 255.255.255.255] AND dip:[192.168.0.0 TO 192.168.255.255]"
# tcp_query_str = "(dport:80 OR dport:443) AND timeout_state_num:8 AND sip:[192.168.0.0 TO 192.168.255.255] AND unknown_conn:0"


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

def get_tcp_all(index,gte,lte):
    __ustc_sip__ = [
        ['192.168.0.0 TO 192.168.255.255'],
        ['114.214.160.0 TO 114.214.191.255'],
        ['114.214.192.0 TO 114.214.255.255'],
        ['202.38.64.0 TO 202.38.95.255'],
        ['210.45.64.0 TO 210.45.79.255'],
        ['210.45.112.0 TO 210.45.127.255'],
        ['211.86.144.0 TO 211.86.159.255'],
        ['222.195.64.0 TO 222.195.95.255'],
        ['210.72.22.0 TO 210.72.22.255'],
        ['202.111.192.24 TO 202.111.192.31'],
        ['202.141.160.0 TO 202.141.175.255'],
        ['218.22.21.0 TO 218.22.21.31'],
        ['218.22.22.160 TO 218.22.22.191'],
        ['218.104.71.160 TO 218.104.71.175'],
        ['218.104.71.96 TO 218.104.71.111'],
        ['202.141.176.0 TO 202.141.191.255'],
        ['121.255.0.0 TO 121.255.255.255'],
        ['202.38.140.112 TO 202.38.140.119'],
        ['58.200.29.0 TO 58.200.29.255'],
        ['202.127.237.0 TO 202.127.237.127'],
        ['61.190.7.69 TO 61.190.7.73'],
        ['36.33.32.8 TO 36.33.32.12'],
        ['202.127.200.0 TO 255.255.248.0'],
        ['210.73.16.0 TO 255.255.240.0']
    ];
    tcp_list_all = []
    for key in __ustc_sip__:
        tcp_query_str = "(dport:80 OR dport:443) AND timeout_state_num:8 AND unknown_conn:0" + " AND sip:" + str(key)
        tcp_list_all.append(get_tcp(index,gte,lte,tcp_query_str))
    return tcp_list_all

def get_tcp_wrong(index,sip,dip,gte,lte):
    sip_list = []
    querystr = 'sip:'+ sip + ' AND '+ 'dip:' + dip
    search_option = {
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
                "field": "dport",
                "size": 5,
                "order": {
                    "_count": "desc"
                }
            }
        }
    }
}
    result = es.search(index=index, body=search_option)
    clean_result = result['aggregations']['2']['buckets']
    if (clean_result != []):
        for clean_key in clean_result:
            sip_dict = {}
            sip_dict['sip'] = sip
            sip_dict['dip'] = dip
            sip_dict['dport'] = clean_key['key']
            #sip_dict['sum_flow'] = clean_key['doc_count']
            sip_list.append(sip_dict)
            return sip_dict

def get_dns_wrong(index,answer,gte,lte):
    querystr = "isresponse:1 AND answer:"+answer
    search_option = {
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
    "aggs": { }
}
    result = es.search(index=index,body=search_option)
    clean_result = result['hits']['total']
    return clean_result

def get_dns_wrong2(index,gte,lte):
    querystr = "isresponse:1 AND answer:[0.0.0.0 TO 255.255.255.255]"
    dip_list = []
    search_optopn = {
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
                "field": "answer",
                "size": 100000,
                "order": {
                    "_count": "desc"
                }
            }
        }
    }
}
    result = es.search(index=index,body=search_optopn)
    clean_result = result['aggregations']['2']['buckets']
    for clean_key in clean_result:
        dip_list.append(clean_key['key'])
    return dip_list

def repeated_check(index,sip,dip,gte,lte):
    querystr = 'sip:'+sip+' AND dip:'+dip+' unknown_conn:0'
    search_option = {
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
    "aggs": { }
}
    result = es.search(index=index, body=search_option)
    clean_result = result['hits']['total']
    if (clean_result != 0):
        return 1
    else:
        return 0

def repeated_check2(index,sip,dip,gte,lte):
    interval_time = '5m'
    time_zone = "Asia/Shanghai"
    querystr = 'sip:'+sip+' AND dip:'+dip+' unknown_conn:0'
    search_option = {
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
        "1": {
            "avg_bucket": {
                "buckets_path": "1-bucket>_count"
            }
        },
        "1-bucket": {
            "date_histogram": {
                "field": "@timestamp",
                "interval": interval_time,
                "time_zone": time_zone,
                "min_doc_count": 1
            }
        }
    }
}
    result = es.search(index=index, body=search_option)
    clean_result = result["aggregations"]['1-bucket']['buckets']
    return (len(clean_result))


def main(interval):
    pot1 = time.clock()

    now = time.time()
    sec_now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(now))
    time_list = []
    sec_now_split = sec_now.split('-')
    for key in sec_now_split:
        time_list.append(key)
    # tcp_index = 'tcp-' + time_list[0] + '-' + time_list[1] + '-' + time_list[2]
    # dns_index = 'dns-' + time_list[0] + '-' + time_list[1] + '-' + time_list[2]
    tcp_index = 'tcp-2018-09-10'
    dns_index = 'dns-2018-09-10'
    # tcp_gte = int(round(now - 60 * interval) * 1000)
    # dns_gte = int(round(now - 60 * (interval+dns_cache)) * 1000)
    # lte = int(round(now) * 1000)
    tcp_gte = 1536026100000
    dns_gte = 1536025800000
    lte     = 1536026340000
    dns_list = get_dns(dns_index,dns_gte,lte,dns_query_str)
    tcp_list = get_tcp(tcp_index,tcp_gte,lte,tcp_query_str)
    #tcp_list = get_tcp_all(tcp_index,tcp_gte,lte)
    pot2 = time.clock()
    print (pot2-pot1)
    lostlist_tcp = []
    for tcp_key in tcp_list:
        if tcp_key not in dns_list:
            lostlist_tcp.append(tcp_key)
        else:
            continue

    pot3 = time.clock()

    conn_lasted = []
    conn_repeated = []
    # tcp_check_gte = int(round(now - 120 * interval) * 1000)
    tcp_check_gte = 1536022800000
    tcp_check_lte = tcp_gte
    #将么有经过DNS解析的TCP连接分为：重复出现的，最近interval出现的。
    #检查该ip在过去的double时间内有没有再次访问（可考虑频次问题）
    # for lost_key in lostlist_tcp:
    #     sip_dict = get_tcp_wrong(tcp_index,lost_key['sip'],lost_key['dip'],tcp_check_gte,tcp_check_lte)
    #     #sip_list.append(sip_dict)
    #     if (sip_dict == None):
    #         conn_lasted.append(lost_key)
    #     else:
    #         conn_repeated.append(sip_dict)
    the_last_tcp_list = get_tcp(tcp_index,tcp_check_gte,tcp_check_lte,tcp_query_str)
    for lost_key in lostlist_tcp:
        if lost_key in the_last_tcp_list:
            conn_repeated.append(lost_key)
        else:
            conn_lasted.append(lost_key)


    pot4 = time.clock()

    #检查lasted是否在之前的24h时间内有DNS解析，但没有访问（TTL情况）
    #既同一dip，但sip不同
    # dns_check_gte = int(round(now - 60 * interval - 86400) * 1000)
    dns_check_gte = 1536022800000
    dns_check_lte = dns_gte
    dns_clean_result = []
    dns_ttl_result = []
    # for lasted_key in conn_lasted:
    #     dns_count = get_dns_wrong(dns_index,lasted_key['dip'],dns_check_gte,dns_check_lte)
    #     if (dns_count == 0):
    #         dns_clean_result.append(lasted_key)
    the_last_dns_list = get_dns_wrong2(dns_index,dns_check_gte,dns_check_lte)
    for lasted_key in conn_lasted:
        if lasted_key['dip']  not in the_last_dns_list:
            dns_clean_result.append(lasted_key)
        else:
            dns_ttl_result.append(lasted_key)

    pot5 = time.clock()

    #检查repeated是否是有规律的访问情况，在过去3h内(访问同一主机3h内以每interval2的频次访问在90%以上)。正常的web访问应该极少发生
    #注意，查10000次公司ES数据约21s，该操作非常耗时
    error_repeated = []
    #查询过去固定时间内的总sip-dip
    time_check_hour = 3
    # interval2 = 5
    # time_round = int(180/interval2)
    # time_interval = 60*interval2
    # for repeated_key in conn_repeated:
    #     count = 0
    #     for i in range(0, time_round):
    #         gte = int(round(now - (i +1) * time_interval) * 1000)
    #         lte = int(round(now - i * time_interval) * 1000)
    #         result_conn = repeated_check(tcp_index,repeated_key['sip'],repeated_key['dip'],gte,lte,)
    #         count = count + result_conn
    #     if (count >= 32):
    #         error_repeated.append(repeated_key)
    for repeated_key in conn_repeated:
        # gte = int(round(now - 60 * interval - time_check_hour * 3600) * 1000)
        # lte = gte
        gte = 1536022800000
        lte = 1536026340000
        result_conn = repeated_check2(tcp_index,repeated_key['sip'],repeated_key['dip'],gte,lte)
        if (result_conn >= 10):
            error_repeated.append(repeated_key)


    print ('dns list length:                       '  + str(len(dns_list)))
    print ('tcp list length:                       '  + str(len(tcp_list)))
    print ("tcp_dns_diff:                          "  + str(len(lostlist_tcp)))
    print ("repeated in last double interval time: "  + str(len(conn_repeated)))
    print ("the lasted in last interval time  :    "  + str(len(conn_lasted)))
    print ("the lasted and 24h dns not checked:    "  + str(len(dns_ttl_result)))
    print ("the error_repeated conn                "  + str(len(error_repeated)))
    print ("the error_repeated conn : ")
    for error_key in error_repeated:
        print (error_key)
    pot6 = time.clock()

    print('GET TCP&DNS time:    %s Seconds' % (pot2 - pot1))
    print('GET DIFF time:       %s Seconds' % (pot3 - pot2))
    print('GET Re&LA time:      %s Seconds' % (pot4 - pot3))
    print('GET UnTTL time:      %s Seconds' % (pot5 - pot4))
    print('GET 5 minutely time: %s Seconds' % (pot6 - pot5))
    print('Running time:        %s Seconds' % (pot6 - pot1))
    print ("the DNS_TTL_Result : ")
    # for key in dns_ttl_result:
    #     print key

if __name__ == '__main__':
    interval = input("你想获得多久的数据(从当前时间往前按分钟计算）： ")
    main(interval)