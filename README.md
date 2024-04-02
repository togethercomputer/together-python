The [Together Python Library](https://pypi.org/project/together/) is the official Python client for Together's API platform, providing a convenient way for interacting with the REST APIs and enables easy integrations with Python 3.8+ applications with easy to use synchronous and asynchronous clients.

# Installation

> 🚧
> The library was rewritten in v1.0.0 released in April of 2024. There were significant changes made. Find the complete migration guide [here](docs/MIGRATION_GUIDE_v1.md).

To install Together Python Library from PyPi, simply run:

```shell Shell
pip install --upgrade together
```

## Setting up API Key

> 🚧 You will need to create an account with [Together.ai](https://api.together.xyz/) to obtain a Together API Key.

Once logged in to the Together Playground, you can find available API keys in [this settings page](https://api.together.xyz/settings/api-keys).

### Setting environment variable

```shell
export TOGETHER_API_KEY=xxxxx
```

### Using the client

```python
from together import Together

client = Together(api_key="xxxxx")
```

This library contains both a python library and a CLI. We'll demonstrate how to use both below.

# Usage – Python Client

## Chat Completions

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

response = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[{"role": "user", "content": "tell me about new york"}],
)
print(response.choices[0].message.content)
```

### Streaming

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
stream = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[{"role": "user", "content": "tell me about new york"}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Async usage

```python
import os, asyncio
from together import AsyncTogether

async_client = AsyncTogether(api_key=os.environ.get("TOGETHER_API_KEY"))
messages = [
    "What are the top things to do in San Francisco?",
    "What country is Paris in?",
]

async def async_chat_completion(messages):
    async_client = AsyncTogether(api_key=os.environ.get("TOGETHER_API_KEY"))
    tasks = [
        async_client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": message}],
        )
        for message in messages
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.choices[0].message.content)

asyncio.run(async_chat_completion(messages))
```

## Completions

Completions are for code and language models shown [here](https://docs.together.ai/docs/inference-models). Below, a code model example is shown.

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

response = client.completions.create(
    model="codellama/CodeLlama-34b-Python-hf",
    prompt="Write a Next.js component with TailwindCSS for a header component.",
)
print(response.choices[0].text)
```

### Streaming

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
stream = client.completions.create(
    model="codellama/CodeLlama-34b-Python-hf",
    prompt="Write a Next.js component with TailwindCSS for a header component.",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Async usage

```python
import os, asyncio
from together import AsyncTogether

async_client = AsyncTogether(api_key=os.environ.get("TOGETHER_API_KEY"))
prompts = [
    "Write a Next.js component with TailwindCSS for a header component.",
    "Write a python function for the fibonacci sequence",
]

async def async_chat_completion(prompts):
    async_client = AsyncTogether(api_key=os.environ.get("TOGETHER_API_KEY"))
    tasks = [
        async_client.completions.create(
            model="codellama/CodeLlama-34b-Python-hf",
            prompt=prompt,
        )
        for prompt in prompts
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.choices[0].text)

asyncio.run(async_chat_completion(prompts))
```

## Image generation

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

response = client.images.generate(
    prompt="space robots",
    model="stabilityai/stable-diffusion-xl-base-1.0",
    steps=10,
    n=4,
)
print(response.data[0].b64_json)
```

## Embeddings

```python
from typing import List
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

def get_embeddings(texts: List[str], model: str) -> List[List[float]]:
    texts = [text.replace("\n", " ") for text in texts]
    outputs = client.embeddings.create(model=model, input = texts)
    return [outputs.data[i].embedding for i in range(len(texts))]

input_texts = ['Our solar system orbits the Milky Way galaxy at about 515,000 mph']
embeddings = get_embeddings(input_texts, model='togethercomputer/m2-bert-80M-8k-retrieval')

print(embeddings)
```

## Files

// examples for upload, list, etc.

## Fine-tunes

// examples for create, list, etc.

## Models

This lists all the models that Together supports.

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

models = client.models.list()

for model in models:
    print(model)
```

# Usage – CLI

## Chat Completions

### Async usage

### Streaming

## Completions

### Streaming

## Image Generations

## Files

// examples for upload, list, etc.

## Fine-tunes

// examples for create, list, etc.

## Models

// listing models

## Contributing

Refer to the [Contributing Guide](CONTRIBUTING.md)
