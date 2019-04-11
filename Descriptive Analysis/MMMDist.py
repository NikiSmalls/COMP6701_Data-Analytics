import time, os, psutil, math, csv
from collections import Counter
from itertools import groupby
import statistics
								
################################################################
#Calculate mean, mode, median

#variables
mean=0
sumratings = 0
count=0
max_rating = 0
mode = 0
skewed = ""


#file to hold results
#item:mean:mode:median:distribition/skew

readcsv=open('musical_ratings.csv','r')

out= open("mmmdist.csv", "+w")
out.write("{},{},{},{},{} \n".format("product","mean","median","mode","distribution"))

i = 0

for row in readcsv:
        #print(row + "{}".format(i) )
        
        if i != 0:
                column=row.split(',')
                asin=column[0]
                one=int(column[1])
                two=int(column[2])
                three=int(column[3])
                four=int(column[4])
                five=int(column[5])
                count=one+two+three+four+five
                mean=(one*1+two*2+three*3+four*4+five*5)/count
                mode=1
                modev = one;
                if modev < two:
                        mode=2
                        modev = two
                if modev <three:
                        mode=3
                        modev =three
                if modev < four:
                        mode=4
                        modev=four
                if modev < five:
                        mode=5
                        modev=five
                median=(count+1)/2
                med1f = False;
                med2f = False;
                medianv1= 0
                medianv2= 0
                curr=0
                if curr+one >= math.floor(median):
                        medianv1=1
                        med1f=True
                if curr+one >= math.ceil(median):
                        medianv2=1
                        med2f=True
                curr+=one
                if curr+two >= math.floor(median)and not (med1f):
                        medianv1=2
                        med1f=True
                if curr+two >= math.ceil(median)and not (med2f):
                        medianv2=2
                        med2f=True
                curr+=two
                if curr+three >= math.floor(median)and not (med1f):
                        medianv1=3
                        med1f=True
                if curr+three >= math.ceil(median)and not (med2f):
                        medianv2=3
                        med2f=True
                curr+=three
                if curr+four >= math.floor(median)and not (med1f):
                        medianv1=4
                        med1f=True
                if curr+four >= math.ceil(median)and not (med2f):
                        medianv2=4
                        med2f=True
                curr+=four
                if curr+five >= math.floor(median)and not (med1f):
                        medianv1=5
                        med1f=True
                if curr+five >= math.ceil(median)and not (med2f):
                        medianv2=5
                        med2f=True
                curr+=five
                medianv=(medianv1+medianv2)/2
                q1=(count+1)/4#
                q2=2*(count+1)/4
                q3=3*(count+1)/4#
                q4=4*(count+1)/4
                if (q3-q2)==(q2-q1):
                        skewed="Symmetrical"
                if (q3-q2)>(q2-q1):
                        skewed="Positive Skewed"
                if (q3-q2)<(q2-q1):
                        skewed="Negatively Skewed"
                #if medianv >=2:
                #        skewed="Positive Skewed"
                #elif medianv <=4:
                #        skewed="Negatively Skewed"
                #else:
                #        skewed="Symmetrical"
     
                out.write("{},{},{},{},{} \n".format(asin,mean,medianv,mode,skewed))
                
        i+=1


readcsv.close()
out.close()
