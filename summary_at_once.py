import openai
import settings
import key

openai.api_key = key.api_key

if __name__ == "__main__":
    # prompt/prompt_1.txtの内容を読み込みます。
    with open("prompt/prompt_2.txt") as f:
        prompt = f.read()

    # GPTを使用してテキストを生成します。
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

    print(response['choices'][0]['message']['content'])
