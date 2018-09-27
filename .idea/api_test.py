# -*- coding: utf-8 -*-
import paramiko
import os,time
import commands
import logging

list_file_content = []


logging.basicConfig(level = logging.INFO,
                    format   = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt  = '%a, %d %b %Y %H:%M:%S',
                    filename = 'getip.log',#日志目录
                    filemode = 'a')

def ssh_conn(host,old_ip,domain_ip):
	#print(host)
	ssh = paramiko.SSHClient()  # 创建ssh对象
	# 允许连接不在know_hosts文件中的主机
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# 连接服务器

	ssh.connect(hostname=host, port=3722, username='getip', password='5LqR5Yip5p2l')
	# 执行追加文件内容命令
	#echo_cmd = "echo \'" + domain_ip + "\' > /usr/getip/groupIP.conf"
	conf_cmd = "sed -i \'s/" + old_ip + "/"+ domain_ip + "/\' logtest2.conf"
	print conf_cmd
	stdin, stdout, stderr = ssh.exec_command(conf_cmd)

	# 修改zabbix agent内容
	# stdin, stdout, stderr = ssh.exec_command \
	# 	("sed -i 's/^Server=[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*/Server=33.66.88.99/g' /etc/zabbix/zabbix_agentd.conf")

	ssh.close()
	print ('done')


class changeip():
	def __init__(self):
		self.last_ip = '192.168.10.65'

	def run(self):
		#host = '192.168.10.92'
		host = '23.92.24.244'

		cmd = 'curl ifconfig.co -s'
		domain_ip = os.popen(cmd).read().split()[0]
		if domain_ip == self.last_ip:
			logging.info('has not changed')
			print (self.last_ip)
		else:
			try:
				print domain_ip
				ssh_conn(host, self.last_ip, domain_ip)
				logging.info("es_ip changed")
			except Exception, e:
				logging.error(e)
				print (e)
				return
			self.last_ip = domain_ip
			logging.info('changed')
			logging.info(domain_ip)
		time.sleep(300)
		return

if __name__ == '__main__':
	ip = changeip()
	while (True):
		ip.run()