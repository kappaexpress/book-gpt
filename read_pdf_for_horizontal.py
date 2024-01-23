import pandas as pd
import fitz
import pickle


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
def page_to_dataframe(page: fitz.Page) -> pd.DataFrame:
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
                "bbox_0": line["bbox"][0],
                "bbox_1": line["bbox"][1],
                "bbox_2": line["bbox"][2],
                "bbox_3": line["bbox"][3],
            }
            line_num += 1

    return pd.DataFrame(out).T


# すべてのページを読み込む関数
def read_all_pages(doc: fitz.Document) -> pd.DataFrame:
    # すべてのページをdataframeに変換
    out: list = [page_to_dataframe(page) for page in doc]

    # すべてのページを結合
    return pd.concat(out)


if __name__ == "__main__":
    doc: fitz.Document = fitz.open("book_2.pdf", filetype="pdf")

    df: pd.DataFrame = read_all_pages(doc)

    # pickleで保存
    with open("tmp/df.pickle", "wb") as f:
        pickle.dump(df, f)
