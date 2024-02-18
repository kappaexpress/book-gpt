# read_pdf.pyの設定
# 書籍内で1ページ目が記載されているページの番号（pdfviewerで確認した値）
first_page_in_book: int = 9
# 処理を行う最初のページ（pdfviewerで確認した値）
first_page: int = 9
# 処理を行う最後のページ（pdfviewerで確認した値）
last_page: int = 268
# pdfのパス
pdf_path: str = "book.pdf"

# search_split_point_candidate.pyの設定
# 検索する文字サイズの最小値
min_font_size: int = 20
# 検索する文字サイズの最大値
max_font_size: int = 100


# create_prompt.pyの設定
# GPTに入力する命令
order: str = '''
あなたはプロの編集者です。以下の制約条件に従って、入力する文章を箇条書きで要約してください。
#制約条件
・重要なキーワードを取りこぼさない。
・文章の意味を変更しない。
・架空の表現や言葉を使用しない。
・文章中の数値には変更を加えない。
・各要素に対応する文章の頭のページ番号をつける。
・「だ・である調」で要約する。
#要約例
 - マスコミはこれらの本をまともなものとして扱っていた (p.25)
 - 1987年12月27日、テレビ東京は「国際ユダヤ資本家」のドキュメンタリーを全国放映 (p.25-26)
#入力
'''

# summary.pyの設定
# モデルの設定
model: str = "gpt-4-turbo-preview"
# temperatureの設定
temperature: float = 0.01
# top_pの設定
top_p: float = 1
# max_tokensの設定
max_tokens: int = 1006
# 実行時のsleep時間(短いとRate Limitのエラーが発生する)
sleep_time: int = 30