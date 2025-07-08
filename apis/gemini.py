import json
import time

from dotenv import load_dotenv

load_dotenv()  # take environment variables
# ruff: noqa: E402

import os
import pathlib

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

prompt = open("./prompt.txt", "r").read()


def call_gemini(path):
    filepath = pathlib.Path(path)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type="application/pdf",
            ),
            prompt,
        ],
        config=types.GenerateContentConfig(
            # Turn off thinking:
            thinking_config=types.ThinkingConfig(thinking_budget=0)
            # thinking_config=types.ThinkingConfig(thinking_budget=1024)
        ),
    )
    content = response.candidates[0].content.parts
    for part in content:
        text = part.text
        print(text)
    tokens = response.usage_metadata
    input_tokens = tokens.prompt_token_count
    candidate_tokens = tokens.candidates_token_count
    thought_tokens = tokens.thoughts_token_count
    if thought_tokens:
        output_tokens = candidate_tokens + thought_tokens
    else:
        output_tokens = candidate_tokens

    input_details_tokens = tokens.prompt_tokens_details

    name = os.path.basename(path).split(".")[0]

    with open(f"./test/outputs/{name}.txt", "w") as f:
        f.write(text)
        f.write("\n\n\n")
        f.write(f"input tokens: {input_tokens}\n")
        f.write(f"output tokens: {output_tokens}\n")
        f.write(f"input detail tokens: {input_details_tokens}\n")
        f.write(f"output candidate tokens: {candidate_tokens}\n")
        f.write(f"output thought tokens: {thought_tokens}\n")

    return response


if __name__ == "__main__":
    pdfs_path = "YGT Cost/YGT Sample Invoices/"

    all_files = [f for f in os.listdir(pdfs_path)]

    for path in all_files:
        full_path = os.path.join(pdfs_path, path)
        start = time.time()
        response = call_gemini(full_path)

        with open(f"./outputs/{path.split(".")[0]}.txt", "a") as f:
            f.write(f"Response time:{time.time() - start}")
