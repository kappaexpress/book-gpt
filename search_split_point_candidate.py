import pickle
import os
import pandas as pd
import settings
from scipy.stats import trim_mean


# データの中身を確認する関数
def check_df(df: pd.DataFrame) -> None:
    
    check_df_page(df, 303)

    exit()


# 特定のページのデータの中身を確認する関数
def check_df_page(df: pd.DataFrame, page_num: int) -> None:
    print(f"page_num: {page_num}")
    # page_numのデータを表示
    print(df[df["page_no"] == page_num])
    print("\n")


if __name__ == "__main__":
    # 1列に表示する文字数を指定する
    pd.set_option("display.max_colwidth", 30)

    # 表示する行数を指定する
    pd.set_option("display.max_rows", 200)

    # 表示する際に日本語がずれるのを防ぐ
    pd.set_option("display.unicode.east_asian_width", True)

    # df.pickleを読み込む
    with open("tmp/df.pickle", "rb") as f:
        df = pickle.load(f)

    # データの中身を確認する
    check_df(df)

    # charが" "の行を削除
    df = df[df["char"] != " "]

    df["height"] = df["y1"] - df["y0"]

    df_text = df.groupby(["page_no", "block_no"])["char"].apply(lambda x: "".join(x))

    df_size = df.groupby(["page_no", "block_no"])["height"].apply(
        lambda x: trim_mean(x, 0.3)
    )

    # df_textとdf_heightを結合する
    df = pd.concat([df_text, df_size], axis=1)

    df_out = df[
        (df["height"] > settings.min_font_size)
        & (df["height"] < settings.max_font_size)
    ]

    # split_point_candidate.csvを保存する
    df_out[["height", "char"]].to_csv("tmp/split_point_candidate.csv", index=True)
