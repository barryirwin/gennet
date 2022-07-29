# gennet

Subnet worksheet generator

This script was developed to aid in the need for drill and practice exercises for teaching an introductory networks course. This has devleoped over the years to add additional functionality and use cases.

The worksheets contents are randomly generated and outputted as (a minimal) LaTeX document. This document (or select parts of it) can then be converted to a PDF using pdflatex or similar. 

Options allow for the generation of a two-sided worksheet containing solutions. Alternately this can be suppressed, for more summative type exercises.

The problems and solutions tables can each be generated separately for inclusionas part of a larger LaTeX document.

Seed values are stroed in the LaTeX versions of the output. These can be used to regenerate a particular set of output (for example a solution) at a later stage.

##USAGE
This produced a list of IPv4 subnets to stdout in a variety of formats


 ./gennet.py [-hV] [-px] [-m <num>] [-s <num] [-L [-o val] | -C] 
  -h     This usage guide
  -m <n> Number of IP subnets to generate  (default=20)
  -o <type> Output type for partial output in LaTex mode
           soln - Solutions table
           prob - Problems table
  -p     Include RFC1918/RFC 3300 special use IP addresses (default=no)
  -x     Do not print the example row in the problems table
  -L     Latex Documnet output mode
  -C     CSV output mode
  -S <n> Seed (int or hex - [0x????] )
  -V    Version and source information

Minimum examples:
	./gennet.py -L # prints a ful LaTeX dump
	./gennet.py -C # prints CSV output

Conversion:
	$ ./gennet.py -L > temp.tex; pdflatex temp.tex

$Id$

