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

`yajilin.tex` に説明を記述しました（[PDF](https://raw.githubusercontent.com/wiki/ytakata69/yajilin-sat/yajilin.pdf)）．    
Please see `yajilin.tex` and its [PDF](https://raw.githubusercontent.com/wiki/ytakata69/yajilin-sat/yajilin.pdf)
for the details of the SAT encoding.
