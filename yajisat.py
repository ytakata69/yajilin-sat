#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ヤジリンをSATソルバで解く
# 2018.8.29 y-takata
# cf.
# ヤジリンの遊び方，ルール，解き方
# https://www.nikoli.co.jp/ja/puzzles/yajilin/

# usage:
#   yajisat.py [-d | --decode] [-v | --verbose] [<inputfile>]
#
# $ ./yajisat.py > y.cnf
# $ minisat y.cnf o.txt
# $ ./yajisat.py --decode < o.txt

from sys import argv, stderr

# コマンドライン引数
argv.pop(0)  # コマンド名自身を削除
decode_mode  = '-d' in argv or '--decode'  in argv
verbose_mode = '-v' in argv or '--verbose' in argv
inputfile = \
    ([v for v in argv if not v.startswith('-')] + [None])[0]

# 方向を表す諸定数
left  = lambda x: (x[0] - 1, x[1])
right = lambda x: (x[0] + 1, x[1])
up    = lambda x: (x[0],     x[1] - 1)
down  = lambda x: (x[0],     x[1] + 1)
X = [left, right, up, down]
revers = {left: right, right: left, up: down, down: up}
prnt   = [None, "'<'", "'>'", "'^'", "'v'"]
def ob(x, a): return not(1 <= a(x)[0] <= W and 1 <= a(x)[1] <= H)

# 盤面

# 「ヤジリンの遊び方，ルール，解き方」の例題
# https://www.nikoli.co.jp/ja/puzzles/yajilin/
W = 7  # 幅
H = 7  # 高さ
digit = { # (列, 行): (数字, 矢印) 列・行は1から
    (3,2): (1,up),
    (6,2): (1,left),
    (2,5): (1,up),
    (4,5): (2,right),
    (3,7): (0,left)
}

# 盤面をファイルから読み出す
if inputfile != None:
    with open(inputfile, 'r') as f:
        first = True
        for row in f:
            if row.strip().startswith('#') or row.strip() == '':
                continue
            if first:
                W, H = [int(t) for t in row.split()]
                digit = {}
                first = False
            else:
                t = row.lower().split()
                i, j, k = map(int, t[:3])
                a = {'>': right, '<': left, '^': up, 'v': down}[t[3]]
                digit[(i, j)] = (k, a)

# 必ず線を引くべきマスを1個選ぶ（到達可能性を調べる起点）
pivot = None
for i, j in digit:
    k, a = digit[(i, j)]
    if k == 0:
        x, y = i, j
        while not ob((x, y), a):
            x, y = a((x, y))
            if (x, y) not in digit:
                pivot = (x, y)
                break
    if pivot != None: break

# SAT符号化

# 命題変数
def basedist(i, j, x, y):
    """マス(i,j)とマス(x,y)の奇偶が同じなら0，異なれば1"""
    return 0 if (i + j) % 2 == (x + y) % 2 else 1
def cell(i, j):
    """マス番号 1 〜 W*H"""
    assert 1 <= i <= W and 1 <= j <= H
    return (j-1) * W + i
def angle(a):
    """方向番号 1〜4"""
    assert a in X
    return {left: 1, right: 2, up: 3, down: 4}[a]
def Vb(i, j):
    return cell(i, j)
def Vd(i, j):
    return cell(i, j) + Vb(W, H)
def Vl(i, j, a):
    return (cell(i, j) - 1) * 4 + angle(a) + Vd(W, H)
