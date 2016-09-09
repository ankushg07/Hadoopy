#! usr/bin/python
import sys
import time
import os
import commands


def firewall(ip):
	iptable="sshpass -p "+str(scp_pass)+ " ssh root@"+str(ip)+ " 'iptables -F' "
	os.system(iptable)
	setenforce="sshpass -p "+str(scp_pass)+ " ssh root@"+str(x)+ " 'setenforce 0' "
	os.system(setenforce)


cwd=os.getcwd()
#os.chdir("..")
pwd=os.getcwd()
inp=os.path.join(pwd,"temp/ip.txt")
os.system("dialog --inputbox 'Enter the range of IP to be searched in form a.b.c.x-y  ' 20 40 2> "+str(inp))
f1=open(inp)
IPrange=f1.read()
f1.close()
#IPrange='192.168.1.1-80'
cmd = "nmap -sP "+str(IPrange) + " -n |grep 'Nmap scan' |cut -d ' ' -f5"
ip=commands.getstatusoutput(cmd)
ips=[]
ips=ip[1].split("\n")



#securing the password for ssh and scp
os.system("dialog --passwordbox 'Please enter the common password for the connected system' 20 40 2> "+str(inp))
f1=open(inp)
scp_pass=f1.read()
scp_pass=scp_pass.strip()
f1.close()
scp_pass="ankush"
#Setting up IP in string for dialog box input
s=" "
x=1
button='on '
for i in ips:
	s=s+str(x)
	s+=" '"
	s+=str(i)
	s+="' "
	s+=button
	button = "off "	
	x+=1
	



#	***	Name Node	*** 

os.system("dialog --infobox 'Please select IP for the Name node' 20 40")
time.sleep(2)
os.system("dialog --radiolist 'Name node' 20 40 "+str(len(ips)) +s +" 2> "+str(inp)) 
f1=open(inp)
ch_nn=f1.read()
f1.close()
ch_nn=ch_nn.strip()

#as indexing is 0 based

ch_nn=int(ch_nn)-1

#nn has ip of system to be set as name node

nn=ips[ch_nn]

#configuring the files
core=os.path.join(pwd,"hdfs/core-site.xml")
f1=open(core,'w')
f1.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>')
f1.write("\n\n\n<configuration>\n")
f1.write("<property>\n")
f1.write("<name>fs.default.name</name>\n")
f1.write("<value>hdfs://" +str(nn)+ ":9001</value>\n")
f1.write("</property>\n")
f1.write("</configuration>\n")
f1.close()

#sharing the file to respective system

firewall(nn)
core_share='sshpass -p '+str(scp_pass)+' scp '+str(core)+ ' root@'+str(nn)+ ':/etc/hadoop/'
os.system(core_share)
hdfs=os.path.join(pwd,'hdfs/name_node/hdfs-site.xml')

sh_hdfs='sshpass -p '+str(scp_pass)+' scp '+str(hdfs)+ ' root@'+str(nn)+ ':/etc/hadoop/'
os.system(sh_hdfs)


#starting the service

#echo y for if it asked for permisions 

nn_format="sshpass -p "+str(scp_pass)+ " ssh root@"+str(nn)+ " 'echo y | hadoop namenode -format' "
os.system(nn_format)
nn_service="sshpass -p "+str(scp_pass)+ " ssh root@"+str(nn)+ " 'hadoop-daemon.sh start namenode ' "
os.system(nn_service)


#	*** 	Job Tracker  ****


os.system("dialog --infobox 'Please select IP for Job Tracker ' 20 40")
time.sleep(2)
os.system("dialog --radiolist 'Job Tracker ' 20 40 " + str(len(ips)) + s + "2>"+str(inp) )
f1=open(inp)
ch_jt=f1.read()
f1.close()
ch_jt=ch_jt.strip()
ch_jt=int( ch_jt )-1
jt=ips[ch_jt]


