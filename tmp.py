import pickle
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import trim_mean


if __name__ == "__main__":
    # 1行に表示する文字数を設定
    pd.set_option("display.max_colwidth", 40)

    # 表示する行数を設定
    pd.set_option("display.max_rows", 100)

    # 日本語の表示がそろうようにする
    pd.set_option("display.unicode.east_asian_width", True)

    # 保存したファイルを読み込む
    with open("tmp/df.pickle", "rb") as f:
        df = pickle.load(f)
    
    
    # charが" "の行を削除
    df = df[df["char"] != " "]

    df["height"] = df["y1"] - df["y0"]

    df_text = df.groupby(["page_no", "block_no"])["char"].apply(lambda x: "".join(x))

    df_size = df.groupby(["page_no", "block_no"])["height"].apply(
        lambda x: trim_mean(x, 0.3)
    )

    # df_textとdf_heightを結合する
    df = pd.concat([df_text, df_size], axis=1)

    # csvで保存
    df.to_csv("tmp/df.csv")

    # heightが13~16の行を表示
    print(df[(df["height"] > 14) & (df["height"] < 18)])