def Vc(i, j, x, y, m):
    assert 0 <= m <= W * H // 2
    assert basedist(i, j, x, y) == m % 2
    v = (cell(i, j) - 1) * W * H if pivot == None else 0
    v = (v + cell(x, y) - 1) * (W * H // 2 + 1) + (m + 1)
    return v + Vl(W, H, down)
def Vcp(i, j, x, y, m, a):
    assert 0 <= m <= W * H // 2
    assert basedist(i, j, x, y) == m % 2
    v = (Vc(i, j, x, y, m) - Vc(1, 1, 1, 1, 0)) * 4 + angle(a)
    return v + Vc(W, H, W, H, W * H // 2)
def Vn(i, j, a, m):
    assert 0 <= m <= max(W, H)
    v = ((cell(i, j) - 1) * 4 + angle(a) - 1) * (max(W, H) + 1) + (m + 1)
    return v + Vcp(W, H, W, H, W * H // 2, down)
def Vp(i):
    """p_i: 数字でも黒マスでもないマスがi番目以前に存在する．"""
    assert 0 <= i <= W * H
    return i + 1 + Vn(W, H, down, max(W, H))
Vlast = Vp(W * H) if pivot == None else Vn(W, H, down, max(W, H))

def celldecode(v):
    i = (v - 1) %  W + 1
    j = (v - 1) // W + 1
    return i, j
def Vdecode(v):
    assert 1 <= v <= Vlast
    if v <= Vb(W, H):
        i, j = celldecode(v)
        return 'b({},{})'.format(i, j)
    elif v <= Vd(W, H):
        v -= Vb(W, H)
        i, j = celldecode(v)
        k, a = digit[(i, j)]
        return 'd({},{},{},{})'.format(i, j, k, prnt[angle(a)])
    elif v <= Vl(W, H, down):
        v -= Vd(W, H)
        a    = (v - 1) %  4 + 1
        i, j = celldecode((v - 1) // 4 + 1)
        return 'l({},{},{})'.format(i, j, prnt[a])
    elif v <= Vc(W, H, W, H, W * H // 2):
        v -= Vl(W, H, down)
        m = (v - 1) %  (W * H // 2 + 1)
        v = (v - 1) // (W * H // 2 + 1) + 1
        x, y = celldecode((v - 1) %  (W * H) + 1)
        i, j = celldecode((v - 1) // (W * H) + 1)
        return 'c({},{},{},{},{})'.format(i, j, x, y, m)
    elif v <= Vcp(W, H, W, H, W * H // 2, down):
        v -= Vc(W, H, W, H, W * H // 2)
        a = (v - 1) %  4 + 1
        v = (v - 1) // 4 + 1
        m = (v - 1) %  (W * H // 2 + 1)
        v = (v - 1) // (W * H // 2 + 1) + 1
        x, y = celldecode((v - 1) %  (W * H) + 1)
        i, j = celldecode((v - 1) // (W * H) + 1)
        return 'cp({},{},{},{},{},{})'.format(i, j, x, y, m, prnt[a])
    elif v <= Vn(W, H, down, max(W, H)):
        v -= Vcp(W, H, W, H, W * H // 2, down)
        m = (v - 1) %  (max(W, H) + 1)
        v = (v - 1) // (max(W, H) + 1) + 1
        a = (v - 1) %  4 + 1
        i, j = celldecode((v - 1) // 4 + 1)
        return 'n({},{},{},{})'.format(i, j, prnt[a], m)
    elif v <= Vp(W * H):
        v -= Vn(W, H, down, max(W, H))
        i = v - 1
        return 'p({})'.format(i)
    else:
        raise

# 復号モード
if decode_mode:
    input()  # skip the header (SAT or UNSAT)
    lit = [int(t) for t in input().split() if int(t) >= 0]
    assert lit[-1] == 0
    lit.pop()
    print('W,H={},{}'.format(W, H))
    for s in map(Vdecode, lit):
        if not verbose_mode and s.startswith('c'): break
        print(s)
    exit()


# 符号化モード

def doubleloop(f1, t1, f2, t2):
    for i in range(f1, t1):
        for j in range(f2, t2):
            yield (i, j)

def add_reachability_clauses(i, j, clause):
    """マス(i,j)からの到達可能性に関する節をclauseに追加する．"""

    # 起点マスが存在するなら起点からの到達可能性のみ調べればよい
    if pivot != None and pivot != (i, j): return

    # 自分自身のみ距離0で到達可能
    clause.append([Vc(i,j,i,j,0)])
    for x, y in doubleloop(1, W+1, 1, H+1):
        if (x, y) == (i, j): continue
        if pivot == None and (x, y) <= (i, j): continue
        if basedist(i, j, x, y) == 0:
            clause.append([-Vc(i,j,x,y,0)])

    # cp(i,j,x,y,m,a) == c(i,j,x,y,m) and l(x,y,a)
    for x, y in doubleloop(1, W+1, 1, H+1):
        if pivot == None and (x, y) < (i, j): continue
        for m in range(basedist(i,j,x,y), W * H // 2 + 1, 2):
            for a in X:
                clause.append([-Vcp(i,j,x,y,m,a), Vc(i,j,x,y,m)])
                clause.append([-Vcp(i,j,x,y,m,a), Vl(x,y,a)])

    # 線でつながっているマスに到達可能であるときのみ到達可能
    for x, y in doubleloop(1, W+1, 1, H+1):
        if pivot == None and (x, y) <= (i, j): continue
        for m in range(2 - basedist(i,j,x,y), W * H // 2 + 1, 2):
            tmpcl = [-Vc(i,j,x,y,m)]
            if m >= 2:
                tmpcl.append(Vc(i,j,x,y,m-2))
            for a in X:
                if ob((x, y), a): continue
                xp, yp = a((x, y))
                if pivot == None and (xp, yp) < (i, j): continue
                tmpcl.append(Vcp(i,j,xp,yp,m-1,revers[a]))
            clause.append(tmpcl)

    # マスの通し番号 ((i,j) < (x,y) なら idx(i,j) < idx(x,y))
    idx = (i - 1) * H + j

    # 起点マス（または最初の空白マス）からすべての空白マスに到達可能
    for x, y in doubleloop(1, W+1, 1, H+1):
        if pivot == None and (x, y) <= (i, j): continue
        m = W * H // 2
        if m % 2 != basedist(i,j,x,y): m -= 1
        tempcl = [Vd(x,y), Vb(x,y), Vc(i,j,x,y,m)]
        if pivot == None:
            tempcl.extend([-Vp(idx), Vp(idx-1)])
        clause.append(tempcl)

    # 起点マスがあるなら「最初の空白マス」に関する節は不要
    if pivot != None: return

    # idx番目のマス以前に空白マスがある ⇔ idx-1番目以前にある ∨ idx番目が空白マス
    clause.append([-Vp(idx-1), Vp(idx)])
    clause.append([Vb(i,j), Vd(i,j), Vp(idx)])
    clause.append([-Vp(idx), Vp(idx-1), -Vb(i,j)])
    clause.append([-Vp(idx), Vp(idx-1), -Vd(i,j)])

    # 番兵: 0番目のマス以前に白マスはない
    if idx == 1:
        clause.append([-Vp(0)])

# 節
clause = []
for i, j in doubleloop(1, W+1, 1, H+1):
    print('Processing cell ({}, {})'.format(i, j), file=stderr)

    # 数字マスは黒マスでない
    clause.append([-Vd(i,j), -Vb(i,j)])

    for a in X:
        # 黒マスは線が通らない
        clause.append([-Vb(i,j), -Vl(i,j,a)])
        # 数字マスは線が通らない
        clause.append([-Vd(i,j), -Vl(i,j,a)])

    # 黒マスはタテヨコに連続しない
    if i < W:
        clause.append([-Vb(i,j), -Vb(i+1,j)])
    if j < H:
        clause.append([-Vb(i,j), -Vb(i,j+1)])

    # マス(i,j)が数字マスである or ない
    if (i,j) in digit:
        clause.append([Vd(i,j)])
    else:
        clause.append([-Vd(i,j)])

    # 線は対称
    if i < W:
        clause.append([-Vl(i,j,right),  Vl(i+1,j,left)])
        clause.append([ Vl(i,j,right), -Vl(i+1,j,left)])
    if j < H:
        clause.append([-Vl(i,j,down),  Vl(i,j+1,up)])
        clause.append([ Vl(i,j,down), -Vl(i,j+1,up)])
    # 端っこ
    for a in X:
        if ob((i, j), a):
            clause.append([-Vl(i,j,a)])

    # たかだか2つのマスと線でつながる
    clause.append([-Vl(i,j,left),  -Vl(i,j,right), -Vl(i,j,up)])
    clause.append([-Vl(i,j,left),  -Vl(i,j,right), -Vl(i,j,down)])
    clause.append([-Vl(i,j,left),  -Vl(i,j,up),    -Vl(i,j,down)])
    clause.append([-Vl(i,j,right), -Vl(i,j,up),    -Vl(i,j,down)])

    # 1マスとだけ線でつながることはない
    clause.append([Vl(i,j,left), Vl(i,j,right), Vl(i,j,up), -Vl(i,j,down)])
    clause.append([Vl(i,j,left), Vl(i,j,right), -Vl(i,j,up), Vl(i,j,down)])
    clause.append([Vl(i,j,left), -Vl(i,j,right), Vl(i,j,up), Vl(i,j,down)])
    clause.append([-Vl(i,j,left), Vl(i,j,right), Vl(i,j,up), Vl(i,j,down)])

    # 到達可能性に関する節を追加
    add_reachability_clauses(i, j, clause)

    # 黒マスの数
    for a in X:
        if ob((i, j), a):
            # マス(i,j)は盤面の端なので黒マスはない
            clause.append([Vn(i,j,a,0)])
            for m in range(1, max(W, H)+1):
                clause.append([-Vn(i,j,a,m)])
        else:
            # a方向の黒マスの数
            x, y = a((i, j))
            for m in range(0, max(W, H)+1):
                clause.append([-Vn(x,y,a,m), Vn(i,j,a,m)])
            for m in range(1, max(W, H)+1):
                clause.append([-Vn(x,y,a,m-1), -Vb(x,y), Vn(i,j,a,m)])
                clause.append([-Vn(i,j,a,m), Vn(x,y,a,m), Vn(x,y,a,m-1)])
                clause.append([-Vn(i,j,a,m), Vn(x,y,a,m), Vb(x,y)])

    # マス(i,j)に矢印aと数字kが書かれている
    if (i,j) in digit:
        k, a = digit[(i, j)]
        clause.append([ Vn(i,j,a,k)])
        clause.append([-Vn(i,j,a,k+1)])


# CNFファイル出力
print('Writing a CNF file', file=stderr)
print("p cnf {} {}".format(Vlast, len(clause)))
for c in clause:
    print(' '.join(map(str, c)), 0)
