#! /usr/bin/python

import commands , os
import sys
import time


pwd = os.path.dirname("_file_")
choice = os.path.join(pwd,"temp/choice.txt")

os.system("dialog --radiolist 'Choose the opeartion ' 20 40 2 1 'deplyment' on 2 'operations' off  2> "+str(choice) )
f1=open(choice,'r')
ch=f1.read()
f1.close()
if(ch=='1'):
	os.system("dialog --radiolist 'Choose mode for cluster deployment ' 20 40 2 1 'Manual' on 2 'Automatic' off  2> " +str(choice) )
	f1=open(choice,'r')
	ch=f1.read()
	f1.close()
	ipscan=os.path.join(pwd,"network_config/ip_scan.py")
	if(ch.strip() == '1'):
		exec file(ipscan)
	
else:
	job=os.path.join(pwd,"job/job.py")
	exec file(job)

