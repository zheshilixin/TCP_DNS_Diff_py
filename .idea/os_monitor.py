# -*- coding: utf-8 -*-
import psutil
import time
import winsound

disk = psutil.disk_partitions()
for i in disk:
    print "磁盘：%s   分区格式:%s"%(i.device,i.fstype)
    disk_use = psutil.disk_usage(i.device)
    print "使用了：%sM,空闲：%sM,总共：%sM,使用率\033[1;31;42m%s%%\033[0m,"%(disk_use.used/1024/1024,disk_use.free/1024/1024,disk_use.total/1024/1024,disk_use.percent)

memory = psutil.virtual_memory()
print ("mem used:  %s ,mem total: %s"%(memory.used,memory.total))
ab = float(memory.used)/float(memory.total)*100
print "%.2f%%"%ab
print psutil.swap_memory()

count = psutil.net_io_counters()
print "发送字节数：\033[1;31;42m%s\033[0mbytes,接收字节数：\033[1;31;42m%s\033[0mbytes,发送包数：%s,接收包数%s"%(count.bytes_sent,count.bytes_recv,count.packets_sent,count.packets_recv)

users = psutil.users()
print "当前登录用户：",users[0].name
#时间
curent_time = psutil.boot_time()

# pid = psutil.pids()
# for k, i in enumerate(pid):
#     try:
#         proc = psutil.Process(i)
#         print k, i, "%.2f%%" % (proc.memory_percent()), "%", proc.name(), proc.exe()
#
#     except psutil.AccessDenied:
#         print "psutil.AccessDenied"
#
# curent_time_1 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(curent_time))
# print curent_time_1

def cpu():
    while True:
        time.sleep(1)
        cpu_liyonglv = psutil.cpu_percent()
        print "当前cpu利用率：\033[1;31;42m%s%%\033[0m"%cpu_liyonglv
        if cpu_liyonglv >15.0:
            baojing()
def baojing():
    i = 0
    while i < 10 :
        i += 1
        time.sleep(0.5)
        winsound.PlaySound("ALARM8",winsound.SND_ALIAS)
#cpu()

print "done"
a =  psutil.disk_usage('/')
print a
disk  = {}
disk['total'] = round(a[0]/1073741824.0,3)
disk['used']  = round(a[1]/1073741824.0,3)
disk['free']  = round(a[2]/1073741824.0,3)
disk['percent'] = a[3]
print disk

b = psutil.disk_partitions()
disk = []
for key in b:
    c = psutil.disk_usage(key.device)
    disk_key = {}
    disk_key['total'] = round(c[0] / 1073741824.0, 3)
    disk_key['used'] = round(c[1] / 1073741824.0, 3)
    disk_key['free'] = round(c[2] / 1073741824.0, 3)
    disk_key['percent'] = c[3]
    disk.append(disk_key)
for key in disk:
    print key
#es直接获取es信息
#curl -X GET "192.168.0.122:9222/_cat/nodes?v&h=host,heap.current,heap.percent,heap.max,ram.max,disk.avail,node.role,m"

#curl -X GET "10.38.64.55:9200//_cat/nodes?v"

#curl" -X GET "10.38.64.55:9200/_cat/allocation?v&