#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Draw a solution of a Yajilin problem using matplotlib.
# Usage:
# $ ./yajisat.py decode < o.cnf | ./draw.py

import matplotlib.pyplot as plt
import sys

digit = {}
black = []
link  = {}

# Functions for executing commands
def d(i, j, k, a):
    """Cell (i, j) contains a digit k and arrow a."""
    global digit
    digit[(i, j)] = (k, a)
def b(i, j):
    """Cell (i, j) is black."""
    global black
    black.append((i, j))
def l(i, j, a):
    """Cell (i, j) is linked to the cell at the direction a."""
    global link
    if (i, j) not in link: link[(i, j)] = []
    link[(i, j)].append(a)
def c (*x): pass
def cp(*x): pass
def n (*x): pass

# Read and execute commands
lines = sys.stdin.read()
exec(lines)

# Draw
ax  = plt.gca()

for i, j in digit:
    COL = '#000000'
    k, a = digit[(i, j)]
    plt.text(i-.5, -j+.5, str(k), ha='center', va='center')
    param = {'>': (i - .7, -j + .8,  .4, 0),
             '<': (i - .3, -j + .8, -.4, 0),
             '^': (i - .2, -j + .3,   0, .4),
             'v': (i - .2, -j + .7,   0, -.4)}
    x, y, dx, dy = param[a]
    plt.arrow(x, y, dx, dy, ec=None, fc=COL,
              head_width=.1, head_length=.12, length_includes_head=True)

for i, j in black:
    COL = '#000000'
    r = plt.Rectangle((i-1,-j), 1, 1, ec=COL, fc=COL)
    ax.add_patch(r)

for i, j in link:
    for a in link[(i, j)]:
        COL = '#cccccc'
        param = {'>': (i - .55, -j + .45, .55, .1),
                 '<': (i - 1,   -j + .45, .55, .1),
                 '^': (i - .55, -j + .45, .1, .55),
                 'v': (i - .55, -j,       .1, .55)}
        x, y, w, h = param[a]
        r = plt.Rectangle((x, y), w, h, ec=COL, fc=COL)
        ax.add_patch(r)

plt.axis('scaled')  # make each cell a square
plt.xlim( 0, W)
plt.ylim(-H, 0)
plt.grid()          # draw the grid

plt.show()
