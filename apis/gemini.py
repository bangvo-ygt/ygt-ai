from dotenv import load_dotenv

load_dotenv()  # take environment variables
# ruff: noqa: E402

import json
import os
import pathlib
import time
from typing import Any

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

prompt = open("./apis/prompt.txt", "r").read()


def call_gemini(content: str = "") -> tuple[Any, Any]:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=content,
                mime_type="text/html",
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
    tokens = response.usage_metadata

    return text, tokens
