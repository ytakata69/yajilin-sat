# Yajilin-Sat

ヤジリン問題をSATソルバで解く
（& 結果を[Matplotlib](https://matplotlib.org)で描画する）．    
Solve [Yajilin](https://www.nikoli.co.jp/en/puzzles/yajilin.html) problems
with a SAT solver (and draw the solution with
[Matplotlib](https://matplotlib.org)).

<img src="https://raw.githubusercontent.com/wiki/ytakata69/yajilin-sat/yajilin-sat.png" width="400" />

(上図は下記ページに掲載の例題を解いた様子．
The above figure is the solution of the sample problem in the
following Web page.)

- [ヤジリンの遊び方，ルール，解き方 | WEBニコリ](https://www.nikoli.co.jp/ja/puzzles/yajilin/)
  ([English page](https://www.nikoli.co.jp/en/puzzles/yajilin.html))

## 準備 - Preliminaries

下記が必要です (Required):

- [Minisat](http://minisat.se)（または他のSATソルバ）(Other SAT solvers may also work.)
- Python 3
- [Matplotlib](https://matplotlib.org) - 解の描画に使用 (Used for drawing solutions)

オプション (Optional):

- [PyPy 3](https://pypy.org) - SAT符号化器 (`yajisat.py`) の動作が数倍程度速くなります．
  (Using Pypy 3, the SAT encoder `yajisat.py` may run about five or six times faster.)

Python処理系の選択 (The interpreter selection sequence):

- 下記のように動作します．コマンド名等がちがう場合は各スクリプトの先頭部分を修正してください．
  (The programs in this repository select a Python interpreter as follows. If your interpreter has another name, please modify the first several lines of each script.)
  - `yajisat.py` は `pypy3`, `pypy`, `python3`, `python` の順に探して自動選択します．
    (`yajisat.py` automatically selects the first existing interpreter in the following list: `pypy3`, `pypy`, `python3`, `python`.)
  - `draw.py` は `python3` を使います．
    (`draw.py` uses `python3`.)

## 使い方 - How to use

- 上図の例題をSAT符号化して解き，結果を表示します．
  (Solve the sample problem in the above figure, and then draw the solution.)

  ```sh
  $ make
  ```
- 問題記述ファイルを入力し，それを解いた結果を表示します．[ぱずぷれv3](https://github.com/sabo2/pzprv3/)形式のファイルも指定可能です．
  (Solve the problem given in the specified text file, and then draw the solution. You can also specify a file in the [PUZ-PRE v3](https://github.com/sabo2/pzprv3/) format.)

  ```sh
  $ make INPUT=otameshi1.yaj
  ```
- SAT符号化についての文書 (`yajilin.tex`) を組版します．
  (Typeset the document about the SAT encoding (`yajilin.tex`).)

  ```sh
  $ make pdf
  ```

### 入力ファイル - Input File Format

問題記述ファイルの構文は `otameshi1.yaj` 中のコメントを参照してください．
(Please see the comments written in `otameshi1.yaj` that describe the format of the input files.)

また，[ぱずぷれv3](https://github.com/sabo2/pzprv3/)形式のファイルも入力できます．ファイル形式はファイルの先頭行で判断します．
(The SAT-encoding program also accepts text files in [PUZ-PRE v3](https://github.com/sabo2/pzprv3/) format.
It distinguishes the file formats by looking the first line of that file.)

## SAT符号化 - SAT Encoding

ごく普通の符号化法を使っています．    
Plain encoding methods were adopted.

- 黒マスの個数: n個の中からk個 ([k-out-of-n](https://cs.stackexchange.com/questions/13188/encoding-1-out-of-n-constraint-for-sat-solvers))    
  (A ["k-out-of-n"](https://cs.stackexchange.com/questions/13188/encoding-1-out-of-n-constraint-for-sat-solvers) method is used for checking the number of black cells.)
- 一つの輪っか: マス間の接続関係の推移閉包    
  (Compute the transitive closure of the linking relation between two cells for checking that the lines form a single loop.)

普通の大きさのヤジリン問題の場合，マスの個数nに対して符号化後のCNF式の長さがO(n<sup>2</sup>)なら符号化・求解とも十分速くできますが，O(n<sup>3</sup>)だとかなり重くなります（前者なら36&times;20の問題でも符号化・求解できますが，後者だと難しいです）．    
推移閉包を求める式の長さをO(n<sup>2</sup>)に抑える簡単な工夫（符号化前に，黒マスにならないことが確実なマスを1個見つけておく）を行っています．    
When the size of the resultant CNF formula is O(n<sup>2</sup>) for the number n of cells,
you can encode and solve that problem sufficiently fast (and you can solve a problem with 36&times;20 cells in a practical time).
However, when that size is O(n<sup>3</sup>), encoding and solving a Yajilin problem takes much time, even for a problem with 10&times;10 cells.    
To make the size of the CNF formula for computing the transitive closure O(n<sup>2</sup>),
before the encoding the SAT encoder looks for a cell that never be black
and then generates formulae only for checking the reachability from that cell.

SAT符号化の詳細は `yajilin.tex` を参照してください（[PDF](https://raw.githubusercontent.com/wiki/ytakata69/yajilin-sat/yajilin.pdf)）．    
Please see `yajilin-en.tex` and its [PDF](https://raw.githubusercontent.com/wiki/ytakata69/yajilin-sat/yajilin-en.pdf)
for the details of the SAT encoding.
