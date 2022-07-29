#!/usr/bin/env python3

# gennet.py  (c) Barry Irwin  
# Generates a series of IP supnets and outputs these as LaTeX or as a CSV
# In the case of LaTeX - tables are produced both populated and unpopulated
# Intention is fotr this to be used to generate worksheets for use in classroom
# enviroments analongside accompanying solutions.
#
# USAGE
#   $ gennet <args> > worksheet.tex; pdflatex worksheet.tex
#
# This is intended to be a minimal function and LaTeX formatting can be adjusted in an edditor of choice
try:
    import iptools
except:
    print("You require the  iptools module to run this script\n pip install iptools")
    sys.exit(2)
import random # For random generated IP addresses
import socket, struct
import sys, getopt


## -------------- some variables to handle data ---------------
VERSION = '0.3b'
CONF={}
# Default values set
CONF['maxip']= 20
CONF['output']= 'L'
CONF['not_valid']= [10,127,169,172,192] # RFC 3330 special use cases
CONF['seed']= random.randrange(31337,65535) # this is potentially ~2^32 combinations
CONF['exline']= True  #include an example line in problem output
CONF['loutput']= 'full' #by default full output

iplist=[]
masklist=[]
cidrlist=[]

# This is used to hold a list of subnets which are used to henerate the following:
#    [ip/netmask] - IP address/netmask in CIDR
#    [broadcast] - Broadcast address for the subnet
#    [cidr] - cidr notation
#    [range] - first/last IP in net ( via cidr2block)
#    [netmask] - in dotted quad
#    [count] - number of IPs in subnet - not considering availability (2^n-2)

#set the seed explicitly for repeatability


def dqnetmask(prefix):
    return socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def printlatex(mylist):
    print ("% Do not edit unless you really know what you are doing")
    print ("\\documentclass[english]{article}")
    print ("\\usepackage[a4paper]{geometry}")
    print ("\\geometry{verbose,tmargin=2.5cm,bmargin=2.5cm,lmargin=2.0cm,rmargin=2.0cm,headheight=2.5cm,headsep=2.5cm,footskip=2.5cm}")
    print ("\\usepackage{setspace}")
    print ("\\doublespacing")
    print ("\\makeatletter")
    print ("\\providecommand{\\tln}{\\\\}")
    print ("\\makeatother")
    print ("\\newcommand{\\rndseed}{",end='')
    print (f"{hex(CONF['seed'])}",end='')
    print ("}",end='')
    print (f" % {CONF['seed']}")
    print ("\\begin{document}")
    print ("\\title{IP Subnetting worksheet - \\rndseed}\n\\date{}\n\\maketitle")
    print ("\\pagenumbering{gobble}")  #remove page numbers for improved inclusion elsewhere

    print ("\\section*{PROBLEMS}")
    latexproblem(mylist)
    print ("\\pagebreak{}\n")
    print ("section*{SOLUTIONS}")
    latexsoln(mylist)

    print ("\\end{document}")

def latexproblem(mylist):    
    print (f"% {hex(CONF['seed'])} - to be used for later generation of solutions") 

    print ("\\begin{tabular}{|c|c|c|c|c|c|} \hline CIDR &")
    print ("Network & Bcast & IP Count & First IP & DQ Netmask \\tln")
    print ("\\hline\n\\hline")
    if (CONF['exline']):
        print ("102.204.166.91/16 & 102.204.0.0 & 102.204.255.255 & 65536 & 102.204.0.1 & 255.255.0.0 \\tln")
        print ("\\hline")

    for x in  mylist:
        print (f"{x} &            &            &            &            &            \\tln")
        print ("\\hline")

    print ("\\end{tabular}")

def latexsoln(mylist):
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
    print ("#IP/mask,IP Count,Netblock,Broadcast,First IP,DQ Netmask")
    for c in mylist:
        netname=iptools.ipv4.cidr2block(c)[0]
        bcast=iptools.ipv4.cidr2block(c)[1]
        first=iptools.ipv4.long2ip(iptools.ipv4.ip2long(netname)+1)
        ipcount=len(iptools.IpRangeList(c))

        dqmask=dqnetmask(int(c[-2:]))
        print (f"{c},{ipcount},{netname},{bcast},{first},{dqmask}")

