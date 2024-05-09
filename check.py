import pickle
import pandas as pd


# データの中身を確認する関数
def check_df(df: pd.DataFrame) -> None:

    # 8
    check_df_page(df, 80)
    # 269
    check_df_page(df, 269)


# 特定のページのデータの中身を確認する関数
def check_df_page(df: pd.DataFrame, page_num: int) -> None:

    # page_numのデータのchar, block_no, page_noを表示
    print(df[df["page_no"] == page_num][["char", "block_no", "page_no"]].head(12))

    print("\n")

    # page_numのデータのblock_no==0のcharを結合して表示
    print(
        df[(df["page_no"] == page_num) & (df["block_no"] == 0)][["char"]].apply(
            lambda x: "".join(x)
        )
    )


if __name__ == "__main__":

    # データの読み込み
    with open("tmp/df.pickle", "rb") as f:
        data = pickle.load(f)

    # データの中身を確認
    check_df(data)
