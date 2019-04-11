import gzip, json, time, os, psutil, math
from collections import Counter
from itertools import groupby
import statistics

def getProcessInfo(process):
	mem = process.memory_info().rss;
	measure = 'B'
	if (mem >= 1024):
			mem = mem / 1024;
			measure = "KB";
	if (mem >= 1024):
			mem = mem / 1024;
			measure = "MB";
	if (mem >= 1024):
			mem = mem / 1024;
			measure = "GB";
	return ("{:,}".format(round(mem,2)) + " " + measure)

def getTime(starTS):
	seconds = time.time() - starTS
	measure = "s";
	hours = 0;
	days = 0;
	mins = 0;
	if (seconds >= 60):
			mins = int (seconds / 60)
			seconds = seconds - 60*mins           	 
	if (mins >= 60):
			hours = int (mins / 60)
			mins = mins - 60*hours
	if (hours >= 24):
			days = int (hours / 24)
			hours = hours - 24*days

	output = str(days) + ":" + str('%02d' % hours) + ":" + str('%02d' % mins) + ":" + str('%02d' % seconds) ;
	return (output)
		 
#variables
start_ts = time.time();
itemids = {};
userids = {};
i = 0;

sums = 0
process = psutil.Process(os.getpid())

#create gzip output file
#
out=gzip.open('rev1.json.gz','wt') 

#parsing through zipped json file
#extract and dump itemid, reviewerid,helpful, rewiewTime
with gzip.open('aggressive_dedup.json.gz','r') as f:
    for line in f:
        parsed = json.loads(line);
        dict1={}
        
        dict1['asin'] = parsed['asin']
        dict1['reviewerID'] = parsed['reviewerID']
        if 'helpful' in parsed:
                dict1['helpful']=parsed['helpful']
                dict1['reviewTime']=parsed['reviewTime']
        out.write(json.dumps(dict1)+ '\n')
        if (i % 500000 == 0 and i != 0):
            print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process) + ")");
        i+= 1

out.close();        
print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process));
print ("Total time taken:" + getTime(start_ts) + " (Memory usage " + getProcessInfo(process));	
     
