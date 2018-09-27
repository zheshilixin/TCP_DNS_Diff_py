# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import IPy
from IPy import IP
import time
import json
import datetime, sys
import os
import re
import demjson
false = False
true  = True

json  = {
    "took": 2,
    "timed_out": False,
    "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0
    },
    "hits": {
        "total": 329,
        "max_score": 0,
        "hits": [ ]
    },
    "aggregations": {
        "2": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [
                {
                    "key": 80,
                    "doc_count": 329
                }

            ]
        }
    },
    "status": 200
}

json_flase = {
    "took": 2,
    "timed_out": False,
    "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0
    },
    "hits": {
        "total": 0,
        "max_score": 0,
        "hits": [ ]
    },
    "aggregations": {
        "2": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets": [ ]
        }
    },
    "status": 200
}
json_total_result = {
  "took": 1,
  "timed_out": False,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "hits": {
    "total": 71,
    "max_score": 0,
    "hits": []
  },
  "status": 200
}

json_date_histogram = {
    "took": 2,
    "timed_out": False,
    "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0
    },
    "hits": {
        "total": 108,
        "max_score": 0,
        "hits": [ ]
    },
    "aggregations": {
        "1": {
            "value": 9
        },
        "1-bucket": {
            "buckets": [
                {
                    "key_as_string": "2018-09-06T10:00:00.000+08:00",
                    "key": 1536199200000,
                    "doc_count": 7
                },
                {
                    "key_as_string": "2018-09-06T10:05:00.000+08:00",
                    "key": 1536199500000,
                    "doc_count": 9
                },
                {
                    "key_as_string": "2018-09-06T10:10:00.000+08:00",
                    "key": 1536199800000,
                    "doc_count": 10
                },
                {
                    "key_as_string": "2018-09-06T10:15:00.000+08:00",
                    "key": 1536200100000,
                    "doc_count": 8
                },
                {
                    "key_as_string": "2018-09-06T10:20:00.000+08:00",
                    "key": 1536200400000,
                    "doc_count": 10
                },
                {
                    "key_as_string": "2018-09-06T10:25:00.000+08:00",
                    "key": 1536200700000,
                    "doc_count": 8
                },
                {
                    "key_as_string": "2018-09-06T10:30:00.000+08:00",
                    "key": 1536201000000,
                    "doc_count": 10
                },
                {
                    "key_as_string": "2018-09-06T10:35:00.000+08:00",
                    "key": 1536201300000,
                    "doc_count": 9
                },
                {
                    "key_as_string": "2018-09-06T10:40:00.000+08:00",
                    "key": 1536201600000,
                    "doc_count": 9
                },
                {
                    "key_as_string": "2018-09-06T10:45:00.000+08:00",
                    "key": 1536201900000,
                    "doc_count": 10
                },
                {
                    "key_as_string": "2018-09-06T10:50:00.000+08:00",
                    "key": 1536202200000,
                    "doc_count": 8
                },
                {
                    "key_as_string": "2018-09-06T10:55:00.000+08:00",
                    "key": 1536202500000,
                    "doc_count": 10
                }
            ]
        }
    },
    "status": 200
}


