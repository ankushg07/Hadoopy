#! /usr/bin/python

import os
import commands
import sys
import time

pwd = os.path.dirname("_file_")
choice = os.path.join(pwd,"temp/choice.txt")

option = 0
while(True):
	os.system("dialog --radiolist 'Type of operation ' 20 40 3 1 'File Upload' on 2 'Job Run' off 3 'Exit' off  2> " +str(choice) )
	f1=open(choice,'r')
	option=f1.read()
	f1.close()
	if(option == '1'):
		#file uplaod
		os.system("dialog --inputbox 'enter the name of file' 20 40 2> " +str(choice) )
		f1=open(choice,'r')
		fname=f1.read()
		f1.close()
		fname=fname.strip()
		fput="hadoop fs -put "+fname+" /"
		os.system(fput)
		
	elif(option == '2'):
		#job run
		os.system("dialog --inputbox 'enter the name of file for job' 20 40 2> " +str(choice) )
		f1=open(choice,'r')
		fname=f1.read()
		f1.close()
		fname=fname.strip()
		
		wcnt="hadoop jar /usr/share/hadoop/hadoop-examples-1.2.1.jar wordcount /"+fname+" /output"
		os.system(wcnt)		
	else:
		break;


