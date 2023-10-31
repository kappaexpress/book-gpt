# read_pdf.pyの設定
# 本とページ番号を合わせるために引く数
page_num_adjustment: int = 9
# 処理を行う最初のページ
first_page: int = 10
# 処理を行う最後のページ
last_page: int = 215
# pdfのパス
pdf_path: str = "book.pdf"

# search_split_point_candidate.pyの設定
# 列幅の閾値
width_threshold: int = 13
# フォントサイズの閾値
font_size_threshold: int = 9.5

# create_prompt.pyの設定
# 1つのpromptに含めるページ数
page_in_prompt: int = 2
# GPTに入力する命令
order: str = '''
#制約条件
・重要なキーワードを取りこぼさない。
・文章の意味を変更しない。
・架空の表現や言葉を使用しない。
・文章中の数値には変更を加えない。
・10個の箇条書きに要約する。
・各要素に対応する文章の頭のページ番号をつける。
・「だ・である調」で要約する。
#要約例
 - マスコミはこれらの本をまともなものとして扱っていた (p.25)
 - 1987年12月27日、テレビ東京は「国際ユダヤ資本家」のドキュメンタリーを全国放映 (p.25-26)
#入力'''

# summary.pyの設定
# GPTに与える文脈
context: str = '''あなたはプロの編集者です。以下の制約条件に従って、入力する文章を箇条書きで要約してください。'''
# モデルの設定
model: str = "gpt-3.5-turbo"
# temperatureの設定
temperature: float = 0.01
# top_pの設定
top_p: float = 1
# max_tokensの設定
max_tokens: int = 1006
# 実行時のsleep時間(短いとRate Limitのエラーが発生する)
sleep_time: int = 20