shards = {
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_all": {
    "primaries": {
      "docs": {
        "count": 552091,
        "deleted": 0
      },
      "store": {
        "size_in_bytes": 202094919,
        "throttle_time_in_millis": 0
      },
      "indexing": {
        "index_total": 552091,
        "index_time_in_millis": 266911,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": False,
        "throttle_time_in_millis": 0
      },
      "get": {
        "total": 0,
        "time_in_millis": 0,
        "exists_total": 0,
        "exists_time_in_millis": 0,
        "missing_total": 0,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 32538,
        "query_time_in_millis": 527342,
        "query_current": 0,
        "fetch_total": 13155,
        "fetch_time_in_millis": 19784,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0
      },
      "merges": {
        "current": 0,
        "current_docs": 0,
        "current_size_in_bytes": 0,
        "total": 182,
        "total_time_in_millis": 135488,
        "total_docs": 2819240,
        "total_size_in_bytes": 1044373044,
        "total_stopped_time_in_millis": 0,
        "total_throttled_time_in_millis": 1253,
        "total_auto_throttle_in_bytes": 19065018
      },
      "refresh": {
        "total": 1657,
        "total_time_in_millis": 50422,
        "listeners": 0
      },
      "flush": {
        "total": 1,
        "total_time_in_millis": 266
      },
      "warmer": {
        "current": 0,
        "total": 1659,
        "total_time_in_millis": 474
      },
      "query_cache": {
        "memory_size_in_bytes": 5314240,
        "total_count": 397679,
        "hit_count": 172378,
        "miss_count": 225301,
        "cache_size": 1409,
        "cache_count": 5041,
        "evictions": 3632
      },
      "fielddata": {
        "memory_size_in_bytes": 119760,
        "evictions": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 12,
        "memory_in_bytes": 638348,
        "terms_memory_in_bytes": 375178,
        "stored_fields_memory_in_bytes": 87384,
        "term_vectors_memory_in_bytes": 0,
        "norms_memory_in_bytes": 768,
        "points_memory_in_bytes": 79742,
        "doc_values_memory_in_bytes": 95276,
        "index_writer_memory_in_bytes": 0,
        "version_map_memory_in_bytes": 0,
        "fixed_bit_set_memory_in_bytes": 0,
        "max_unsafe_auto_id_timestamp": -1,
        "file_sizes": {}
      },
      "translog": {
        "operations": 0,
        "size_in_bytes": 43
      },
      "request_cache": {
        "memory_size_in_bytes": 121313,
        "evictions": 0,
        "hit_count": 4143,
        "miss_count": 23083
      },
      "recovery": {
        "current_as_source": 0,
        "current_as_target": 0,
        "throttle_time_in_millis": 0
      }
    },
    "total": {
      "docs": {
        "count": 552091,
        "deleted": 0
      },
      "store": {
        "size_in_bytes": 202094919,
        "throttle_time_in_millis": 0
      },
      "indexing": {
        "index_total": 552091,
        "index_time_in_millis": 266911,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": False,
        "throttle_time_in_millis": 0
      },
      "get": {
        "total": 0,
        "time_in_millis": 0,
        "exists_total": 0,
        "exists_time_in_millis": 0,
        "missing_total": 0,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 32538,
        "query_time_in_millis": 527342,
        "query_current": 0,
        "fetch_total": 13155,
        "fetch_time_in_millis": 19784,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0
      },
      "merges": {
        "current": 0,
        "current_docs": 0,
        "current_size_in_bytes": 0,
        "total": 182,
        "total_time_in_millis": 135488,
        "total_docs": 2819240,
        "total_size_in_bytes": 1044373044,
        "total_stopped_time_in_millis": 0,
        "total_throttled_time_in_millis": 1253,
        "total_auto_throttle_in_bytes": 19065018
      },
      "refresh": {
        "total": 1657,
        "total_time_in_millis": 50422,
        "listeners": 0
      },
      "flush": {
        "total": 1,
        "total_time_in_millis": 266
      },
      "warmer": {
        "current": 0,
        "total": 1659,
        "total_time_in_millis": 474
      },
      "query_cache": {
        "memory_size_in_bytes": 5314240,
        "total_count": 397679,
        "hit_count": 172378,
        "miss_count": 225301,
        "cache_size": 1409,
        "cache_count": 5041,
        "evictions": 3632
      },
      "fielddata": {
        "memory_size_in_bytes": 119760,
        "evictions": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 12,
        "memory_in_bytes": 638348,
        "terms_memory_in_bytes": 375178,
        "stored_fields_memory_in_bytes": 87384,
        "term_vectors_memory_in_bytes": 0,
        "norms_memory_in_bytes": 768,
        "points_memory_in_bytes": 79742,
        "doc_values_memory_in_bytes": 95276,
        "index_writer_memory_in_bytes": 0,
        "version_map_memory_in_bytes": 0,
        "fixed_bit_set_memory_in_bytes": 0,
        "max_unsafe_auto_id_timestamp": -1,
        "file_sizes": {}
      },
      "translog": {
        "operations": 0,
        "size_in_bytes": 43
      },
      "request_cache": {
        "memory_size_in_bytes": 121313,
        "evictions": 0,
        "hit_count": 4143,
        "miss_count": 23083
      },
      "recovery": {
        "current_as_source": 0,
        "current_as_target": 0,
        "throttle_time_in_millis": 0
      }
    }
  },
  "indices": {
    "tcp-2018-09-06": {
      "primaries": {
        "docs": {
          "count": 552091,
          "deleted": 0
        },
        "store": {
          "size_in_bytes": 202094919,
          "throttle_time_in_millis": 0
        },
        "indexing": {
          "index_total": 552091,
          "index_time_in_millis": 266911,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": False,
          "throttle_time_in_millis": 0
        },
        "get": {
          "total": 0,
          "time_in_millis": 0,
          "exists_total": 0,
          "exists_time_in_millis": 0,
          "missing_total": 0,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 32538,
          "query_time_in_millis": 527342,
          "query_current": 0,
          "fetch_total": 13155,
          "fetch_time_in_millis": 19784,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0
        },
        "merges": {
          "current": 0,
          "current_docs": 0,
          "current_size_in_bytes": 0,
          "total": 182,
          "total_time_in_millis": 135488,
          "total_docs": 2819240,
          "total_size_in_bytes": 1044373044,
          "total_stopped_time_in_millis": 0,
          "total_throttled_time_in_millis": 1253,
          "total_auto_throttle_in_bytes": 19065018
        },
        "refresh": {
          "total": 1657,
          "total_time_in_millis": 50422,
          "listeners": 0
        },
        "flush": {
          "total": 1,
          "total_time_in_millis": 266
        },
        "warmer": {
          "current": 0,
          "total": 1659,
          "total_time_in_millis": 474
        },
        "query_cache": {
          "memory_size_in_bytes": 5314240,
          "total_count": 397679,
          "hit_count": 172378,
          "miss_count": 225301,
          "cache_size": 1409,
          "cache_count": 5041,
          "evictions": 3632
        },
        "fielddata": {
          "memory_size_in_bytes": 119760,
          "evictions": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 12,
          "memory_in_bytes": 638348,
          "terms_memory_in_bytes": 375178,
          "stored_fields_memory_in_bytes": 87384,
          "term_vectors_memory_in_bytes": 0,
          "norms_memory_in_bytes": 768,
          "points_memory_in_bytes": 79742,
          "doc_values_memory_in_bytes": 95276,
          "index_writer_memory_in_bytes": 0,
          "version_map_memory_in_bytes": 0,
          "fixed_bit_set_memory_in_bytes": 0,
          "max_unsafe_auto_id_timestamp": -1,
          "file_sizes": {}
        },
        "translog": {
          "operations": 0,
          "size_in_bytes": 43
        },
        "request_cache": {
          "memory_size_in_bytes": 121313,
          "evictions": 0,
          "hit_count": 4143,
          "miss_count": 23083
        },
        "recovery": {
          "current_as_source": 0,
          "current_as_target": 0,
          "throttle_time_in_millis": 0
        }
      },
      "total": {
        "docs": {
          "count": 552091,
          "deleted": 0
        },
        "store": {
          "size_in_bytes": 202094919,
          "throttle_time_in_millis": 0
        },
        "indexing": {
          "index_total": 552091,
          "index_time_in_millis": 266911,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": False,
          "throttle_time_in_millis": 0
        },
        "get": {
          "total": 0,
          "time_in_millis": 0,
          "exists_total": 0,
          "exists_time_in_millis": 0,
          "missing_total": 0,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 32538,
          "query_time_in_millis": 527342,
          "query_current": 0,
          "fetch_total": 13155,
          "fetch_time_in_millis": 19784,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0
        },
        "merges": {
          "current": 0,
          "current_docs": 0,
          "current_size_in_bytes": 0,
          "total": 182,
          "total_time_in_millis": 135488,
          "total_docs": 2819240,
          "total_size_in_bytes": 1044373044,
          "total_stopped_time_in_millis": 0,
          "total_throttled_time_in_millis": 1253,
          "total_auto_throttle_in_bytes": 19065018
        },
        "refresh": {
          "total": 1657,
          "total_time_in_millis": 50422,
          "listeners": 0
        },
        "flush": {
          "total": 1,
          "total_time_in_millis": 266
        },
        "warmer": {
          "current": 0,
          "total": 1659,
          "total_time_in_millis": 474
        },
        "query_cache": {
          "memory_size_in_bytes": 5314240,
          "total_count": 397679,
          "hit_count": 172378,
          "miss_count": 225301,
          "cache_size": 1409,
          "cache_count": 5041,
          "evictions": 3632
        },
        "fielddata": {
          "memory_size_in_bytes": 119760,
          "evictions": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 12,
          "memory_in_bytes": 638348,
          "terms_memory_in_bytes": 375178,
          "stored_fields_memory_in_bytes": 87384,
          "term_vectors_memory_in_bytes": 0,
          "norms_memory_in_bytes": 768,
          "points_memory_in_bytes": 79742,
          "doc_values_memory_in_bytes": 95276,
          "index_writer_memory_in_bytes": 0,
          "version_map_memory_in_bytes": 0,
          "fixed_bit_set_memory_in_bytes": 0,
          "max_unsafe_auto_id_timestamp": -1,
          "file_sizes": {}
        },
        "translog": {
          "operations": 0,
          "size_in_bytes": 43
        },
        "request_cache": {
          "memory_size_in_bytes": 121313,
          "evictions": 0,
          "hit_count": 4143,
          "miss_count": 23083
        },
        "recovery": {
          "current_as_source": 0,
          "current_as_target": 0,
          "throttle_time_in_millis": 0
        }
      }
    }
  }
}
shards2= {
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_all": {
    "primaries": {
      "docs": {
        "count": 552091,
        "deleted": 0
      },
      "store": {
        "size_in_bytes": 202094919,
        "throttle_time_in_millis": 0
      },
      "indexing": {
        "index_total": 552091,
        "index_time_in_millis": 266911,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": false,
        "throttle_time_in_millis": 0
      },
      "get": {
        "total": 0,
        "time_in_millis": 0,
        "exists_total": 0,
        "exists_time_in_millis": 0,
        "missing_total": 0,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 32538,
        "query_time_in_millis": 527342,
        "query_current": 0,
        "fetch_total": 13155,
        "fetch_time_in_millis": 19784,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0
      },
      "merges": {
        "current": 0,
        "current_docs": 0,
        "current_size_in_bytes": 0,
        "total": 182,
        "total_time_in_millis": 135488,
        "total_docs": 2819240,
        "total_size_in_bytes": 1044373044,
        "total_stopped_time_in_millis": 0,
        "total_throttled_time_in_millis": 1253,
        "total_auto_throttle_in_bytes": 19065018
      },
      "refresh": {
        "total": 1657,
        "total_time_in_millis": 50422,
        "listeners": 0
      },
      "flush": {
        "total": 1,
        "total_time_in_millis": 266
      },
      "warmer": {
        "current": 0,
        "total": 1659,
        "total_time_in_millis": 474
      },
      "query_cache": {
        "memory_size_in_bytes": 5314240,
        "total_count": 397679,
        "hit_count": 172378,
        "miss_count": 225301,
        "cache_size": 1409,
        "cache_count": 5041,
        "evictions": 3632
      },
      "fielddata": {
        "memory_size_in_bytes": 119760,
        "evictions": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 12,
        "memory_in_bytes": 638348,
        "terms_memory_in_bytes": 375178,
        "stored_fields_memory_in_bytes": 87384,
        "term_vectors_memory_in_bytes": 0,
        "norms_memory_in_bytes": 768,
        "points_memory_in_bytes": 79742,
        "doc_values_memory_in_bytes": 95276,
        "index_writer_memory_in_bytes": 0,
        "version_map_memory_in_bytes": 0,
        "fixed_bit_set_memory_in_bytes": 0,
        "max_unsafe_auto_id_timestamp": -1,
        "file_sizes": {}
      },
      "translog": {
        "operations": 0,
        "size_in_bytes": 43
      },
      "request_cache": {
        "memory_size_in_bytes": 121313,
        "evictions": 0,
        "hit_count": 4143,
        "miss_count": 23083
      },
      "recovery": {
        "current_as_source": 0,
        "current_as_target": 0,
        "throttle_time_in_millis": 0
      }
    },
    "total": {
      "docs": {
        "count": 552091,
        "deleted": 0
      },
      "store": {
        "size_in_bytes": 202094919,
        "throttle_time_in_millis": 0
      },
      "indexing": {
        "index_total": 552091,
        "index_time_in_millis": 266911,
        "index_current": 0,
        "index_failed": 0,
        "delete_total": 0,
        "delete_time_in_millis": 0,
        "delete_current": 0,
        "noop_update_total": 0,
        "is_throttled": false,
        "throttle_time_in_millis": 0
      },
      "get": {
        "total": 0,
        "time_in_millis": 0,
        "exists_total": 0,
        "exists_time_in_millis": 0,
        "missing_total": 0,
        "missing_time_in_millis": 0,
        "current": 0
      },
      "search": {
        "open_contexts": 0,
        "query_total": 32538,
        "query_time_in_millis": 527342,
        "query_current": 0,
        "fetch_total": 13155,
        "fetch_time_in_millis": 19784,
        "fetch_current": 0,
        "scroll_total": 0,
        "scroll_time_in_millis": 0,
        "scroll_current": 0,
        "suggest_total": 0,
        "suggest_time_in_millis": 0,
        "suggest_current": 0
      },
      "merges": {
        "current": 0,
        "current_docs": 0,
        "current_size_in_bytes": 0,
        "total": 182,
        "total_time_in_millis": 135488,
        "total_docs": 2819240,
        "total_size_in_bytes": 1044373044,
        "total_stopped_time_in_millis": 0,
        "total_throttled_time_in_millis": 1253,
        "total_auto_throttle_in_bytes": 19065018
      },
      "refresh": {
        "total": 1657,
        "total_time_in_millis": 50422,
        "listeners": 0
      },
      "flush": {
        "total": 1,
        "total_time_in_millis": 266
      },
      "warmer": {
        "current": 0,
        "total": 1659,
        "total_time_in_millis": 474
      },
      "query_cache": {
        "memory_size_in_bytes": 5314240,
        "total_count": 397679,
        "hit_count": 172378,
        "miss_count": 225301,
        "cache_size": 1409,
        "cache_count": 5041,
        "evictions": 3632
      },
      "fielddata": {
        "memory_size_in_bytes": 119760,
        "evictions": 0
      },
      "completion": {
        "size_in_bytes": 0
      },
      "segments": {
        "count": 12,
        "memory_in_bytes": 638348,
        "terms_memory_in_bytes": 375178,
        "stored_fields_memory_in_bytes": 87384,
        "term_vectors_memory_in_bytes": 0,
        "norms_memory_in_bytes": 768,
        "points_memory_in_bytes": 79742,
        "doc_values_memory_in_bytes": 95276,
        "index_writer_memory_in_bytes": 0,
        "version_map_memory_in_bytes": 0,
        "fixed_bit_set_memory_in_bytes": 0,
        "max_unsafe_auto_id_timestamp": -1,
        "file_sizes": {}
      },
      "translog": {
        "operations": 0,
        "size_in_bytes": 43
      },
      "request_cache": {
        "memory_size_in_bytes": 121313,
        "evictions": 0,
        "hit_count": 4143,
        "miss_count": 23083
      },
      "recovery": {
        "current_as_source": 0,
        "current_as_target": 0,
        "throttle_time_in_millis": 0
      }
    }
  },
  "indices": {
    "tcp-2018-09-06": {
      "primaries": {
        "docs": {
          "count": 552091,
          "deleted": 0
        },
        "store": {
          "size_in_bytes": 202094919,
          "throttle_time_in_millis": 0
        },
        "indexing": {
          "index_total": 552091,
          "index_time_in_millis": 266911,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": false,
          "throttle_time_in_millis": 0
        },
        "get": {
          "total": 0,
          "time_in_millis": 0,
          "exists_total": 0,
          "exists_time_in_millis": 0,
          "missing_total": 0,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 32538,
          "query_time_in_millis": 527342,
          "query_current": 0,
          "fetch_total": 13155,
          "fetch_time_in_millis": 19784,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0
        },
        "merges": {
          "current": 0,
          "current_docs": 0,
          "current_size_in_bytes": 0,
          "total": 182,
          "total_time_in_millis": 135488,
          "total_docs": 2819240,
          "total_size_in_bytes": 1044373044,
          "total_stopped_time_in_millis": 0,
          "total_throttled_time_in_millis": 1253,
          "total_auto_throttle_in_bytes": 19065018
        },
        "refresh": {
          "total": 1657,
          "total_time_in_millis": 50422,
          "listeners": 0
        },
        "flush": {
          "total": 1,
          "total_time_in_millis": 266
        },
        "warmer": {
          "current": 0,
          "total": 1659,
          "total_time_in_millis": 474
        },
        "query_cache": {
          "memory_size_in_bytes": 5314240,
          "total_count": 397679,
          "hit_count": 172378,
          "miss_count": 225301,
          "cache_size": 1409,
          "cache_count": 5041,
          "evictions": 3632
        },
        "fielddata": {
          "memory_size_in_bytes": 119760,
          "evictions": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 12,
          "memory_in_bytes": 638348,
          "terms_memory_in_bytes": 375178,
          "stored_fields_memory_in_bytes": 87384,
          "term_vectors_memory_in_bytes": 0,
          "norms_memory_in_bytes": 768,
          "points_memory_in_bytes": 79742,
          "doc_values_memory_in_bytes": 95276,
          "index_writer_memory_in_bytes": 0,
          "version_map_memory_in_bytes": 0,
          "fixed_bit_set_memory_in_bytes": 0,
          "max_unsafe_auto_id_timestamp": -1,
          "file_sizes": {}
        },
        "translog": {
          "operations": 0,
          "size_in_bytes": 43
        },
        "request_cache": {
          "memory_size_in_bytes": 121313,
          "evictions": 0,
          "hit_count": 4143,
          "miss_count": 23083
        },
        "recovery": {
          "current_as_source": 0,
          "current_as_target": 0,
          "throttle_time_in_millis": 0
        }
      },
      "total": {
        "docs": {
          "count": 552091,
          "deleted": 0
        },
        "store": {
          "size_in_bytes": 202094919,
          "throttle_time_in_millis": 0
        },
        "indexing": {
          "index_total": 552091,
          "index_time_in_millis": 266911,
          "index_current": 0,
          "index_failed": 0,
          "delete_total": 0,
          "delete_time_in_millis": 0,
          "delete_current": 0,
          "noop_update_total": 0,
          "is_throttled": false,
          "throttle_time_in_millis": 0
        },
        "get": {
          "total": 0,
          "time_in_millis": 0,
          "exists_total": 0,
          "exists_time_in_millis": 0,
          "missing_total": 0,
          "missing_time_in_millis": 0,
          "current": 0
        },
        "search": {
          "open_contexts": 0,
          "query_total": 32538,
          "query_time_in_millis": 527342,
          "query_current": 0,
          "fetch_total": 13155,
          "fetch_time_in_millis": 19784,
          "fetch_current": 0,
          "scroll_total": 0,
          "scroll_time_in_millis": 0,
          "scroll_current": 0,
          "suggest_total": 0,
          "suggest_time_in_millis": 0,
          "suggest_current": 0
        },
        "merges": {
          "current": 0,
          "current_docs": 0,
          "current_size_in_bytes": 0,
          "total": 182,
          "total_time_in_millis": 135488,
          "total_docs": 2819240,
          "total_size_in_bytes": 1044373044,
          "total_stopped_time_in_millis": 0,
          "total_throttled_time_in_millis": 1253,
          "total_auto_throttle_in_bytes": 19065018
        },
        "refresh": {
          "total": 1657,
          "total_time_in_millis": 50422,
          "listeners": 0
        },
        "flush": {
          "total": 1,
          "total_time_in_millis": 266
        },
        "warmer": {
          "current": 0,
          "total": 1659,
          "total_time_in_millis": 474
        },
        "query_cache": {
          "memory_size_in_bytes": 5314240,
          "total_count": 397679,
          "hit_count": 172378,
          "miss_count": 225301,
          "cache_size": 1409,
          "cache_count": 5041,
          "evictions": 3632
        },
        "fielddata": {
          "memory_size_in_bytes": 119760,
          "evictions": 0
        },
        "completion": {
          "size_in_bytes": 0
        },
        "segments": {
          "count": 12,
          "memory_in_bytes": 638348,
          "terms_memory_in_bytes": 375178,
          "stored_fields_memory_in_bytes": 87384,
          "term_vectors_memory_in_bytes": 0,
          "norms_memory_in_bytes": 768,
          "points_memory_in_bytes": 79742,
          "doc_values_memory_in_bytes": 95276,
          "index_writer_memory_in_bytes": 0,
          "version_map_memory_in_bytes": 0,
          "fixed_bit_set_memory_in_bytes": 0,
          "max_unsafe_auto_id_timestamp": -1,
          "file_sizes": {}
        },
        "translog": {
          "operations": 0,
          "size_in_bytes": 43
        },
        "request_cache": {
          "memory_size_in_bytes": 121313,
          "evictions": 0,
          "hit_count": 4143,
          "miss_count": 23083
        },
        "recovery": {
          "current_as_source": 0,
          "current_as_target": 0,
          "throttle_time_in_millis": 0
        }
      }
    }
  }
}
json_dns_answer=  {
    "took": 7,
    "timed_out": False,
    "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0
    },
    "hits": {
        "total": 1308,
        "max_score": 0,
        "hits": [ ]
    },
    "aggregations": {
        "2": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 1090,
            "buckets": [
                {
                    "key": "202.102.94.124",
                    "doc_count": 105
                },
                {
                    "key": "131.107.255.255",
                    "doc_count": 46
                },
                {
                    "key": "121.227.7.48",
                    "doc_count": 30
                },
                {
                    "key": "180.97.154.49",
                    "doc_count": 20
                },
                {
                    "key": "121.227.7.33",
                    "doc_count": 17
                }
            ]
        }
    },
    "status": 200
}
json_ustc = {
  "took": 3625,
  "timed_out": False,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "hits": {
    "total": 3213000,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 2862525,
      "buckets": [
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 244379,
            "buckets": [
              {
                "key": "45.119.99.35",
                "doc_count": 39677
              },
              {
                "key": "121.194.0.221",
                "doc_count": 10040
              }
            ]
          },
          "key": "210.45.123.127",
          "doc_count": 294096
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 56363,
            "buckets": [
              {
                "key": "114.214.161.6",
                "doc_count": 9
              },
              {
                "key": "114.214.215.211",
                "doc_count": 7
              }
            ]
          },
          "key": "146.185.222.61",
          "doc_count": 56379
        }
      ]
    }
  },
  "status": 200
}
# clean_result = json_date_histogram["aggregations"]['1-bucket']['buckets']
# shards_result = shards2['_all']['primaries']['store']['size_in_bytes']
# shards_docs = shards2['_all']['primaries']['docs']['count']
json_answer_question = {
  "took": 31,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "hits": {
    "total": 882,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 760,
      "buckets": [
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 55,
            "buckets": [
              {
                "key": "app.qyer.com",
                "doc_count": 5
              },
              {
                "key": "ask.qyer.com",
                "doc_count": 5
              }
            ]
          },
          "key": "211.155.80.56",
          "doc_count": 65
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 41,
            "buckets": [
              {
                "key": "wx1.sinaimg.cn",
                "doc_count": 8
              },
              {
                "key": "wx2.sinaimg.cn",
                "doc_count": 8
              }
            ]
          },
          "key": "202.102.94.124",
          "doc_count": 57
        }
      ]
    }
  },
  "status": 200
}


