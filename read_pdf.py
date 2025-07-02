import pandas as pd
import fitz
import pickle
import multiprocessing
import os
import settings


# textのdictをdataframeに変換する関数
def dict_to_dataframe_2(texts: dict, page_num: int) -> pd.DataFrame:
    print(f"page_num: {page_num}")

    out = []
    for i_b, block in enumerate(texts["blocks"]):
        if "lines" not in block:  # linesキーがない場合はスキップ
            continue

        for i_l, line in enumerate(block["lines"]):
            for i_s, span in enumerate(line["spans"]):
                for i_c, char in enumerate(span["chars"]):
                    char_data = (
                        char["bbox"][0],
                        char["bbox"][1],
                        char["bbox"][2],
                        char["bbox"][3],
                        char["c"],
                        i_b,
                        i_l,
                        i_s,
                        i_c,
                    )
                    out.append(char_data)

    # columnsはx0, y0, x1, y1, char, block_no, line_no, word_no, char_no
    df = pd.DataFrame(
        out,
        columns=[
            "x0",
            "y0",
            "x1",
            "y1",
            "char",
            "block_no",
            "line_no",
            "span_no",
            "char_no",
        ],
    )

    # pdfviewerで確認した値に合わせる
    df["page_no"] = page_num + 1

    return df


# すべてのページを読み込む関数
def read_all_pages(doc: fitz.Document) -> pd.DataFrame:
    # すべてのページをdataframeに変換
    args: list = [(page.get_text("rawdict"), page.number) for page in doc]

    # マルチプロセスで処理
    with multiprocessing.Pool() as pool:
        out: list = pool.starmap(dict_to_dataframe_2, args)

    # すべてのページを結合
    return pd.concat(out)


# メイン関数
def main():
    # tmpディレクトリがなければ作成
    os.makedirs("tmp", exist_ok=True)

    doc: fitz.Document = fitz.open(settings.pdf_path, filetype="pdf")

    df: pd.DataFrame = read_all_pages(doc)

    # pickleで保存
    with open("tmp/df.pickle", "wb") as f:
        pickle.dump(df, f)


if __name__ == "__main__":
    main()
