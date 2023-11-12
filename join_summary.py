import docx
import pandas as pd


if __name__ == '__main__':
    # tmp/index.csvを読み込む
    df = pd.read_csv('tmp/index.csv')

    # docxを新規作成
    doc = docx.Document()

    # loop_split_rangeを初期化する
    loop_split_range = df.at[0, 'split_range']

    # docxにsplit_rangeを見出しとして追加する
    doc.add_heading(loop_split_range, level=1)

    # dfをforループで処理する
    for index, row in df.iterrows():
        # summaryから呼び込むためのファイルパスに変更する
        summary_path = row['file_name'].replace('prompt', 'summary')

        # summaryを読み込む
        with open(summary_path) as f:
            summary = f.read()
        
        # その行のsplit_rangeがloop_split_rangeと異なる場合
        if row['split_range'] != loop_split_range:
            # docxに改ページを追加する
            # doc.add_page_break()
            
            # loop_split_rangeを更新する
            loop_split_range = row['split_range']

            # titleを変数に格納する
            title = row['title']

            # docxにsplit_rangeを追加する
            doc.add_heading(loop_split_range+" "+title, level=1)
        
        # docxにsummaryを追加する
        doc.add_paragraph(summary)
    
    # docxを保存する
    doc.save('tmp/summary.docx')