es = Elasticsearch(['192.168.10.102'], port=9200)

# clean_dns_result = json_answer_question['aggregations']['2']['buckets']
# tcp_list = []
# for dns_key in clean_dns_result:
#     dict = {}
#     question = dns_key['3']['buckets']
#     question_list = []
#     for q_key in question:
#         question_list.append(q_key['key'])
#     dict['answer'] = dns_key['key']
#     dict['question'] = question_list
#     tcp_list.append(dict)
# print tcp_list


json_check_disk = {
    "_shards": {
        "total": 20,
        "successful": 20,
        "failed": 0
    },
    "_all": {
        "primaries": {
            "docs": {
                "count": 86404485,
                "deleted": 0
            },
            "store": {
                "size_in_bytes": 35285323041,
                "throttle_time_in_millis": 0
            },
            "indexing": {
                "index_total": 0,
                "index_time_in_millis": 0,
                "index_current": 0,
                "index_failed": 0,
                "delete_total": 0,
                "delete_time_in_millis": 0,
                "delete_current": 0,
                "noop_update_total": 0,
                "is_throttled": false,
                "throttle_time_in_millis": 0
            },
            "get": {
                "total": 0,
                "time_in_millis": 0,
                "exists_total": 0,
                "exists_time_in_millis": 0,
                "missing_total": 0,
                "missing_time_in_millis": 0,
                "current": 0
            },
            "search": {
                "open_contexts": 0,
                "query_total": 117967,
                "query_time_in_millis": 4266334,
                "query_current": 0,
                "fetch_total": 0,
                "fetch_time_in_millis": 0,
                "fetch_current": 0,
                "scroll_total": 0,
                "scroll_time_in_millis": 0,
                "scroll_current": 0,
                "suggest_total": 0,
                "suggest_time_in_millis": 0,
                "suggest_current": 0
            },
            "merges": {
                "current": 0,
                "current_docs": 0,
                "current_size_in_bytes": 0,
                "total": 0,
                "total_time_in_millis": 0,
                "total_docs": 0,
                "total_size_in_bytes": 0,
                "total_stopped_time_in_millis": 0,
                "total_throttled_time_in_millis": 0,
                "total_auto_throttle_in_bytes": 209715200
            },
            "refresh": {
                "total": 9,
                "total_time_in_millis": 49,
                "listeners": 0
            },
            "flush": {
                "total": 9,
                "total_time_in_millis": 0
            },
            "warmer": {
                "current": 0,
                "total": 19,
                "total_time_in_millis": 8
            },
            "query_cache": {
                "memory_size_in_bytes": 166307808,
                "total_count": 642768,
                "hit_count": 279708,
                "miss_count": 363060,
                "cache_size": 9999,
                "cache_count": 14376,
                "evictions": 4377
            },
            "fielddata": {
                "memory_size_in_bytes": 45973192,
                "evictions": 0
            },
            "completion": {
                "size_in_bytes": 0
            },
            "segments": {
                "count": 277,
                "memory_in_bytes": 70499073,
                "terms_memory_in_bytes": 40857059,
                "stored_fields_memory_in_bytes": 12957832,
                "term_vectors_memory_in_bytes": 0,
                "norms_memory_in_bytes": 17728,
                "points_memory_in_bytes": 11828538,
                "doc_values_memory_in_bytes": 4837916,
                "index_writer_memory_in_bytes": 0,
                "version_map_memory_in_bytes": 0,
                "fixed_bit_set_memory_in_bytes": 0,
                "max_unsafe_auto_id_timestamp": -1,
                "file_sizes": { }
            },
            "translog": {
                "operations": 0,
                "size_in_bytes": 817
            },
            "request_cache": {
                "memory_size_in_bytes": 24818082,
                "evictions": 1272,
                "hit_count": 92602,
                "miss_count": 23929
            },
            "recovery": {
                "current_as_source": 0,
                "current_as_target": 0,
                "throttle_time_in_millis": 668313
            }
        },
        "total": {
            "docs": {
                "count": 172808970,
                "deleted": 0
            },
            "store": {
                "size_in_bytes": 70570646073,
                "throttle_time_in_millis": 0
            },
            "indexing": {
                "index_total": 0,
                "index_time_in_millis": 0,
                "index_current": 0,
                "index_failed": 0,
                "delete_total": 0,
                "delete_time_in_millis": 0,
                "delete_current": 0,
                "noop_update_total": 0,
                "is_throttled": false,
                "throttle_time_in_millis": 0
            },
            "get": {
                "total": 0,
                "time_in_millis": 0,
                "exists_total": 0,
                "exists_time_in_millis": 0,
                "missing_total": 0,
                "missing_time_in_millis": 0,
                "current": 0
            },
            "search": {
                "open_contexts": 0,
                "query_total": 233672,
                "query_time_in_millis": 6529008,
                "query_current": 0,
                "fetch_total": 0,
                "fetch_time_in_millis": 0,
                "fetch_current": 0,
                "scroll_total": 0,
                "scroll_time_in_millis": 0,
                "scroll_current": 0,
                "suggest_total": 0,
                "suggest_time_in_millis": 0,
                "suggest_current": 0
            },
            "merges": {
                "current": 0,
                "current_docs": 0,
                "current_size_in_bytes": 0,
                "total": 0,
                "total_time_in_millis": 0,
                "total_docs": 0,
                "total_size_in_bytes": 0,
                "total_stopped_time_in_millis": 0,
                "total_throttled_time_in_millis": 0,
                "total_auto_throttle_in_bytes": 419430400
            },
            "refresh": {
                "total": 9,
                "total_time_in_millis": 49,
                "listeners": 0
            },
            "flush": {
                "total": 9,
                "total_time_in_millis": 0
            },
            "warmer": {
                "current": 0,
                "total": 29,
                "total_time_in_millis": 8
            },
            "query_cache": {
                "memory_size_in_bytes": 270341272,
                "total_count": 1246008,
                "hit_count": 539520,
                "miss_count": 706488,
                "cache_size": 17366,
                "cache_count": 26114,
                "evictions": 8748
            },
            "fielddata": {
                "memory_size_in_bytes": 91940240,
                "evictions": 0
            },
            "completion": {
                "size_in_bytes": 0
            },
            "segments": {
                "count": 554,
                "memory_in_bytes": 140998146,
                "terms_memory_in_bytes": 81714118,
                "stored_fields_memory_in_bytes": 25915664,
                "term_vectors_memory_in_bytes": 0,
                "norms_memory_in_bytes": 35456,
                "points_memory_in_bytes": 23657076,
                "doc_values_memory_in_bytes": 9675832,
                "index_writer_memory_in_bytes": 0,
                "version_map_memory_in_bytes": 0,
                "fixed_bit_set_memory_in_bytes": 0,
                "max_unsafe_auto_id_timestamp": -1,
                "file_sizes": { }
            },
            "translog": {
                "operations": 0,
                "size_in_bytes": 1247
            },
            "request_cache": {
                "memory_size_in_bytes": 46438156,
                "evictions": 5155,
                "hit_count": 183446,
                "miss_count": 47786
            },
            "recovery": {
                "current_as_source": 0,
                "current_as_target": 0,
                "throttle_time_in_millis": 1305926
            }
        }
    },
    "indices": {
        "tcp-2018-09-01": {
            "primaries": {
                "docs": {
                    "count": 86404485,
                    "deleted": 0
                },
                "store": {
                    "size_in_bytes": 35285323041,
                    "throttle_time_in_millis": 0
                },
                "indexing": {
                    "index_total": 0,
                    "index_time_in_millis": 0,
                    "index_current": 0,
                    "index_failed": 0,
                    "delete_total": 0,
                    "delete_time_in_millis": 0,
                    "delete_current": 0,
                    "noop_update_total": 0,
                    "is_throttled": false,
                    "throttle_time_in_millis": 0
                },
                "get": {
                    "total": 0,
                    "time_in_millis": 0,
                    "exists_total": 0,
                    "exists_time_in_millis": 0,
                    "missing_total": 0,
                    "missing_time_in_millis": 0,
                    "current": 0
                },
                "search": {
                    "open_contexts": 0,
                    "query_total": 117967,
                    "query_time_in_millis": 4266334,
                    "query_current": 0,
                    "fetch_total": 0,
                    "fetch_time_in_millis": 0,
                    "fetch_current": 0,
                    "scroll_total": 0,
                    "scroll_time_in_millis": 0,
                    "scroll_current": 0,
                    "suggest_total": 0,
                    "suggest_time_in_millis": 0,
                    "suggest_current": 0
                },
                "merges": {
                    "current": 0,
                    "current_docs": 0,
                    "current_size_in_bytes": 0,
                    "total": 0,
                    "total_time_in_millis": 0,
                    "total_docs": 0,
                    "total_size_in_bytes": 0,
                    "total_stopped_time_in_millis": 0,
                    "total_throttled_time_in_millis": 0,
                    "total_auto_throttle_in_bytes": 209715200
                },
                "refresh": {
                    "total": 9,
                    "total_time_in_millis": 49,
                    "listeners": 0
                },
                "flush": {
                    "total": 9,
                    "total_time_in_millis": 0
                },
                "warmer": {
                    "current": 0,
                    "total": 19,
                    "total_time_in_millis": 8
                },
                "query_cache": {
                    "memory_size_in_bytes": 166307808,
                    "total_count": 642768,
                    "hit_count": 279708,
                    "miss_count": 363060,
                    "cache_size": 9999,
                    "cache_count": 14376,
                    "evictions": 4377
                },
                "fielddata": {
                    "memory_size_in_bytes": 45973192,
                    "evictions": 0
                },
                "completion": {
                    "size_in_bytes": 0
                },
                "segments": {
                    "count": 277,
                    "memory_in_bytes": 70499073,
                    "terms_memory_in_bytes": 40857059,
                    "stored_fields_memory_in_bytes": 12957832,
                    "term_vectors_memory_in_bytes": 0,
                    "norms_memory_in_bytes": 17728,
                    "points_memory_in_bytes": 11828538,
                    "doc_values_memory_in_bytes": 4837916,
                    "index_writer_memory_in_bytes": 0,
                    "version_map_memory_in_bytes": 0,
                    "fixed_bit_set_memory_in_bytes": 0,
                    "max_unsafe_auto_id_timestamp": -1,
                    "file_sizes": { }
                },
                "translog": {
                    "operations": 0,
                    "size_in_bytes": 817
                },
                "request_cache": {
                    "memory_size_in_bytes": 24818082,
                    "evictions": 1272,
                    "hit_count": 92602,
                    "miss_count": 23929
                },
                "recovery": {
                    "current_as_source": 0,
                    "current_as_target": 0,
                    "throttle_time_in_millis": 668313
                }
            },
            "total": {
                "docs": {
                    "count": 172808970,
                    "deleted": 0
                },
                "store": {
                    "size_in_bytes": 70570646073,
                    "throttle_time_in_millis": 0
                },
                "indexing": {
                    "index_total": 0,
                    "index_time_in_millis": 0,
                    "index_current": 0,
                    "index_failed": 0,
                    "delete_total": 0,
                    "delete_time_in_millis": 0,
                    "delete_current": 0,
                    "noop_update_total": 0,
                    "is_throttled": false,
                    "throttle_time_in_millis": 0
                },
                "get": {
                    "total": 0,
                    "time_in_millis": 0,
                    "exists_total": 0,
                    "exists_time_in_millis": 0,
                    "missing_total": 0,
                    "missing_time_in_millis": 0,
                    "current": 0
                },
                "search": {
                    "open_contexts": 0,
                    "query_total": 233672,
                    "query_time_in_millis": 6529008,
                    "query_current": 0,
                    "fetch_total": 0,
                    "fetch_time_in_millis": 0,
                    "fetch_current": 0,
                    "scroll_total": 0,
                    "scroll_time_in_millis": 0,
                    "scroll_current": 0,
                    "suggest_total": 0,
                    "suggest_time_in_millis": 0,
                    "suggest_current": 0
                },
                "merges": {
                    "current": 0,
                    "current_docs": 0,
                    "current_size_in_bytes": 0,
                    "total": 0,
                    "total_time_in_millis": 0,
                    "total_docs": 0,
                    "total_size_in_bytes": 0,
                    "total_stopped_time_in_millis": 0,
                    "total_throttled_time_in_millis": 0,
                    "total_auto_throttle_in_bytes": 419430400
                },
                "refresh": {
                    "total": 9,
                    "total_time_in_millis": 49,
                    "listeners": 0
                },
                "flush": {
                    "total": 9,
                    "total_time_in_millis": 0
                },
                "warmer": {
                    "current": 0,
                    "total": 29,
                    "total_time_in_millis": 8
                },
                "query_cache": {
                    "memory_size_in_bytes": 270341272,
                    "total_count": 1246008,
                    "hit_count": 539520,
                    "miss_count": 706488,
                    "cache_size": 17366,
                    "cache_count": 26114,
                    "evictions": 8748
                },
                "fielddata": {
                    "memory_size_in_bytes": 91940240,
                    "evictions": 0
                },
                "completion": {
                    "size_in_bytes": 0
                },
                "segments": {
                    "count": 554,
                    "memory_in_bytes": 140998146,
                    "terms_memory_in_bytes": 81714118,
                    "stored_fields_memory_in_bytes": 25915664,
                    "term_vectors_memory_in_bytes": 0,
                    "norms_memory_in_bytes": 35456,
                    "points_memory_in_bytes": 23657076,
                    "doc_values_memory_in_bytes": 9675832,
                    "index_writer_memory_in_bytes": 0,
                    "version_map_memory_in_bytes": 0,
                    "fixed_bit_set_memory_in_bytes": 0,
                    "max_unsafe_auto_id_timestamp": -1,
                    "file_sizes": { }
                },
                "translog": {
                    "operations": 0,
                    "size_in_bytes": 1247
                },
                "request_cache": {
                    "memory_size_in_bytes": 46438156,
                    "evictions": 5155,
                    "hit_count": 183446,
                    "miss_count": 47786
                },
                "recovery": {
                    "current_as_source": 0,
                    "current_as_target": 0,
                    "throttle_time_in_millis": 1305926
                }
            }
        }
    }
}
json_sip = {
  "took": 88,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "hits": {
    "total": 184541,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 129679,
      "buckets": [
        {
          "key": "23.92.24.244",
          "doc_count": 14206
        },
        {
          "key": "192.168.0.66",
          "doc_count": 7108
        },
        {
          "key": "180.97.33.107",
          "doc_count": 6119
        },
        {
          "key": "180.97.33.108",
          "doc_count": 4574
        },
        {
          "key": "74.125.204.113",
          "doc_count": 3865
        },
        {
          "key": "74.125.204.101",
          "doc_count": 3849
        },
        {
          "key": "74.125.204.138",
          "doc_count": 3847
        },
        {
          "key": "74.125.204.102",
          "doc_count": 3776
        },
        {
          "key": "74.125.204.139",
          "doc_count": 3764
        },
        {
          "key": "74.125.204.100",
          "doc_count": 3754
        }
      ]
    }
  },
  "status": 200
}
json_sip_dip = {
  "took": 240,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "failed": 0
  },
  "hits": {
    "total": 1493663,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 4226,
      "sum_other_doc_count": 550449,
      "buckets": [
        {
          "3": {
            "doc_count_error_upper_bound": 2886,
            "sum_other_doc_count": 367438,
            "buckets": [
              {
                "key": "202.102.94.125",
                "doc_count": 7745
              },
              {
                "key": "180.97.245.254",
                "doc_count": 6583
              },
              {
                "key": "180.97.245.253",
                "doc_count": 6543
              },
              {
                "key": "188.172.219.132",
                "doc_count": 4465
              },
              {
                "key": "180.97.33.107",
                "doc_count": 3719
              }
            ]
          },
          "key": "192.168.4.100",
          "doc_count": 396493
        },
        {
          "3": {
            "doc_count_error_upper_bound": 1801,
            "sum_other_doc_count": 281838,
            "buckets": [
              {
                "key": "180.97.33.107",
                "doc_count": 10874
              },
              {
                "key": "180.97.33.108",
                "doc_count": 4578
              },
              {
                "key": "101.226.211.101",
                "doc_count": 2276
              },
              {
                "key": "61.129.248.209",
                "doc_count": 2154
              },
              {
                "key": "223.252.199.69",
                "doc_count": 1581
              }
            ]
          },
          "key": "192.168.3.100",
          "doc_count": 303301
        },
        {
          "3": {
            "doc_count_error_upper_bound": 212,
            "sum_other_doc_count": 20066,
            "buckets": [
              {
                "key": "8.8.8.8",
                "doc_count": 22686
              },
              {
                "key": "114.114.114.114",
                "doc_count": 22660
              },
              {
                "key": "221.13.30.242",
                "doc_count": 22606
              },
              {
                "key": "45.33.52.101",
                "doc_count": 2671
              },
              {
                "key": "121.156.123.249",
                "doc_count": 2573
              }
            ]
          },
          "key": "192.168.0.201",
          "doc_count": 93262
        },
        {
          "3": {
            "doc_count_error_upper_bound": 1184,
            "sum_other_doc_count": 58964,
            "buckets": [
              {
                "key": "180.97.33.107",
                "doc_count": 8040
              },
              {
                "key": "180.97.33.108",
                "doc_count": 7509
              },
              {
                "key": "74.125.204.101",
                "doc_count": 3470
              },
              {
                "key": "74.125.204.100",
                "doc_count": 3468
              },
              {
                "key": "74.125.204.102",
                "doc_count": 3466
              }
            ]
          },
          "key": "192.168.1.17",
          "doc_count": 84917
        },
        {
          "3": {
            "doc_count_error_upper_bound": 1072,
            "sum_other_doc_count": 49795,
            "buckets": [
              {
                "key": "74.125.204.138",
                "doc_count": 3152
              },
              {
                "key": "74.125.204.102",
                "doc_count": 3090
              },
              {
                "key": "74.125.204.101",
                "doc_count": 3081
              },
              {
                "key": "74.125.204.139",
                "doc_count": 3067
              },
              {
                "key": "74.125.204.100",
                "doc_count": 3056
              }
            ]
          },
          "key": "192.168.1.58",
          "doc_count": 65241
        }
      ]
    }
  },
  "status": 200
}

