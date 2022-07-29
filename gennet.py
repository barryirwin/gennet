#!/usr/bin/env python3

# gennet.py  v0.2 
# Generates a series of IP supnets and outputs these as LaTeX or as a CSV
# In the case of LaTeX - tables are produced both populated and unpopulated
# Intention is fotr this to be used to generate worksheets for use in classroom
# enviroments analongside accompanying solutions.
#
# USAGE
#   $ gennet > worksheet.tex; pdflatex worksheet.tex
#
# This is intended to be a minimal function and LaTeX formatting can be adjusted in an edditor of choice

# Use IPtools package
import iptools

# For random generated IP addresses
import random
import socket
import struct

## -------------- some variables to handle data ---------------
MAXIP=20
# RFC 3330 special ise cases
not_valid = [10,127,169,172,192]

#Generates A random IP
# socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

iplist=[]

# This is used to hold a list of subnets which are used to henerate the following:
#    [ip/netmask] - IP address/netmask in CIDR
#    [broadcast] - Broadcast address for the subnet
#    [cidr] - cidr notation
#    [range] - first/last IP in net ( via cidr2block)
#    [netmask] - in dotted quad
#    [count] - number of IPs in subnet - not considering availability (2^n-2)

# this is potentially ~2^32 combinations - and can be changed if needed
seed=random.randrange(31337,65535)
print(f"% {seed} {hex(seed)}")
#set the seed explicitly for repeatability
random.seed(seed)


def dqnetmask(prefix):
    return socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))

def printlatex(mylist):




def latexpreamble()    
    print ("% Do not edit unless you really know what you are doing")
    print ("\\documentclass[english]{article}")
#    print ("\\usepackage[T1]{fontenc}")
#    print ("\\usepackage[latin9]{inputenc}")
    print ("\\usepackage[a4paper]{geometry}")
    print ("\\geometry{verbose,tmargin=2.5cm,bmargin=2.5cm,lmargin=2.0cm,rmargin=2.0cm,headheight=2.5cm,headsep=2.5cm,footskip=2.5cm}")
    print ("\\usepackage{setspace}")
    print ("\\doublespacing")
    print ("\\makeatletter")
    print ("\\providecommand{\\tln}{\\\\}")
    print ("\\makeatother")
    print ("\\newcommand{\\rndseed}{",end='')
    print (f"{hex(seed)}",end='')
    print ("}",end='')
    print (f" % {seed}")
    print ("\\begin{document}")
    print ("\\title{IP Subnetting worksheet - \\rndseed}\n\\date{}\n\\maketitle")
    print ("\\pagenumbering{gobble}")  #remove page numbers for improved inclusion elsewhere

    print ("\\section*{PROBLEMS}")
    latexproblem(mylist)
    print ("\\pagebreak{}\n")
    print ("section*{SOLUTIONS}")
    latexsoln(mylist)

    print ("\\end{document}")

def latexproblem(mylist)    
    print (f"% {hex(seed)} - to be used for later generation of solutions") 

    print ("\\begin{tabular}{|c|c|c|c|c|c|} \hline CIDR &")
    print ("Network & Bcast & IP Count & First IP & DQ Netmask \\tln")
    print ("\\hline\n\\hline")
    print ("102.204.166.91/16 & 102.204.0.0 & 102.204.255.255 & 65536 & 102.204.0.1 & 255.255.0.0 \\tln")
    print ("\\hline")
    for x in  mylist:
        print (f"{x} &            &            &            &            &            \\tln")
        print ("\\hline")

    print ("\\end{tabular}")

def latexsoln(mylist)
    print ("\\begin{tabular}{|c|c|c|c|c|c|} \hline CIDR &")
    print ("Network & Bcast & IP Count & First IP & DQ Netmask \\tln")
    print ("\\hline\n\\hline")


    for x in  mylist:
        netname=iptools.ipv4.cidr2block(x)[0]
        bcast=iptools.ipv4.cidr2block(x)[1]
        first=iptools.ipv4.long2ip(iptools.ipv4.ip2long(netname)+1)
        ipcount=len(iptools.IpRangeList(x))
        dqmask=dqnetmask(int(x[-2:]))
        print (f"{x} & {netname} & {bcast} & {ipcount} & {first} & {dqmask} \\tln") 
        print ("\\hline")

    print ("\\end{tabular}\n")

def printcsv(mylist):
    print(mylist)
    for c in mylist:
        netname=iptools.ipv4.cidr2block(c)[0]
        bcast=iptools.ipv4.cidr2block(c)[1]
        first=iptools.ipv4.long2ip(iptools.ipv4.ip2long(netname)+1)
        ipcount=len(iptools.IpRangeList(c))

        dqmask=dqnetmask(int(c[-2:]))
        print (f"{c},{ipcount},{netname},{bcast},{first},{dqmask}")

# Real work starts here
# print out a a list limited by MAXIP
for i in range(MAXIP):
    first = random.randrange(1,256)
    while (first in not_valid) & (first < 224) :  # no multicast space and no special blocks
        first = random.randrange(1,256)

    ip = ".".join([str(first),str(random.randrange(1,256)),str(random.randrange(1,256)),str(random.randrange(1,256))])
    iplist.append(ip)


for i in iplist:
    mask=random.randrange(16,29)
    masklist.append(mask)
    cidrlist.append("%s/%d" % (i,mask))

#print(cidrlist)
#printcsv(cidrlist)
printlatex(cidrlist)


