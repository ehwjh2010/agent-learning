import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)

talks = [
    {
        "role": "system",
        "content": "你是一个食谱助理",
    }
]

if __name__ == "__main__":
    while True:
        try:
            prompt = input("请输入你的问题：")
            if prompt.lower() in ["exit", "quit", "退出"]:
                break

            talks.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=[talks[0], *talks[1:][-14:]],
            )
            print(response.choices[0].message.content)
            talks.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
        except KeyboardInterrupt:
            print("Interrupted")
            break
        except Exception as e:
            print(e)
            break
