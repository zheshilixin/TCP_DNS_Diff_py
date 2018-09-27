import commands
import os
import time
false = False
pot1 = time.clock()
index = ['tcp','udp','http','dns','link','traffic','status','alert']
# ip_net = raw_input("input the es ip")
# ip_port = raw_input("input the es dport")
ip_net = '192.168.0.122'
ip_port = '9222'
index_inform = []
for index_key in index:
    for i in range(1,7):
        try:
            n = str(i).zfill(2)
            all_index = index_key + "-2018-09-" + n
            cmd = 'curl -X GET \"' + ip_net + ':' + ip_port +'/' + all_index + '/_stats' +'\"'
            print cmd
            result = os.popen(cmd)
            output = eval(result.read())
            #print output
            shards_size = output['_all']['primaries']['store']['size_in_bytes']
            shards_docs = output['_all']['primaries']['docs']['count']
            used_size   = output['_all']['total']['store']['size_in_bytes']
            dict = {}
            dict['index'] = all_index
            dict['size'] = str(round(shards_size/1073741824.0,3))+" GB"
            dict['disk_size'] = str(round(used_size/1073741824.0,3)) +' GB'
            dict['docs'] = shards_docs
            index_inform.append(dict)
        except:
            print "null"
pot6 = time.clock()
for index_key in index_inform:
    print index_key
print (pot6-pot1)

# cmd = 'curl -X GET \"23.92.24.244:9200/tcp-2018-09-04/_stats\"'
#
# result = os.popen(cmd)
# res = eval(result.read())
# print res['_all']['primaries']['store']['size_in_bytes']
# print res['_all']['primaries']['docs']['count']

# cmd_get_storage = "df -h"
# result = os.popen(cmd_get_storage)
# output = commands.getstatusoutput(cmd_get_storage)
# print output

