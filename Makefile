# Usage:
# $ make			# Solve a sample problem
# $ make INPUT=otameshi1.yaj	# Solve the given problem
# $ make pdf			# Make yajilin.pdf and yajilin-en.pdf

.PHONY: default all clean solve pdf

default: clean solve
all: pdf solve
pdf: yajilin-en.pdf yajilin.pdf

%.pdf: %.dvi
	-dvipdfmx $<
%.dvi: %.tex
	-platex $<
	-grep 'Label(s) may have changed' $(<:.tex=.log) && \
	platex $<
yajilin-en.pdf: yajilin-en.tex
	-pdflatex $<
	-grep 'Label(s) may have changed' $(<:.tex=.log) && \
	pdflatex $<

solve: o.cnf
	./yajisat.py --decode $(INPUT) < $< | ./draw.py

o.cnf: y.cnf
	minisat $< $@ ; test $$? = 10

y.cnf: yajisat.py
	./yajisat.py $(INPUT) > $@

clean:
	$(RM) *.aux *.dvi *.log [yo].cnf yajilin*.pdf
