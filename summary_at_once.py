import openai
import settings
import key

openai.api_key = key.api_key
prompt_path = "prompt"
summary_path = "summary"

# 通常モデルを使用してテキストを生成する関数
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model=settings.model,
        messages=[
            {"role": "system", "content": settings.context},
            {"role": "user", "content": prompt},
        ],
        temperature=settings.temperature,
        top_p=settings.top_p,
        max_tokens=settings.max_tokens,
    )
    return response['choices'][0]['message']['content']


# instructモデルを使用してテキストを生成する関数
def generate_text_instruct(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=settings.temperature,
        top_p=settings.top_p,
        max_tokens=settings.max_tokens,
    )
    return response['choices'][0]['text']


# ファイル名に基づいて書き込みを行う関数
def write_file(file_name: str, summary: str):
    # ファイル名を作成　prompt_0000.txt -> summary_0000.txt
    file_name = file_name.replace(prompt_path, summary_path)

    with open(summary_path + "/" + file_name, "w") as f:
        f.write(summary)


if __name__ == "__main__":
    path = "prompt/prompt_0175.txt"
    with open(path) as f:
        prompt = f.read()

    response = generate_text(prompt)

    print(response)

    file_name = path.split("/")[-1]

    write_file(file_name, response)
