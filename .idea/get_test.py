from elasticsearch import Elasticsearch
import IPy
from IPy import IP
import time
import json
import datetime, sys
import os
pot1 = time.clock()
es = Elasticsearch(['192.168.10.102'], port=9200)
search_option = {
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
              "gte": 1535990400000,
              "lte": 1536076799999,
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
tcp_result = es.search(index='tcp-2018-09-10', body=search_option)

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

print (len(tcp_list))
pot2 = time.clock()
print (pot2 - pot1)