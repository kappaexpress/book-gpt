import pickle
import pandas as pd
import settings
from scipy.stats import trim_mean


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

    # charが" "の行を削除
    df = df[df["char"] != " "]

    df["height"] = df["y1"] - df["y0"]

    # blockごとの文字を結合する
    df_text = df.groupby(["page_no", "block_no"])["char"].apply(lambda x: "".join(x))

    # blockごとの文字の高さの平均値を計算する
    df_size = df.groupby(["page_no", "block_no"])["height"].apply(
        lambda x: trim_mean(x, 0.3)
    )

    # df_textとdf_heightを結合する
    df = pd.concat([df_text, df_size], axis=1)

    # 文字の高さを最小値と最大値でフィルタリングする
    df_out = df[
        (df["height"] > settings.min_font_size)
        & (df["height"] < settings.max_font_size)
    ]

    # page_noをfirst_pageとlast_pageでフィルタリングする
    df_out = df_out[
        (df_out.index.get_level_values("page_no") >= settings.first_page - 1)
        & (df_out.index.get_level_values("page_no") <= settings.last_page - 1)
    ]

    # split_point_candidate.csvを保存する
    df_out[["height", "char"]].to_csv("tmp/split_point_candidate.csv", index=True)
