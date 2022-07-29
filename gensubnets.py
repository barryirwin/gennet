#!/usr/bin/env python3


# Use IPtools package
import iptools

# For random generated IP addresses
import random
import socket
import struct

MAXIP=20
# RFC 3330 special ise cases
not_valid = [10,127,169,172,192]

#Generates A random IP
# socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

iplist=[]
cidrlist=[]
masklist=[]

# this is potentially ~2^32 combinations - and can be changed if needed
seed=random.randrange(31337,65535)
print(f"% {seed} {hex(seed)}")
#set the seed explicitly for repeatability
random.seed(seed)
# strucuture
#/*
#demolist[]
# [ip] - IP addresses
#    [netmask] - netmask in CIDR
#    [cidr] - cidr notation
#    [range] - first/last IP in net ( via cidr2block)
#    [nm2] - dotted quad  via
#    [cnt] - number of IPs avalable
#*/

def dqnetmask(prefix):
    return socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))

def printlatex(mylist):
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
    print (f"% {hex(seed)}") 

    print ("\\begin{tabular}{|c|c|c|c|c|c|} \hline CIDR &")
    print ("Network & Bcast & IP Count & First IP & DQ Netmask \\tln")
    print ("\\hline\n\\hline")
    print ("102.204.166.91/16 & 102.204.0.0 & 102.204.255.255 & 65536 & 102.204.0.1 & 255.255.0.0 \\tln")
    print ("\\hline")
    for x in  mylist:
        print (f"{x} &            &            &            &            &            \\tln")
        print ("\\hline")

    print ("\\end{tabular}")

    print ("\\pagebreak{}\n\\section*{SOLUTIONS}")

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

    print ("\\end{tabular}\n\\end{document}")

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


