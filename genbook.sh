#!/bin/sh



# (c) 2022 Barry Irwin
# Generates worksheets and matchign solutions in a format for inclusion into a workbook using LaTeX
# Produces worksheets and solutions as separte files in the directories soln/ and prob/
#   Solutions.tex and problems.tex contain the pre-generated lines to be able to easily include the files in a document.


#DEFINE HERE
MAX=50

nums=`seq 1 $MAX`

#debug () {
#  echo "DEBUG: $*"
#}

echo "Generatign workbook content with ${MAX} worksheets"
for i in $nums
do
	./gennet.py -L -o prob > prob/pr$i.tex
	 #extract the seed to generatie a matching solution sheet
	 seed=`head -1 prob/pr$i.tex  |awk '{print $3}'`
	 #echo "$seed"
	./gennet.py -L -o soln -S $seed > soln/soln$i.tex
done

echo Generation complete. Preparign inclusion files for workbook

for i in $nums
do
	# \include forces generationon a new page vs '\input which just inserts
	echo "\\section{Problem $i}" >>problems.tex
	echo -n "\\input{prob/pr${i}.tex}" >> problems.tex
	echo "\\section{Solution $i}" >> solutions.tex
	echo -n "\\input{soln/soln${i}.tex}" >> solutions.tex
done

echo Complete

echo These files are now ready for use in your LaTeX document
