import pickle
import os
import pandas as pd
import settings


# データの中身を確認する関数
def check_df(df: pd.DataFrame) -> None:
    # Dataframeの末尾のインデックスを取得する
    last_index = df.index[-1]
    for c in df.columns:
        print(c, df.at[0, c])
        print(c, df.at[last_index, c])

    # page_numのtext, size, between_lineを表示する
    print(
        df[df["page_num"] == (settings.first_page - settings.page_num_adjustment)][
            ["text", "size", "between_line"]
        ]
    )
    print(
        df[df["page_num"] == settings.last_page - settings.page_num_adjustment][
            ["text", "size", "between_line"]
        ]
    )
    print(df[df["page_num"] == 166][["text", "size", "between_line"]])

    exit()


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

    # 列幅が一定以上か否かを判定する列を追加する
    df["width_is_over"] = df["between_line"].apply(
        lambda x: x > settings.width_threshold
    )

    # between_lineがNaNの行はwidth_is_overをTrueにする
    # (タイトルだけのページかもしれないから)
    df.loc[df["between_line"].isnull(), "width_is_over"] = True

    # width_is_overがTrueの行のみを抽出する
    df = df[df["width_is_over"] == True]

    # sizeが15以上の行のみを抽出する
    df = df[df["size"] >= settings.font_size_threshold]

    # width_is_overがTrueの行のみ表示する
    print(df[["text", "page_num", "size"]])

    # width_is_overがTrueの行のみCSVに出力する
    df[["text", "page_num", "size", "between_line", "width_is_over"]].to_csv(
        "tmp/split_point_candidate.csv", index=True
    )

    # split_point.csvというファイルを作成する
    # すでに存在する場合は、作成しない
    if not os.path.exists("tmp/split_point.csv"):
        with open("tmp/split_point.csv", "w") as f:
            # 1行目に列名を書き込む
            f.write("split_point\n")