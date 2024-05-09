import summary_all
import os

if __name__ == "__main__":
    # ファイル名を指定する(書き換える)
    flie = "0000.txt"

    # summaryディレクトリを作成する
    os.makedirs("summary", exist_ok=True)

    summary_all.one_thread(flie)