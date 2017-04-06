# Challenge: Insight Fansite Analytics
Given internet traffic data for a NASA fan page, perform basic analysis on the server log file.

The desired features are described below: 

### Feature 1: 
Top 10 most active host/IP addresses that have accessed the site.

### Feature 2: 
Top 10 resources by site bandwidth consumption

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 

### Feature 4: 
Blocked traffic by host/IP addresses after three consecutive failed login attemps over a 20-second window

### Feature 5:
Top 10 most popular resource by traffic

Through first run of this feature, it was observed that the most popular resources are .gifs--it is obvious to see that these are simple webpage logos and as such provide no insight. 
```
 /, 687452
 /images/NASA-logosmall.gif, 216949
 /images/KSC-logosmall.gif, 175041
 /images/USA-logosmall.gif, 121267
 /images/WORLD-logosmall.gif, 117974
 /images/MOSAIC-logosmall.gif, 117771
 /images/ksclogo-medium.gif, 112146
 /images/launch-logo.gif, 94576
 /ksc.html, 89004
 /shuttle/countdown/, 84922
```
After ignoring .gifs, we see the following:

```
 /, 1421896
  /ksc.html, 162816
  /shuttle/countdown/, 151767
  /htbin/cdt_main.pl, 94705
  /shuttle/missions/missions.html, 88410
  /history/apollo/apollo.html, 65310
  /shuttle/countdown/liftoff.html, 62660
  /icons/menu.xbm, 62131
  /shuttle/missions/sts-70/mission-sts-70.html, 59120
  /icons/blank.xbm, 58776
```
After consulting the internet, it was revealed that .xmb files are simple black/white icons. So we proceed by ignoring those. This inspired me to look for the most popular videos accessed on the site. Knowing what content generates the most traffic may be helpful in securing more visitors.

### Feature 6:
Top 10 most popular videos by traffic

# Dependencies:
Written in Python 3
```
import os
import re
import sys
import datetime
from collections import deque
from heapq import nlargest

```
# Documentation of successful run: 

![Proof of success illustration](images/Screen%20Shot%202017-04-05%20at%208.54.15%20PM.png)
The only reason I am including this is because I am new to writing Python scripts. In my submission, I used the following to pass the tests
```
os.chdir(os.path.abspath('.'))
```
while I understand that `.` vs `..` refer to current working directory and parent of current working directory respectively, I do not fully understand why `os.chdir(os.path.abspath('..'))` allows for my code to perform the desired tasks--i.e calculates the metrics and saves the `.txt` files in the desired locations--but fails the tests. 

## Download Data
You can download the data here: https://drive.google.com/file/d/0B7-XWjN4ezogbUh6bUl1cV82Tnc/view

## Description of Data

Assume you receive as input, a file, `log.txt`, in ASCII format with one line per request, containing the following columns:

* **host** making the request. A hostname when possible, otherwise the Internet address if the name could not be looked up.

* **timestamp** in the format `[DD/MON/YYYY:HH:MM:SS -0400]`, where DD is the day of the month, MON is the abbreviated name of the month, YYYY is the year, HH:MM:SS is the time of day using a 24-hour clock. The timezone is -0400.

* **request** given in quotes.

* **HTTP reply code**

* **bytes** in the reply. Some lines in the log file will list `-` in the bytes field. For the purposes of this challenge, it is interpreted as 0 bytes.


e.g., `log.txt`

    in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    208.271.69.50 - - [01/Aug/1995:00:00:02 -400] "POST /login HTTP/1.0" 401 1420
    208.271.69.50 - - [01/Aug/1995:00:00:04 -400] "POST /login HTTP/1.0" 200 1420
    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    ...
    
In the above example, the 2nd line shows a failed login (HTTP reply code of 401) followed by a successful login (HTTP reply code of 200) two seconds later from the same IP address.

# Additional Comments:
In the future, could the person in charge of creating the explanatory illustrations please include a color-blind friendly image. I was very confused for a while and needed to have my father point out which arrows were red and which were green. 

