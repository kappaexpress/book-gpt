import summary_all
import os
import settings

if __name__ == "__main__":
    # ファイル名を指定する
    flie = settings.file_name

    # summaryディレクトリを作成する
    os.makedirs("summary", exist_ok=True)

    summary_all.one_thread(flie)
