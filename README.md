# load_fillet_gmail

## 使い方
### 前準備
- Gmailに送られてきたFilletからのメール（今回催事の追加分）に任意のラベルをつける
- .envのLABEL_NAMEの値を、今つけたラベル名称に修正する
---
### 実行
- 下記コマンドで製品シートに製品名称、分量を自動追加

（メール1単位に2つ以上連結されている可能性に注意すること）
```python
python src/run_write_product_summary_if_necessary.py
```
- 下記コマンドで自動的に領域展開する
```python
python src/run_write_mixture_with_amount.py
```
- 下記コマンドで自動的に類似度を計算する
```python
python src/run_calc_and_write_mixture_similarity.py
```
---
### 最終処理
- アダプタを手作業で調整する（まだない材料は新規作成する）
（アダプタシートのB列とG列にそれぞれ領域展開シートのC列と適切な値(H列、材料名称など)を入れる）
- 下記再度実行
```python
python src/run_calc_and_write_mixture_similarity.py
```
- 領域展開シートから製品構成シートへ手動でコピーする（水色の列をコピーする）
- 製品シートの「一回の生産量[個]」が1の各製品は、「一個の重さ[g/個]」が空になっているので、その右隣の列の値を参考に計算して入力する。
---
以上
