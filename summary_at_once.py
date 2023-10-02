import openai
import settings
import key

openai.api_key = key.api_key


# 通常モデルを使用してテキストを生成する関数
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model=settings.model,
        prompt=prompt,
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


if __name__ == "__main__":
    # prompt/prompt_1.txtの内容を読み込みます。
    with open("prompt/prompt_0002.txt") as f:
        prompt = f.read()

    response = generate_text_instruct(prompt)

    print(response)