json_http = {
  "took": 25,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "hits": {
    "total": 3738,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 352,
      "buckets": [
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 333,
            "buckets": [
              {
                "key": "minigame.qq.com/appdir/avatar/element/76.zip",
                "doc_count": 1745
              },
              {
                "key": "dldir3.qq.com/minigamefile/face/30126.7z",
                "doc_count": 35
              },
              {
                "key": "dldir3.qq.com/minigamefile/face/30036.7z",
                "doc_count": 34
              },
              {
                "key": "get.sogou.com/q",
                "doc_count": 15
              },
              {
                "key": "180.96.2.71/download",
                "doc_count": 14
              }
            ]
          },
          "key": "192.168.3.100",
          "doc_count": 2176
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 397,
            "buckets": [
              {
                "key": "cntr.wps.cn/flow",
                "doc_count": 25
              },
              {
                "key": "helpdubaclient.ksmobile.com/nep/v1/",
                "doc_count": 14
              },
              {
                "key": "117.48.124.186/query3",
                "doc_count": 10
              },
              {
                "key": "120.52.183.150/",
                "doc_count": 8
              },
              {
                "key": "122.193.207.52/",
                "doc_count": 8
              }
            ]
          },
          "key": "192.168.4.100",
          "doc_count": 462
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 208,
            "buckets": [
              {
                "key": "192.168.0.118:5602/ui/favicons/favicon-32x32.png",
                "doc_count": 36
              },
              {
                "key": "192.168.0.118:5602/ui/favicons/favicon-16x16.png",
                "doc_count": 29
              },
              {
                "key": "180.96.2.51/download",
                "doc_count": 26
              },
              {
                "key": "192.168.0.118:5602/es_admin/_mget",
                "doc_count": 26
              },
              {
                "key": "192.168.0.118:5601/ui/favicons/favicon-32x32.png",
                "doc_count": 22
              }
            ]
          },
          "key": "192.168.1.18",
          "doc_count": 347
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 92,
            "buckets": [
              {
                "key": "23.92.24.244:5608/ui/favicons/favicon-32x32.png",
                "doc_count": 48
              },
              {
                "key": "23.92.24.244:5608/ui/favicons/favicon-16x16.png",
                "doc_count": 46
              },
              {
                "key": "23.92.24.244:5608/es_admin/_mget",
                "doc_count": 41
              },
              {
                "key": "23.92.24.244:5608/elasticsearch/_msearch",
                "doc_count": 30
              },
              {
                "key": "23.92.24.244:5608/elasticsearch/.dashboardgroup/dashboardgroup/_search",
                "doc_count": 15
              }
            ]
          },
          "key": "192.168.1.15",
          "doc_count": 272
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 122,
            "buckets": [
              {
                "key": "qd-update.qq.com:8080/",
                "doc_count": 2
              },
              {
                "key": "www.eclipse.org/downloads/download.php",
                "doc_count": 2
              },
              {
                "key": "101.110.118.66/ftp.yz.yamagata-u.ac.jp/pub/eclipse/releases/oxygen/201804111000/plugins/org.eclipse.cdt.core.native_5.10.0.201802261533.jar.pack.gz",
                "doc_count": 1
              },
              {
                "key": "101.110.118.70/ftp.yz.yamagata-u.ac.jp/pub/eclipse/releases/oxygen/201804111000/features/org.eclipse.cdt.native_9.4.3.201802261533.jar",
                "doc_count": 1
              },
              {
                "key": "113.96.231.11:443/",
                "doc_count": 1
              }
            ]
          },
          "key": "192.168.1.14",
          "doc_count": 129
        }
      ]
    }
  },
  "status": 200
}
pot1 = time.clock()

