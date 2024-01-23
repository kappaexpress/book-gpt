import os
import pandas as pd
import pickle
import fitz


# bboxの列をパースする関数
def parse_bbox(df: pd.DataFrame) -> pd.DataFrame:
    df["bbox_0"] = df["bbox"].apply(lambda x: x[0])
    df["bbox_1"] = df["bbox"].apply(lambda x: x[1])
    df["bbox_2"] = df["bbox"].apply(lambda x: x[2])
    df["bbox_3"] = df["bbox"].apply(lambda x: x[3])
    return df


# bboxの値から1行の大きさを計算する関数
def calc_line_size_for_horizontal_text(df: pd.DataFrame) -> float:
    df["bbox_width"] = df["bbox_2"] - df["bbox_0"]
    df["bbox_height"] = df["bbox_3"] - df["bbox_1"]

    bbox_width_sum: float = df["bbox_width"].sum()
    df["bbox_width_ratio"] = df["bbox_width"] / bbox_width_sum
    df["bbox_height_ratio"] = df["bbox_height"] * df["bbox_width_ratio"]
    size = df["bbox_height_ratio"].sum()

    return size


# pageをdataframeに変換する関数
def page_to_dataframe(page: fitz.fitz.Page) -> pd.DataFrame:
    out: dict = {}
    texts: dict = page.get_textpage().extractDICT()
    page_num: int = page.number
    line_num: int = 0

    for block in texts["blocks"]:
        for line in block["lines"]:
            df_line: pd.DataFrame = pd.DataFrame(line["spans"])
            df_line = parse_bbox(df_line)

            one_line_size: float = calc_line_size_for_horizontal_text(df_line)
            one_line_text: str = df_line["text"].str.cat(sep="")
            out[f"{page_num}_{line_num}"] = {
                "page_num": page_num,
                "line_num": line_num,
                "text": one_line_text,
                "size": one_line_size,
            }
            line_num += 1

    return pd.DataFrame(out).T


# すべてのページを読み込む関数
def read_all_pages(doc: fitz.fitz.Document) -> pd.DataFrame:
    out: list = []

    for page in doc:
        df: pd.DataFrame = page_to_dataframe(page)

        # ページ番号を追加
        page_id: int = page.number
        df["page_id"] = page_id

        if page_id == 30:
            exit()

        # bboxの列をパース
        df = parse_bbox(df)
        out.append(df)

    # すべてのページを結合&indexを振り直す
    df = pd.concat(out).reset_index(drop=True)
    return df


if __name__ == "__main__":
    doc: fitz.fitz.Document = fitz.open("book_2.pdf", filetype="pdf")

    # dfの日本語を表示する際にずれないようにする
    pd.set_option("display.unicode.east_asian_width", True)

    # dfの1行の文字数を増やす
    pd.set_option("display.max_colwidth", 1000)

    for i in range(100):
        df = page_to_dataframe(doc[i])
        try:
            print(df["text"])
        except KeyError:
            continue
