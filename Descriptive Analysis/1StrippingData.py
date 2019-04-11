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
rates = {};
rating = {};
rating['reviews'] = []
ratings_sorted = {};
ratings_sorted['reviews'] = []
i = 0;

sums = 0
process = psutil.Process(os.getpid())

out=gzip.open('metadatanew.json.gz','wt') 
meta={}

#strippingmetadata
#parsing through zipped json file
#
with gzip.open('metadata.json.gz','r') as f:
    for line in f:
        line_json=json.dumps(eval(line))
        parsed = json.loads(line_json);
        dict1={}
        
        asin = parsed['asin']
        dict1['price'] = -1
        if 'price' in parsed:
                dict1['price']=parsed['price']
        out.write(json.dumps({asin: dict1})+ '\n')
        meta[asin]=dict1
        if (i % 500000 == 0 and i != 0):
            print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process) + ")");
        i+= 1

out.close();        
print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process));

#create gzip output file
out=gzip.open('reviewsnew.json.gz','wt') 

#parsing through zipped json file
with gzip.open('aggressive_dedup.json.gz','r') as f:
    for line in f:
        parsed = json.loads(line);
        dict1={}

        asin = parsed['asin']
        price=-1
        dict1['asin'] = asin
        dict1['reviewerID'] = parsed['reviewerID']
        
        if asin in meta:
                price=meta[asin]['price']

        dict1['price']=price        
        if 'overall' in parsed:
                dict1['overall']=parsed['overall']
        out.write(json.dumps(dict1)+ '\n')
        if (i % 500000 == 0 and i != 0):
            print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process) + ")");
        i+= 1

out.close();        
print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process));
print ("Total time taken:" + getTime(start_ts) + " (Memory usage " + getProcessInfo(process));
	
      