mapred=os.path.join(pwd,"mapreduce/mapred-site.xml")
f1=open(mapred,'w')
f1.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>')
f1.write("\n<configuration>\n")
f1.write("<property>\n")
f1.write("<name>mapred.job.tracker</name>\n")
f1.write("<value>" +str(jt)+ ":9002</value>\n")
f1.write("</property>\n")
f1.write("</configuration>\n")
f1.close()

#sharing the files 
firewall(jt)
sh_mr='sshpass -p '+str(scp_pass)+' scp '+str(mapred)+ ' root@'+str(jt)+ ':/etc/hadoop/'
os.system(sh_mr)

core_share='sshpass -p '+str(scp_pass)+' scp '+str(core)+ ' root@'+str(jt)+ ':/etc/hadoop/'
os.system(core_share)


#starting the JT service

jt_service="sshpass -p "+str(scp_pass)+ " ssh root@"+str(jt)+ " 'hadoop-daemon.sh start jobtracker' "
os.system(jt_service)



#	***	Clent Configuration	***

#getting the client IP
os.system("dialog --inputbox 'Enter the IP of client ' 20 40 2>"+str(inp))
f1=open(inp)
client=f1.read()
f1.close()
client=client.strip()
#client="192.168.43.55"
#Sharing the config files
core_share='sshpass -p '+str(scp_pass)+' scp '+str(core)+ ' root@'+str(client)+ ':/etc/hadoop/'
os.system(core_share)

sh_mr='sshpass -p '+str(scp_pass)+' scp '+str(mapred)+ ' root@'+str(client)+ ':/etc/hadoop/'
os.system(sh_mr)
firewall(client)

#	***	Data Node 	***

os.system("dialog --infobox 'Please select IP for Data Node ' 20 40")
time.sleep(2)
os.system("dialog --checklist 'Data Node ' 20 40 " + str(len(ips)) + s + "2>"+str(inp) )
f1=open(inp)
ch_dn=f1.read()
f1.close()
dn=[]
dn=ch_dn.split(" ")

for x in dn:
	#sharing the files 
	ch_dn=int( x )-1
	firewall(ips[ ch_dn ])
	
	core_share='sshpass -p '+str(scp_pass)+' scp '+str(core)+ ' root@'+str(ips[ ch_dn] )+ ':/etc/hadoop/'

	os.system(core_share)
	hdfs1=os.path.join(pwd,'hdfs/data_node/hdfs-site.xml')

	sh_hdfs='sshpass -p '+str(scp_pass)+' scp '+str(hdfs1)+ ' root@'+str(ips[ ch_dn ])+ ':/etc/hadoop/'
	os.system(sh_hdfs)


	#starting the service

	
	dn_service="sshpass -p "+str(scp_pass)+ " ssh root@"+str(ips[ ch_dn ])+ " 'hadoop-daemon.sh start datanode ' "
	os.system(dn_service)

	




#	*** 	Task Tracker	 ***
os.system("dialog --infobox 'Please select IP for Task Tracker ' 20 40")
time.sleep(2)
os.system("dialog --checklist 'Task Tracker ' 20 40 " + str(len(ips)) + s + "2>"+str(inp) )
f1=open(inp)
ch_tt=f1.read()
f1.close()
tt=[]
tt=ch_tt.split(" ")

for x in tt:	

	ch_tt=int( x )-1
	#sharing the files 
	firewall(ips[ ch_tt ])
	sh_mr='sshpass -p '+str(scp_pass)+' scp '+str(mapred)+ ' root@'+str(ips[ ch_tt ])+ ':/etc/hadoop/'
	os.system(sh_mr)

	
	#starting the TT service

	tt_service="sshpass -p "+str(scp_pass)+ " ssh root@"+str(ips[  ch_tt ])+ " 'hadoop-daemon.sh start tasktracker' "
	os.system(tt_service)



job=os.path.join(pwd,"job/job.py")
execfile(job)

