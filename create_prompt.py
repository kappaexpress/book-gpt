import os
import pandas as pd
import pickle
import settings


# tmp/split_point.csvを読み込む関数
def read_split_point() -> pd.DataFrame:
    return pd.read_csv("tmp/split_point.csv")


# tmp/df.pickleを読み込む関数
def read_df_book() -> pd.DataFrame:
    with open("tmp/df.pickle", "rb") as f:
        return pickle.load(f)


# dfをsplit_pointとend_split_pointで分割する関数
def split_df(
    df: pd.DataFrame, split_point: int, end_split_point: int, text: str
) -> pd.DataFrame:
    # dfをsplit_pointとend_split_pointで分割する
    df_splited = df.iloc[split_point:end_split_point]

    df_splited = df_splited.copy(deep=True)

    # df_splitedにsplit_pointとend_split_pointを追加する
    df_splited["split_range"] = "{}-{}".format(split_point, end_split_point)

    # df_splitedにtitleを追加する
    df_splited["title"] = text
    return df_splited


# 文字列に句点が含まれているかどうかを判定する関数
def is_contain_period(text: str) -> bool:
    return "。" in text


# 文字列の句点の位置を取得する関数
def get_period_index(text: str) -> int:
    # 句点がない場合は-1を返す
    if not is_contain_period(text):
        return -1
    else:
        return text.index("。")


# dfのtext列をページごとに分割する関数
def split_text_by_page(df: pd.DataFrame) -> pd.DataFrame:
    # df_splitの先頭の行のtext列に改行を追加する
    df.iloc[0, df.columns.get_loc("text")] = (
        df.iloc[0, df.columns.get_loc("text")] + "\n"
    )

    # dfのtext列をpage_numの値ごとに結合する
    text_by_page = df.groupby("page_num")["text"].sum()

    # text_by_pageのindexを列に変換する
    text_by_page = text_by_page.reset_index()

    # text_by_pageにsplit_range列を追加する
    text_by_page["split_range"] = df.iat[0, df.columns.get_loc("split_range")]

    # text_by_pageにtitle列を追加する
    text_by_page["title"] = df.iat[0, df.columns.get_loc("title")]

    # text_by_pageのtext列に最初に現れる句点の位置を取得する
    text_by_page["period_index"] = text_by_page["text"].apply(get_period_index)

    # text_by_pageのtext列のperiod_indexまでの文字列を取得する
    text_by_page["before_period_index"] = text_by_page.apply(
        lambda row: row["text"][: row["period_index"] + 1], axis=1
    )

    # text_by_pageのtext列のperiod_indexまでの文字列を削除する
    text_by_page["text"] = text_by_page.apply(
        lambda row: row["text"][row["period_index"] + 1 :], axis=1
    )

    # text_by_pageのbefore_period_index列をshiftして、1つずらした列を追加する
    text_by_page["next_before_period_index"] = text_by_page[
        "before_period_index"
    ].shift(-1)

    # text_by_page["next_before_period_index"]のNaNを空文字に置換する
    text_by_page["next_before_period_index"] = text_by_page[
        "next_before_period_index"
    ].fillna("")

    # text_by_pageのtext列の末尾にnext_before_period_index列を追加する
    text_by_page["text"] = (
        text_by_page["text"] + text_by_page["next_before_period_index"]
    )

    # 先頭の行のtext列にbefore_period_index列を追加する
    text_by_page.iloc[0, text_by_page.columns.get_loc("text")] = (
        text_by_page.iloc[0, text_by_page.columns.get_loc("before_period_index")]
        + text_by_page.iloc[0, text_by_page.columns.get_loc("text")]
    )

    return text_by_page


# text_by_pageのtext列を結合する関数
def combine_text_by_page(text_by_page: list[pd.DataFrame]) -> list[str]:
    output: list[str] = []

    for df in text_by_page:
        # dfのpage_num列に"p."を追加する
        df["page_num"] = "\np." + df["page_num"].astype(str) + "\n"

        # dfのtext列の先頭にpage_num列を追加する
        df["text"] = df["page_num"] + df["text"]

        # dfのtext列を塊ごとに結合する
        prompt = df.groupby(df.index // settings.page_in_prompt)["text"].sum()

        # promptにORDERを追加する
        prompt = settings.order + prompt

        # split_rangeを変数に格納する
        split_range = df.iat[0, df.columns.get_loc("split_range")]

        # titleを変数に格納する
        title = df.iat[0, df.columns.get_loc("title")]

        # promptをリストに追加する
        for p in prompt.to_list():
            output.append({"split_range": split_range, "prompt": p, "title": title})

    return output


if __name__ == "__main__":
    # split_point.csvを読み込む
    split_point = read_split_point()

    # df_bookを読み込む
    df_book = read_df_book()

    # split_pointをshiftして、1つずらした列を追加する
    split_point["end_split_point"] = split_point["split_point"].shift(-1)

    # split_pointの最後の行のend_split_pointをdf_bookの行数に置換する
    split_point.iloc[-1, split_point.columns.get_loc("end_split_point")] = len(df_book)

    # end_split_pointをint型に変換する
    split_point["end_split_point"] = split_point["end_split_point"].astype(int)

    # end_split_pointとsplit_pointの差を取得する
    split_point["diff"] = split_point["end_split_point"] - split_point["split_point"]

    # pandasの設定で日本語がずれるのを防ぐ
    pd.set_option("display.unicode.east_asian_width", True)
    print(split_point)

    # df_bookを分割する
    dfs = []
    for _, row in split_point.iterrows():
        dfs.append(
            split_df(df_book, row["split_point"], row["end_split_point"], row["text"])
        )

    # ページごとに分割する
    text_by_page = list(map(split_text_by_page, dfs))

    # ページごとに結合する
    prompts = combine_text_by_page(text_by_page)

    # promptディレクトリを作成する
    os.makedirs("prompt", exist_ok=True)

    # promptをprompt_{index}.txtとして保存する
    for i, prompt in enumerate(prompts):
        # ファイル名を四桁のゼロでパディングする
        file_name = "prompt/prompt_" + str(i).zfill(4) + ".txt"

        # promptにindexを追加する どのpromptがどのファイルに対応しているかを把握するため
        prompt["file_name"] = file_name

        # promptを保存する
        with open(file_name, "w") as f:
            f.write(prompt["prompt"])

    # promptsをdfに変換する
    df_prompts = pd.DataFrame(prompts)

    # df_promptsのfile_name列とsplit_range列をCSVに保存する
    df_prompts[["file_name", "split_range", "title"]].to_csv("tmp/index.csv", index=False)
