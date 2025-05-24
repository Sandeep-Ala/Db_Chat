from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
google_gemini_api="AIzaSyAE519N9Il3PZjlpGyhu1C_T6Py-4s-5G8"
"AIzaSyC-mfr5gdczCF_5cpA3IAZl_z1mljtGzvA"
# "web-ui>python webui.py --ip 127.0.0.1 --port 7788"
completion = client.chat.completions.create(
#   extra_headers={
#     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#   },

# qwen/qwen-2.5-coder-32b-instruct:free   key:  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
  extra_body={},
  model="cognitivecomputations/dolphin3.0-r1-mistral-24b:free",   #"qwen/qwq-32b:free"--> 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
  messages=[
    {
      "role": "user",
      "content": "write python code to print the prime numbers from  given number range"
    }
  ]
)
print(completion.choices[0].message.content)