pattern2 = re.compile(r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))")
pattern = re.compile(r"^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")

clear_result = json_http['aggregations']['2']['buckets']
http_list = []
url_list = []
for ket in clear_result:
    #print ket
    sip = ket['key']
    for key in ket['3']['buckets']:
        dict = {}
        url = key['key']
        if(pattern2.findall(url)):
            dict['sip'] = sip
            dict['url'] = url
            url_list.append(dict)

for key in url_list:
    print key



# sip_list = []
# for sip_key in clear_result:
#     sip_list.append(sip_key['key'])
# print sip_list

# cmd = 'curl -X GET \"192.168.0.122:9222/tcp-2018-09-01/_stats\"'
# result = eval(os.popen(cmd).read())
# clear_search = result['_all']['total']['store']['size_in_bytes']
# print clear_search
# def host_check(index,gte,lte):
#     search_option= {
#     "size": 0,
#     "query": {
#         "bool": {
#             "must": [
#                 {
#                     "query_string": {
#                         "query": "*",
#                         "analyze_wildcard": True
#                     }
#                 },
#                 {
#                     "range": {
#                         "@timestamp": {
#                             "gte": gte,
#                             "lte": lte,
#                             "format": "epoch_millis"
#                         }
#                     }
#                 }
#             ],
#             "must_not": [ ]
#         }
#     },
#     "_source": {
#         "excludes": [ ]
#     },
#     "aggs": {
#         "2": {
#             "terms": {
#                 "field": "answer",
#                 "size": 100,
#                 "order": {
#                     "_count": "desc"
#                 }
#             },
#             "aggs": {
#                 "3": {
#                     "terms": {
#                         "field": "question",
#                         "size": 100,
#                         "order": {
#                             "_count": "desc"
#                         }
#                     }
#                 }
#             }
#         }
#     }
# }
#     result = es.search(index=index,body=search_option)
#     clean_dns_result = result['aggregations']['2']['buckets']
#     answer_list = []
#     for dns_key in clean_dns_result:
#         dict = {}
#         question = dns_key['3']['buckets']
#         question_list = []
#         for q_key in question:
#             question_list.append(q_key['key'])
#         if (re.match(r"^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))",dns_key['key'])):
#             dict['answer'] = dns_key['key']
#             dict['question'] = question_list
#             answer_list.append(dict)
#     return answer_list
#
# def es_check():
#     search_option = 'GET /_cat/allocation?v'
#     result = es.search(body=search_option)
#     return result
#
#
# index = 'dns-2018-09-10'
# # anwser_list = host_check(index=index,gte=1536026100000,lte=1536026340000)
# # for key in anwser_list:
# #     print key
# # print (len(anwser_list))
#
# print (es_check())
pot2 = time.clock()
print (pot2 - pot1)
