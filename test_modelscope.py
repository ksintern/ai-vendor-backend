from openai import OpenAI

TOKEN="ms-82a69af0-6326-49bf-93b9-d93a61f2c349"

print(
    "TOKEN START:",
    TOKEN[:10]
)

client=OpenAI(

    api_key=TOKEN,

    base_url="https://api-inference.modelscope.ai/v1"

)

try:

    response=(

        client.chat.completions.create(

            model="Qwen/Qwen2.5-7B-Instruct",

            messages=[

                {

                    "role":"user",

                    "content":"hello"

                }

            ]

        )

    )

    print(

        response
        .choices[0]
        .message.content

    )

except Exception as e:

    print(e)