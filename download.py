import http.client    #module used for downloading files
import del1  # a user definde python file which deletes all the files from the destination directory where the files are downloaded
import threading
import progressbar
import multiprocessing 
import urllib.request
import time
import os
import ssl
def down(i,t_end,con,s_ip,file_name):  #function for downloading files from server
    num = 0
    while time.time()<t_end:
        try:
            con[i].request("GET","/"+file_name)
            r1 = con[i].getresponse()
        except http.client.RemoteDisconnected as e:
            print(str(e)+"for thread"+str(i))
        data1 = r1.read()
        handle = open('/home/client1/test/try'+str(num)+str(i)+'.txt','wb')
        handle.write(data1)
        handle.close()
        num+=1
	#print("number of files downloaded for user"+str(i)+"="+str(num))
        con[i].close()
	
		


def count(size,t):   #function for calculating throughput
    no=len([1 for x in list(os.scandir('/home/client1/test')) if x.is_file()])
    through=(no*(size)/int(t))
    through=through/(1024*1024)
    through=round(through,4)
    return no,through

def progress(n,tim):     #function to display progressbar
    bar = progressbar.ProgressBar()
    for j in bar(range(100)): 
    	time.sleep(int(tim)/100)
	   		
if __name__=='__main__': 
    t=input('enter time in seconds\t')
    ip=input('enter server ip address (default value:192.168.12.65)\t')
    n=input('enter no of users (default value:1)\t')
    file_name=input('Enter the file name (default value:try.txt)\t')
    pr=input('enter protocol (default value:http)\t')
    if t=='':
        t=2
    if ip=='':
        ip='192.168.12.65'
    if file_name=='':
        file_name='try.txt'
    if pr=='':
        pr='http'
    if n=='':
        n=1
    s_ip = dict()
    con = dict()
    size = 0
    link ="http://"+ip+"/"+file_name
    site = urllib.request.urlopen(link)
    procs = []
    size = site.length    #to find the size of the file being downloaded
    print("file size:"+str(size))
    p1=multiprocessing.Process(target=progress,args=(n,t))
    p1.start()	
    time.sleep(2)
    for i in range(6,6+int(n)): #creates one IP address for each user
        s_ip[i-6]='192.168.177.'+str(i)
        os.system('sudo ip address add '+s_ip[i-6]+'/24 dev ens33')
    t_end = time.time()+float(t)
    if pr=='http':
        for i in range(int(n)):  #creates a HTTP connection from each user to the server
            con[i] = http.client.HTTPConnection(ip,source_address=(s_ip[i],80))
    else:
        context = ssl._create_unverified_context()   #does not verify the certificate as it is self-signed 
        for i in range(int(n)):
            con[i] = http.client.HTTPSConnection(ip,source_address=(s_ip[i],443),context=context)    #creates a HTTPS connection from each user to the server
		
    try:
        for i in range(int(n)):
            t1 = threading.Thread(target=down,args=(i,t_end,con,s_ip,file_name))   #each thread represts one user
            procs.append(t1)
            t1.start()

    except Exception as e:
        print(str(e))	
    y = 0		
    for proc in procs:
        proc.join()
        if proc.is_alive():
            pass
        else:
            y,x=count(size,t)	

print("Number of files downloaded = "+str(y))
print("Throughput = "+str(x)+"MBps")
for i in range(6,6+int(n)):
		s_ip[i-6]='192.168.177.'+str(i)
		os.system('sudo ip address del '+s_ip[i-6]+'/24 dev ens33')
