# read_pdf.pyの設定
# 処理を行う最初のページ（pdfviewerで確認した値）-①
first_page: int = 32

# 処理を行う最初のページに記載されているページ数（pdfの画像内にある値）-②
first_page_in_book: int = 26

# 処理を行う最後のページ（pdfviewerで確認した値）-③
last_page: int = 447

# pdfのパス
pdf_path: str = "book.pdf"

# search_split_point_candidate.pyの設定
# 検索する文字サイズの最小値 -④
min_font_size: int = 10
# 検索する文字サイズの最大値 -⑤
max_font_size: int = 30


# create_prompt.pyの設定
# 入力する命令 -⑥
order: str = '''あなたはプロの編集者です。以下の制約条件に従って、入力する文章を箇条書きで要約してください。
#制約条件
・架空の表現や言葉を使用しない。
・文章中の数値には変更を加えない。
・各要素に対応する文章の頭のページ番号を箇条書きの末尾につける。
・「だ・である調」で要約する。
・体言止めをしない。
・全てのページについて、1ページにつき1つ以上は要素を書き出す。
・要約の要素数は多すぎるくらいにする。
・要約の数は30個以上出力する。
#要約例
 - マスコミはこれらの本をまともなものとして扱っていた (p.25)
 - 1987年12月27日、テレビ東京は「国際ユダヤ資本家」のドキュメンタリーを全国放映 (p.25-26)
#入力
'''

# summary.pyの設定
# temperatureの設定
temperature: float = 0.01
# top_pの設定
top_p: float = 1
# max_tokensの設定
max_tokens: int = 3500
# 実行時のsleep時間 -⑦
sleep_time: int = 30
# 実行時に同時に処理する数 -⑧
worker_count: int = 2