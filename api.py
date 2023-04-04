import os
from pprint import pprint

import openai

from fastapi import FastAPI, Header, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")


@app.get("/completion")
async def request_completion(q: str):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": q},
        ]
    )

    response_text = response.choices[0].message.content

    return {"message": response_text}


@app.get("/image")
async def request_image(q: str):
    response = openai.Image.create(
        prompt=q,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    return {"url": image_url}