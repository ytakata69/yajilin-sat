# Yajilin-Sat

ヤジリン問題をSATソルバで解く
（& 結果を[Matplotlib](https://matplotlib.org)で描画する）．

<img src="https://raw.githubusercontent.com/wiki/ytakata69/yajilin-sat/yajilin-sat.png" width="300" />

（上図は下記ページに掲載の例題を解いた様子．）

- [ヤジリンの遊び方，ルール，解き方 | WEBニコリ](https://www.nikoli.co.jp/ja/puzzles/yajilin/)

## 準備

下記が必要です．

- [Minisat](http://minisat.se)（または他のSATソルバ）
- Python 3
- [Matplotlib](https://matplotlib.org) - 解の描画に使用

オプション:

- [PyPy 3](https://pypy.org) - SAT符号化器 (`yajisat.py`) の動作が数倍程度速くなります．

Python処理系の選択:

- 下記のように動作します．コマンド名等がちがう場合は各スクリプトの先頭部分を修正してください．
  - `yajisat.py` は `pypy3`, `pypy`, `python3`, `python` の順に探して自動選択します．
  - `draw.py` は `python3` を使います．

## 使い方

- 上図の例題をSAT符号化して解き，結果を表示します．

  ```sh
  $ make clean
  $ make
  ```
- 問題記述ファイルを入力し，それを解いた結果を表示します．

  ```sh
  $ make clean
  $ make INPUT=otameshi1.yaj
  ```
- SAT符号化についての文書 (`yajilin.tex`) を組版します．

  ```sh
  $ make pdf
  ```

問題記述ファイルの構文は `otameshi1.yaj` 中のコメントを参照してください．

## SAT符号化

`yajilin.tex` に説明を記述しました（[PDF](https://raw.githubusercontent.com/wiki/ytakata69/yajilin-sat/yajilin.pdf)）．
