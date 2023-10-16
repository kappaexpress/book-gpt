import os
import pandas as pd
import pickle
import fitz
import settings


# 縦書きのみのテキストを抽出する関数
def extract_vertical_text(page: fitz.fitz.Page) -> pd.DataFrame:
    out: list = []

    for block in page.get_text("dict")["blocks"]:
        try:
            for lines in block["lines"]:
                if (lines["dir"] == (0.0, 1.0)):
                    for span in lines["spans"]:
                        out.append(span)
        except KeyError:
            continue

    df = pd.DataFrame(out)
    return df


# bboxの列をパースする関数
def parse_bbox(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df["bbox_0"] = df["bbox"].apply(lambda x: x[0])
        df["bbox_1"] = df["bbox"].apply(lambda x: x[1])
        df["bbox_2"] = df["bbox"].apply(lambda x: x[2])
        df["bbox_3"] = df["bbox"].apply(lambda x: x[3])
        return df
    except KeyError:
        # 空のdfを返す
        return pd.DataFrame()


# 1列の幅を計算する関数
def calc_line_width(df: pd.DataFrame) -> pd.DataFrame:
    df["line_width"] = df["bbox_2"] - df["bbox_0"]
    return df


# 列間の幅を計算する関数
def calc_between_line(df: pd.DataFrame) -> pd.DataFrame:
    df["bbox_2_shift"] = df["bbox_2"].shift(-1)
    df["between_line"] = df["bbox_0"] - df["bbox_2_shift"]
    return df


# ページごとにdfを作成する関数
def create_df_from_page(page: fitz.fitz.Page) -> pd.DataFrame:
    # 縦書きのみのテキストを抽出する
    df: pd.DataFrame = extract_vertical_text(page)

    # bboxの列をパースする
    df = parse_bbox(df)

    # dfが空の場合はcontinueする
    if df.empty:
        return df

    # 1列の幅を計算する
    df = calc_line_width(df)

    # 列間の幅を計算する
    df = calc_between_line(df)

    return df


if __name__ == "__main__":
    # tmpディレクトリを作成する
    os.makedirs("tmp", exist_ok=True)

    # pdfを読み込む
    doc: fitz.fitz.Document = fitz.open(settings.pdf_path, filetype="pdf")

    # 処理するページを指定する
    page_range = range(settings.first_page, settings.last_page + 1)

    # ページごとにdfを作成する
    dfs = []

    for page_num in page_range:
        print(f"page_num: {page_num}")

        # ページを読み込む
        page: fitz.fitz.Page = doc.load_page(page_num)

        # ページごとにdfを作成する
        df: pd.DataFrame = create_df_from_page(page)

        # ページ番号を追加する(本のページ番号と合わせるように調整が必要)
        df["page_num"] = page_num - settings.page_num_adjustment

        # ページごとのdfをリストに追加する
        dfs.append(df)

    # ページごとのdfを結合する
    df = pd.concat(dfs, ignore_index=True)

    # dfをpickleに出力する
    with open("tmp/df.pickle", "wb") as f:
        pickle.dump(df, f)
