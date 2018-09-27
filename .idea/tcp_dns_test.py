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
import datetime, sys, re
import os

true = True
false = False
#浏览器默认DNS缓存时间：5min
dns_cache = 5

es = Elasticsearch(['192.168.0.122'], port=9222)
#es = Elasticsearch(['192.168.1.103'], port=9200)

dns_query_str = "isresponse:1 AND answer:[0.0.0.0 TO 255.255.255.255] AND dip:[192.168.0.0 TO 192.168.255.255]"
tcp_query_str = "(dport:80 OR dport:443) AND timeout_state_num:8 AND sip:[192.168.0.0 TO 192.168.255.255] AND unknown_conn:0"


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
                    "size": 1000,
                    "order": {
                        "_count": "desc"
                    }
                },
                "aggs": {
                    "3": {
                        "terms": {
                            "field": "dip",
                            "size": 1000,
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

#由于不能解析443对应的HTTPS，只能从DNS中查询host信息
def host_check(index,sip,dip,gte,lte):
    search_option= {
    "size": 0,
    "query": {
        "bool": {
            "must": [
                {
                    "query_string": {
                        "query": "*",
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
                "size": 5,
                "order": {
                    "_count": "desc"
                }
            },
            "aggs": {
                "3": {
                    "terms": {
                        "field": "question",
                        "size": 5,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            }
        }
    }
}
    result = es.search(index=index,body=search_option)
    clean_dns_result = json_answer_question['aggregations']['2']['buckets']
    answer_list = []
    for dns_key in clean_dns_result:
        dict = {}
        question = dns_key['3']['buckets']
        question_list = []
        for q_key in question:
            question_list.append(q_key['key'])
        dict['answer'] = dns_key['key']
        dict['question'] = question_list
        answer_list.append(dict)
    return answer_list

pattern = re.compile(r"^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))")

def get_http(index,gte,lte):
    search_option = {
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "query_string": {
            "analyze_wildcard": true,
            "query": "*"
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
        "size": 1000,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "3": {
          "terms": {
            "field": "url",
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
    result = es.search(index=index,body=search_option)
    clear_result = result['aggregations']['2']['buckets']
    http_list = []
    for ket in clear_result:
        # print ket
        sip = ket['key']
        for key in ket['3']['buckets']:
            dict = {}
            url = key['key']
            if (pattern.findall(url)):
                dict['sip'] = sip
                dict['url'] = url
                http_list.append(dict)
    return http_list

def main(interval):
    pot1 = time.clock()

    now = time.time()
    sec_now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(now))
    print sec_now
    time_list = []
    sec_now_split = sec_now.split('-')
    for key in sec_now_split:
        time_list.append(key)
    tcp_index = 'tcp-' + time_list[0] + '-' + time_list[1] + '-' + time_list[2]
    dns_index = 'dns-' + time_list[0] + '-' + time_list[1] + '-' + time_list[2]
    http_index = 'http-' + time_list[0] + '-' + time_list[1] + '-' + time_list[2]
    tcp_gte = int(round(now - 60 * interval) * 1000)
    dns_gte = int(round(now - 60 * (interval+dns_cache)) * 1000)
    lte = int(round(now) * 1000)
    dns_list = get_dns(dns_index,dns_gte,lte,dns_query_str)
    tcp_list = get_tcp(tcp_index,tcp_gte,lte,tcp_query_str)
    http_list = get_http(http_index,tcp_gte,lte)

    pot2 = time.clock()

    lostlist_tcp = []
    for tcp_key in tcp_list:
        if tcp_key not in dns_list:
            lostlist_tcp.append(tcp_key)
        else:
            continue

    pot3 = time.clock()

    conn_lasted = []
    conn_repeated = []
    tcp_check_gte = int(round(now - 120 * interval) * 1000)
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
    dns_check_gte = int(round(now - 60 * interval - 86400) * 1000)
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
            #过去的24h内没有出现对该host的解析
            dns_clean_result.append(lasted_key)
        else:
            #过去的24h内出现了对该host 的解析，但没有访问
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
        gte = int(round(now - 60 * interval - time_check_hour * 3600) * 1000)
        lte = tcp_gte
        result_conn = repeated_check2(tcp_index,repeated_key['sip'],repeated_key['dip'],gte,lte)
        if (result_conn >= 30):
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
    for key in dns_ttl_result:
        print key

    print ("#@#@$@#$@#$")
    for key in http_list:
        print key

if __name__ == '__main__':
    interval = input("你想获得多久的数据(从当前时间往前按分钟计算）： ")
    main(interval)