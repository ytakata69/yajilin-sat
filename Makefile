# Usage:
# $ make			# Solve a sample problem
# $ make INPUT=otameshi1.yaj	# Solve the given problem
# $ make pdf			# Make yajilin.pdf

.PHONY: default all clean solve pdf

default: solve
all: pdf solve
pdf: yajilin.pdf

%.pdf: %.dvi
	dvipdfmx $<
%.dvi: %.tex
	platex $<

solve: o.cnf
	./yajisat.py --decode $(INPUT) < $< | ./draw.py

o.cnf: y.cnf
	minisat $< $@ ; test $$? = 10

y.cnf: yajisat.py
	./yajisat.py $(INPUT) > $@

clean:
	$(RM) *.aux *.dvi *.log [yo].cnf yajilin.pdf
