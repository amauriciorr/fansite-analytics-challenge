#!/usr/bin/env python3
import os
import re
import sys
import datetime
from collections import deque
from heapq import nlargest

#for some reason I was encoutering a decoding error with the text file
#despite the fact that it was stated in the challenge summary that all the text is in ascii. 
#I was able to find the line of text that was causing this error but did not see anything out of the ordinary.
#a workaround involved using latin-1 encoding

#while looking for resources and corresponding bandwidth consumption, there were several lines of code that appeared
#to be missing resources; 9 lines, to be exact. since 9 out of approximately 4.4 million lines accounts for very little
#I won't stress over finding a way to account for these missing values. 
#for example one of the lines is klothos.crl.research.digital.com - - [10/Jul/1995:16:45:50 -0400] "" 400 -


# ## Feature 1: 10 most active hosts/IP addresses

os.chdir(os.path.abspath('.'))

hosts = {}
file1= open("log_output/hosts.txt","w")
with open("log_input/log.txt","r",encoding='latin-1') as f:
  for line in f:
    ip=re.search(r'[A-Za-z-.0-9_]+(?= - -)',line).group(0)
    if ip not in hosts.keys():
      hosts[ip]=1
    else:
      hosts[ip]+=1

p=nlargest(10,hosts, key= lambda e: hosts[e])
for i in p:
  file1.write(i+','+str(hosts[i])+'\n')


