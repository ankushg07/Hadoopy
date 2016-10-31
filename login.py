#! /usr/bin/python

import time import os 
import sys
import commands

#welcome box

os.system("dialog --infobox 'Welcome to Hadoopy' 10 30 ")
time.sleep(2)

#Login module

pwd = os.path.dirname("_file_")

unm_path = os.path.join(pwd,"temp/uname.txt")
pas_path = os.path.join(pwd,"temp/pas.txt")

os.system("dialog --inputbox 'Please enter the Username' 20 40 2> "+str(unm_path) )
os.system("dialog --passwordbox 'Please enter the password' 20 40 2> " +str(pas_path) )

#Verification

f1=open( unm_path ,'r')
un=f1.read()
f1.close()
f2=open(pas_path ,'r')
pas=f2.read()
f2.close()
if(un.strip()!="admin" or pas.strip()!="admin"):
	os.system("dialog --msgbox 'Wrong Credentials !!' 20 40 ")
	#Exiting if Failed
	sys.exit()

menu_path=os.path.join(pwd,"menu.py")
execfile(menu_path)
	


