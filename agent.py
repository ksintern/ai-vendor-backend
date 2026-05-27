import os
from openai import OpenAI

# 1. Your verified token from your Access Control screenshot
API_TOKEN = "ms-f82346ae-07a5-4be7-be14-e5b6848b0418"

# 2. Point the OpenAI client to ModelScope's serverless cloud URL
client = OpenAI(
    base_url="https://api-inference.modelscope.cn/v1",
    api_key=API_TOKEN
)

# 3. Setup the Vendor Discovery Agent Persona & Job
system_prompt = (
    "You are an AI Vendor Discovery Agent. Your task is to analyze user constraints "
    "and output a clean JSON object identifying vendor criteria, action needed, and industry focus."
)
user_query = "Find me verified cloud database vendors located in North America that comply with SOC2 security rules."

print("⚡ [Vendor Discovery Agent]: Dispatching cloud request to ModelScope...")

try:
    # 4. Fire the completion using standard OpenAI structure
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",  # Or "deepseek-ai/DeepSeek-V3" if you want to try DeepSeek!
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.2
    )
    
    print("\n🎯 [Discovery Data Processed Successfully]:")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")
    print("If you still get a 401, make sure you have sent at least one message inside ModelScope's website chat demo to wake up your token.")