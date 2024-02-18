from time import sleep
import settings
import key
import os
import concurrent.futures
from openai import OpenAI

client = OpenAI(api_key=key.api_key)


# prompt/以下のファイル名をすべて取得する関数
def get_prompt_file_names():
    prompt_file_names = []
    for file_name in os.listdir("prompt"):
        prompt_file_names.append(file_name)

    # ファイル名を昇順に並び替える
    prompt_file_names.sort()

    return prompt_file_names


# 1threadで処理する関数
def one_thread(file_name: str):
    prompt = read_file(file_name)
    print(file_name)

    try:
        summary = generate_summary(prompt)
        sleep(settings.sleep_time)
        write_file(file_name, summary)
    except Exception as e:
        print(file_name+": "+str(e))



# ファイル名に基づいて読み込みを行う関数
def read_file(file_name: str) -> str:
    with open("prompt/" + file_name, "r") as f:
        prompt = f.read()
    return prompt


# # GPTを使用してテキストを生成する関数
def generate_summary(prompt: str) -> str:
    completion = client.chat.completions.create(
        model=settings.model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=settings.temperature,
        top_p=settings.top_p,
        max_tokens=settings.max_tokens,
    )

    return completion.choices[0].message.content


# ファイル名に基づいて書き込みを行う関数
def write_file(file_name: str, summary: str):
    with open("summary/" + file_name, "w") as f:
        f.write(summary)


if __name__ == "__main__":
    # summaryディレクトリを作成する
    os.makedirs("summary", exist_ok=True)

    flies = get_prompt_file_names()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(one_thread, flies)
