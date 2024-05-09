# 作業手順

## 初回セットアップ
```bash
poetry shell
```

## 要約実行
1. pdfをローカルで開く
2. 本の目次、構成を確認する
3. 要約する最初のページを確認する
4. `settings.py`の`first_page`①に要約する最初のページのpdfのviewerでのページ番号を設定する
5. `settings.py`の`first_page_in_book`②に要約する最初のページの画像にあるページ番号を設定する
6. `settings.py`の`last_page`③に要約する最後のページのpdfのviewerでのページ番号を設定する
7. 本のpdfをアップロードし、`book.pdf`に名前を変更する
8. `read_pdf.py`を実行する
```bash
python read_pdf.py
```
9. `search_split_point_candidate.py`を実行する
```bash
python search_split_point_candidate.py
```
10. `tmp/split_point_candidate.csv`が生成されるので、確認し、過不足があれば修正する
11. 10を`tmp/split_point.csv`にコピーする
12. `create_prompt.py`を実行する
```bash
python create_prompt.py
```
13. `prompt/XXXX.txt`が生成されるので、確認し、異常があれば修正する
14. `summary_all.py`を実行する
```bash
python summary_all.py
```
15. `summary/XXXX.txt`が生成されるので、確認し、異常があれば、パラメータの調整などを行い、`summary_all.py`や`summary_at_once.py`を実行する
16. 15を繰り返し、すべてのsummaryが正常になったら、`join_summary.py`を実行する
```bash
python join_summary.py
```
17. `tmp/summary.docx`が生成されるので、確認し、異常があれば修正する


## ディレクトリとファイル

### `__pycache__`
- Pythonスクリプトの読み込み時間を改善するためのコンパイル済みPythonファイルが含まれています。

### `prompt`
- 処理またはテスト用の入力テキストが格納されているテキストファイル (`0000.txt` から `0017.txt`)。

### `summary`
- `prompt` ディレクトリの対応するファイルから生成された要約テキストファイル。

### `tmp`
- 中間処理ステップで使用される可能性のある `df.pickle`（シリアライズされたデータフレーム）、`index.csv`、`split_point.csv`、`split_point_candidate.csv` などのデータファイルが一時的に保存されています。
- `summary.docx` はすべての要約を含むドキュメントである可能性があります。

## Python スクリプト

- `check.py`: ファイルやデータの整合性または形式をチェックする可能性があります。
- `create_prompt.py`: `prompt` ディレクトリに保存されている入力テキストを生成する可能性があります。
- `join_summary.py`: 複数の要約ファイルを単一のドキュメントや出力形式に組み合わせる可能性があります。
- `read_pdf.py`: PDFファイル (`book.pdf`) から内容を読み取り、抽出するスクリプト。
- `search_split_point_candidate.py`: 要約プロセスで使用されるテキストを分割する可能性のあるポイントを見つけるスクリプト。
- `settings.py`: プロジェクトの設定を含む。
- `summary_all.py`: すべての入力テキストを一度に要約する可能性のあるスクリプト。
- `summary_at_once.py`: 要約プロセスに関連する別のスクリプトで、`summary_all.py`の別のアプローチかもしれません。

### 設定ファイル

- `pyproject.toml`: Pythonパッケージ管理のためのツールを設定する。
- `poetry.lock`: インストールの一貫性を保証するためのロックファイル。

### その他のファイル

- `README.md`: このプロジェクトの概要を説明するマークダウンファイル。
- `book.pdf`: テキストが抽出され処理されるソースPDFドキュメント。