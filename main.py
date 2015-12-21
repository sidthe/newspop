import urllib2
from termcolor import colored
import difflib
import shutil
import time
import os.path

source_choice = raw_input('Choose news source. For Engadget 1\n')

if source_choice == '1':
    html_source = urllib2.urlopen('http://engadget.com').readlines()
    website_name = 'ENGADGET'

print colored(('\n################ TODAYS ' + website_name +' HEADLINES ################\n'), 'white', 'on_red')

def newsfeedbase(site_input):
    pattern_header = ('<h4 class="t-h6 th-title"><span class="th-underline">')
    pattern_link = ('class="o-hit__link"')

#keep past iterations of data
    f = open('memoryfile', 'w')
    f.write('')
    f.close


#find first line that has the header pattern
    for num, pattern in enumerate(site_input,1):
        if pattern_header in pattern:
            break
#read starting with header lines and print
    for newsline in site_input[num-1:]:
        if pattern_header in newsline:
            clean_output = newsline.strip(pattern_header).strip('</span></h4>\n')
#print colored(('#####',clean_output, '#####'), 'white', 'on_blue')
            f = open('memoryfile', 'a')
            f.write(clean_output+'\n')
        if pattern_link in newsline:
            clean_output = newsline.strip(' <a href="').strip('\n').strip('class="o-hit__link">View</a>')
#print colored(('http://engadget.com/' + clean_output+'\n'), 'white')
            f = open('memoryfile', 'a')
            f.write('http://engadget.com/' + clean_output+'\n\n')

#compare memoryfile
    oldf = open('oldmemoryfile', 'r')
    currentf = open('memoryfile', 'r')

    diff = difflib.context_diff(oldf.readlines(), currentf.readlines())
    delta = ''.join(diff).splitlines()
    for newsupdate in delta:
        if '+' in newsupdate:
            print colored(newsupdate.strip(' +'), 'red')

    shutil.copyfile('memoryfile', 'oldmemoryfile')

    time.sleep(300)

#check presence of temp files
if os.path.isfile('memoryfile') == True and os.path.isfile('oldmemoryfile') == True :
    pass
else:
    open('memoryfile', 'w')
    open('oldmemoryfile', 'w')

#read previous news set
print colored((open('memoryfile', 'r').read()), 'white', 'on_blue')

while True:
    try:
        newsfeedbase(html_source)
    except ValueError:
        print "Error: Oops"