## Feature 2: top 10 resources by bandwidth consumption/usage
resources={}
file2= open("log_output/resources.txt","w")
with open("log_input/log.txt","r",encoding='latin-1') as f:
  for line in f:
    byte = re.search(r'[0-9]+$|-$',line).group(0)
    if re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\"|/\"',line):
      res = re.sub(r' ([a-zA-Z0-9./]+)?\"|\"','',re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\"|/\"',line).group(0))
      res= res.lstrip(' ')
    elif re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\\xe2\\x80\\x9d|/\"',str(line.encode('Latin-1'))):
      res= re.sub(r' ([a-zA-Z0-9./]+)?\\xe2\\x80\\x9d|\"','',re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\\xe2\\x80\\x9d|/\"',str(line.encode('Latin-1'))).group(0))
      res=res.lstrip(' ')
    if res not in resources.keys():
      if re.search(r'-',byte):
        resources[res]=0
      else:
        resources[res]=int(byte)
    else:
      if not re.search(r'-',byte):
        resources[res]+=int(byte)




p1= nlargest(10,resources,key = lambda j: resources[j])
for i in p1:
  file2.write(i+'\n')


## Feature 3: 10 busiest 60-min windows
visits=[]
tstamps=deque()
limbo=deque()

def evac(min_time,dq):
  while dq[0]<min_time:
    dq.popleft()
    if len(dq)==0:
      break


file3=open("log_output/hours.txt","w")
with open("log_input/log.txt","r",encoding='latin-1') as f:
  for j,line in enumerate(f):
    if j==0:
      t=re.search(r'\[\d{2}/\S{3}/\d{4}:\d{2}:\d{2}:\d{2} -0400\]',line).group(0)
      t=re.sub(r'[\[\]]','',t)
      min_t=datetime.datetime.strptime(t, "%d/%b/%Y:%H:%M:%S %z")
      max_t = min_t+datetime.timedelta(minutes=60)
      tstamps.append(min_t)


    t2=re.search(r'\[\d{2}/\S{3}/\d{4}:\d{2}:\d{2}:\d{2} -0400\]',line).group(0)
    t2=re.sub(r'[\[\]]','',t2)
    t_now=datetime.datetime.strptime(t2, "%d/%b/%Y:%H:%M:%S %z")
    if len(limbo)>0:
      while limbo[0]< max_t:
        tstamps.append(limbo.popleft())
        if len(limbo)==0:
          break

    if len(visits)>10:
      visits=nlargest(10,visits, key =lambda k: k[1])

    if t_now <= max_t and j>0:
      tstamps.append(t_now)

    elif t_now > max_t and j>0:
      visits.append((min_t,len(tstamps)))
      evac(min_t,tstamps)
      min_t= min_t+datetime.timedelta(seconds=1)
      max_t= min_t+datetime.timedelta(minutes=60)
      if t_now <=max_t:
        tstamps.append(max_t)
      else:
        limbo.append(t_now)
  min_t = tstamps[0]
  if len(visits)<10 and tstamps[-1]<=tstamps[0]+datetime.timedelta(minutes=60):
      while len(tstamps)>0:
        visits.append((min_t,len(tstamps)))
        min_t = (min_t+datetime.timedelta(seconds=1))
        evac(min_t,tstamps)

p2= nlargest(10,visits,key =lambda k: k[1])

for i in p2:
  file3.write("{:%d/%b/%Y:%H:%M:%S %z}".format(i[0])+','+str(i[1])+'\n')



## Feature 4: Blocked traffic
breach={}
file4=open("log_output/blocked.txt","w")
with open("log_input/log.txt","r",encoding='latin-1') as f:
  for line in f:
    ip=re.search(r'[A-Za-z-.0-9_]+(?= - -)',line).group(0)

    if ip not in breach.keys() and re.search(r'POST /login HTTP/1.0\" 401',line): 
      t=re.search(r'\[\d{2}/\S{3}/\d{4}:\d{2}:\d{2}:\d{2} -0400\]',line).group(0)
      t=re.sub(r'[\[\]]','',t)
      tt=datetime.datetime.strptime(t, "%d/%b/%Y:%H:%M:%S %z")
      breach[ip]=[tt,1]

    elif ip not in breach.keys():
      breach[ip]=[0,0]

    elif ip in breach.keys() and (breach[ip][1] == 3):
      t=re.search(r'\[\d{2}/\S{3}/\d{4}:\d{2}:\d{2}:\d{2} -0400\]',line).group(0)
      t=re.sub(r'[\[\]]','',t)
      tt=datetime.datetime.strptime(t, "%d/%b/%Y:%H:%M:%S %z")
      if tt < (breach[ip][0]+datetime.timedelta(minutes=5)):
        file4.write(line)
      else:
        breach[ip][1]=0

    elif ip in breach.keys() and (breach[ip][1]==0) and re.search(r'POST /login',line):
      t=re.search(r'\[\d{2}/\S{3}/\d{4}:\d{2}:\d{2}:\d{2} -0400\]',line).group(0)
      t=re.sub(r'[\[\]]','',t)
      tt=datetime.datetime.strptime(t, "%d/%b/%Y:%H:%M:%S %z")
      if re.search(r'\"POST /login HTTP/1.0\" 401',line):
        breach[ip][0]=tt
        breach[ip][1]=1

    elif ip in breach.keys() and (breach[ip][1] < 3) and re.search(r'POST /login',line):
      t=re.search(r'\[\d{2}/\S{3}/\d{4}:\d{2}:\d{2}:\d{2} -0400\]',line).group(0)
      t=re.sub(r'[\[\]]','',t)
      tt=datetime.datetime.strptime(t, "%d/%b/%Y:%H:%M:%S %z")
      if re.search(r'\"POST /login HTTP/1.0\" 200',line) and tt<breach[ip][0]+datetime.timedelta(seconds=20):
        breach[ip][1]=0      

      elif re.search(r'\"POST /login HTTP/1.0\" 401',line) and tt<breach[ip][0]+datetime.timedelta(seconds=20):
        breach[ip][1]+=1

      elif re.search(r'\"POST /login HTTP/1.0\" 401',line) and tt>breach[ip][0]+datetime.timedelta(seconds=20):
        breach[ip][0]=tt
        breach[ip][1]=1


###two additional features: top 10 resources by traffic and top 10 videos by traffic respectively
resources_freq={}
file5=open("log_output/popular_resources.txt","w")
with open("log_input/log.txt","r",encoding='latin-1') as f:
  for line in f:
    if re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\"|/\"',line) and not re.search(r'\.gif',line) and not re.search(r'\.xbm',line) and not re.search(r'\.pl',line):
      res = re.sub(r' ([a-zA-Z0-9./]+)?\"|\"','',re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\"|/\"',line).group(0))
      if res not in resources_freq.keys():
        resources_freq[res]=1
      else:
        resources_freq[res]+=1

pp = nlargest(10, resources_freq, key= lambda d: resources_freq[d])

for i in pp:
  file5.write(i+', '+str(resources_freq[i])+'\n')

mov_freq={}
file6 = open("log_output/videos.txt","w")
with open("log_input/log.txt","r",encoding='latin-1') as f:
  for line in f:
    if re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\"|/\"',line) and re.search(r'\.mpg',line) :
      res = re.sub(r' ([a-zA-Z0-9./]+)?\"|\"','',re.search(r' :?/[\Sa-zA-Z-.0-9_/?, ]+\"|/\"',line).group(0))
      if res not in mov_freq.keys():
        mov_freq[res]=1
      else:
        mov_freq[res]+=1

pm = nlargest(10, mov_freq, key= lambda d: mov_freq[d])
for i in pm:
  file6.write(i+', '+str(mov_freq[i])+'\n')

