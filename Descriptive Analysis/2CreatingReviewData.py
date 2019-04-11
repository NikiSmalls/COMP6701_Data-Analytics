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



#new dictionary
dict2={}


#parsing through zipped json file
with gzip.open('reviewsnew.json.gz','r') as f:
    for line in f:
        parsed = json.loads(line);
        asin=parsed['asin']
        overall=int(parsed['overall'])
        #print (overall);

        if asin not in dict2:
                dict2[asin]={}
        if overall not in dict2[asin]:
                dict2[asin][overall]=0
        dict2[asin][overall]+=1
        if (i % 500000 == 0 and i != 0):
            print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process) + ")");
        i+= 1

out=open('reviewsnew3.csv','+w')
out.write("{},{},{},{},{},{} \n".format("product","r_one","r_two","r_three","r_four","r_five"))
for asin in dict2:
       
        one = 0;
        two = 0;
        three = 0
        four = 0
        five = 0
        if 1 in dict2[asin]:
                one = dict2[asin][1]
        if 2 in dict2[asin]:
                two = dict2[asin][2]
        if 3 in dict2[asin]:
                three = dict2[asin][3]
        if 4 in dict2[asin]:
                four = dict2[asin][4]
        if 5 in dict2[asin]:
                five = dict2[asin][5]
        temp ="{},{},{},{},{},{} \n".format(asin,one,two,three,four,five)
        out.write(temp)
         
out.close();        
print ("{:,}".format(i) + " records processed took " + getTime(start_ts) + " (Memory usage " + getProcessInfo(process));
print ("Total time taken:" + getTime(start_ts) + " (Memory usage " + getProcessInfo(process));
	
      