def usage(name):
    print("This produced a list of IPv4 subnets to stdout in a variety of formats\n\n")
    print (f" {name} [-hV] [-px] [-m <num>] [-s <num] [-L [-o val] | -C] ")
    print ("  -h     This usage guide")
    print ("  -m <n> Number of IP subnets to generate  (default=20)")
   # print ("  -4     IPv4 mode (default)")
    #print ("  -6     IPv6 mode (max subnet of /64)")
    print ('''  -o <type> Output type for partial output in LaTex mode
           soln - Solutions table
           prob - Problems table''')
    print ("  -p     Include RFC1918/RFC 3300 special use IP addresses (default=no)")
    print ("  -x     Do not print the example row in the problems table")
    print ("  -L     Latex Documnet output mode")
    print ("  -C     CSV output mode")
    print ("  -S <n> Seed (int or hex - [0x????] )")
    print ("  -V    Version and source information")

    print(f"\nMinimum examples:\n\t{name} -L # prints a ful LaTeX dump\n\t{name} -C # prints CSV output")


def dumpconf():
    eprint("Dumping Config")
    eprint(f"{CONF}")

def main(argv):
    global CONF
    if(len(sys.argv)<2):
        usage(sys.argv[0])
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv[1:],"46hm:o:pxCLS:V",["help","max-ip=","output","version"])
    except getopt.GetoptError:
        usage(sys.argv[0])  #thrown if any args dont match or no args given
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage(sys.argv[0])
            sys.exit()
        elif opt in ['-o','--output']:
            CONF['loutput']=arg
        elif opt == '-p':
            CONF['not_valid']=[]
        elif opt == '-x':
            CONF['exline'] = False
        elif opt == '-S':
            if arg[:2] == '0x' or arg[:2]=='0X':
                CONF['seed'] = int(arg,base=16)
            else:
                CONF['seed'] = int(arg)
        elif opt in ("-m", "--max-ip"):
           CONF['maxip'] = int(arg)
        elif opt in ("-L","-C"):
           CONF['output'] = opt[1]
        elif opt in ["-V","--version"]:
            print(f"Version: {VERSION} (c) 2022 Barry Irwin")
            print("Available at: https://github.com/barryirwin/gennet")
            usage(sys.argv[0])
            sys.exit()
        elif opt in ["-4","-6"]:
            print(f"This function \"{opt}\" does not yet know what to do")
            usage(sys.argv[0])
            sys.exit()

    random.seed(CONF['seed'])
   # dumpconf()
# Real work starts here
# print out a a list limited by CONF['maxip']
    for i in range(int(CONF['maxip'])):
        first = random.randrange(1,223)


        while ((first in CONF['not_valid']) or (first > 224)) :  # no multicast space and no special blocks
            first = random.randrange(1,256)

        ip = ".".join([str(first),str(random.randrange(1,256)),str(random.randrange(1,256)),str(random.randrange(1,256))])
        iplist.append(ip)

    for i in iplist:
        mask=random.randrange(16,29)
        masklist.append(mask)
        cidrlist.append("%s/%d" % (i,mask))
# now produce outputs based on  instructions
    otype=CONF['output']
    loutput=CONF['loutput']
    if otype == 'C': #CSV dump
        printcsv(cidrlist)
        sys.exit(1)
    elif otype == 'L': # latex options
        if CONF['loutput']=='prob':
            latexproblem(cidrlist)
        elif CONF['loutput']=='soln':
            latexsoln(cidrlist)
        else:
            printlatex(cidrlist)
#print(cidrlist)
#printcsv(cidrlist)
#printlatex(cidrlist)

if __name__ == "__main__":
   main(sys.argv)


# -- fin --
#Generates A random IP
# socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

