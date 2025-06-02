<div align="center">
  <a href="https://www.together.ai/">
    <img alt="together.ai" height="100px" src="https://assets-global.website-files.com/64f6f2c0e3f4c5a91c1e823a/654693d569494912cfc0c0d4_favicon.svg">
  </a>
</div>

# Together Python API library

[![PyPI version](https://img.shields.io/pypi/v/together.svg)](https://pypi.org/project/together/)
[![Discord](https://dcbadge.vercel.app/api/server/9Rk6sSeWEG?style=flat&compact=true)](https://discord.com/invite/9Rk6sSeWEG)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/togethercompute.svg?style=social&label=Follow%20%40togethercompute)](https://twitter.com/togethercompute)

The [Together Python API Library](https://pypi.org/project/together/) is the official Python client for Together's API platform, providing a convenient way for interacting with the REST APIs and enables easy integrations with Python 3.10+ applications with easy to use synchronous and asynchronous clients.



## Installation

> 🚧
> The Library was rewritten in v1.0.0 released in April of 2024. There were significant changes made.

To install Together Python Library from PyPI, simply run:

```shell Shell
pip install --upgrade together
```

### Setting up API Key

> 🚧 You will need to create an account with [Together.ai](https://api.together.xyz/) to obtain a Together API Key.

Once logged in to the Together Playground, you can find available API keys in [this settings page](https://api.together.xyz/settings/api-keys).

#### Setting environment variable

```shell
export TOGETHER_API_KEY=xxxxx
```

#### Using the client

```python
from together import Together

client = Together(api_key="xxxxx")
```

This repo contains both a Python Library and a CLI. We'll demonstrate how to use both below.

## Usage – Python Client

### Chat Completions

```python
from together import Together

client = Together()

# Simple text message
response = client.chat.completions.create(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
    messages=[{"role": "user", "content": "tell me about new york"}],
)
print(response.choices[0].message.content)

# Multi-modal message with text and image
response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://huggingface.co/datasets/patrickvonplaten/random_img/resolve/main/yosemite.png"
                }
            }
        ]
    }]
)
print(response.choices[0].message.content)

# Multi-modal message with multiple images
response = client.chat.completions.create(
    model="Qwen/Qwen2.5-VL-72B-Instruct",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Compare these two images."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://huggingface.co/datasets/patrickvonplaten/random_img/resolve/main/yosemite.png"
                }
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://huggingface.co/datasets/patrickvonplaten/random_img/resolve/main/slack.png"
                }
            }
        ]
    }]
)
print(response.choices[0].message.content)

# Multi-modal message with text and video
response = client.chat.completions.create(
    model="Qwen/Qwen2.5-VL-72B-Instruct",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's happening in this video?"
            },
            {
                "type": "video_url",
                "video_url": {
                    "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
                }
            }
        ]
    }]
)
print(response.choices[0].message.content)
```

The chat completions API supports three types of content:
- Plain text messages using the `content` field directly
- Multi-modal messages with images using `type: "image_url"`
- Multi-modal messages with videos using `type: "video_url"`

When using multi-modal content, the `content` field becomes an array of content objects, each with its own type and corresponding data.

#### Streaming

```python
import os
from together import Together

client = Together()
stream = client.chat.completions.create(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
    messages=[{"role": "user", "content": "tell me about new york"}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

#### Async usage

```python
import asyncio
from together import AsyncTogether

async_client = AsyncTogether()
messages = [
    "What are the top things to do in San Francisco?",
    "What country is Paris in?",
]

async def async_chat_completion(messages):
    async_client = AsyncTogether()
    tasks = [
        async_client.chat.completions.create(
            model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
            messages=[{"role": "user", "content": message}],
        )
        for message in messages
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.choices[0].message.content)

asyncio.run(async_chat_completion(messages))
```

#### Fetching logprobs

Logprobs are logarithms of token-level generation probabilities that indicate the likelihood of the generated token based on the previous tokens in the context. Logprobs allow us to estimate the model's confidence in its outputs, which can be used to decide how to optimally consume the model's output (e.g. rejecting low confidence outputs, retrying or ensembling model outputs etc).

```python
from together import Together

client = Together()

response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    messages=[{"role": "user", "content": "tell me about new york"}],
    logprobs=1
)

response_lobprobs = response.choices[0].logprobs

print(dict(zip(response_lobprobs.tokens, response_lobprobs.token_logprobs)))
# {'New': -2.384e-07, ' York': 0.0, ',': 0.0, ' also': -0.20703125, ' known': -0.20214844, ' as': -8.34465e-07, ... }
```

More details about using logprobs in Together's API can be found [here](https://docs.together.ai/docs/logprobs).


### Completions

Completions are for code and language models shown [here](https://docs.together.ai/docs/inference-models). Below, a code model example is shown.

```python
from together import Together

client = Together()

response = client.completions.create(
    model="codellama/CodeLlama-34b-Python-hf",
    prompt="Write a Next.js component with TailwindCSS for a header component.",
    max_tokens=200,
)
print(response.choices[0].text)
```

#### Streaming

```python
from together import Together

client = Together()
stream = client.completions.create(
    model="codellama/CodeLlama-34b-Python-hf",
    prompt="Write a Next.js component with TailwindCSS for a header component.",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

#### Async usage

```python
import asyncio
from together import AsyncTogether

async_client = AsyncTogether()
prompts = [
    "Write a Next.js component with TailwindCSS for a header component.",
    "Write a python function for the fibonacci sequence",
]

async def async_chat_completion(prompts):
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

### Image generation

```python
from together import Together

client = Together()

response = client.images.generate(
    prompt="space robots",
    model="stabilityai/stable-diffusion-xl-base-1.0",
    steps=10,
    n=4,
)
print(response.data[0].b64_json)
```

### Embeddings

```python
from typing import List
from together import Together

client = Together()

def get_embeddings(texts: List[str], model: str) -> List[List[float]]:
    texts = [text.replace("\n", " ") for text in texts]
    outputs = client.embeddings.create(model=model, input = texts)
    return [outputs.data[i].embedding for i in range(len(texts))]

input_texts = ['Our solar system orbits the Milky Way galaxy at about 515,000 mph']
embeddings = get_embeddings(input_texts, model='togethercomputer/m2-bert-80M-8k-retrieval')

print(embeddings)
```

### Reranking

```python
from typing import List
from together import Together

client = Together()

def get_reranked_documents(query: str, documents: List[str], model: str, top_n: int = 3) -> List[str]:
    outputs = client.rerank.create(model=model, query=query, documents=documents, top_n=top_n)
    # sort by relevance score and returns the original docs
    return [documents[i] for i in [x.index for x in sorted(outputs.results, key=lambda x: x.relevance_score, reverse=True)]]

query = "What is the capital of the United States?"
documents = ["New York","Washington, D.C.", "Los Angeles"]

reranked_documents = get_reranked_documents(query, documents, model='Salesforce/Llama-Rank-V1', top_n=1)

print(reranked_documents)
```

Read more about Reranking [here](https://docs.together.ai/docs/rerank-overview).

### Files

The files API is used for fine-tuning and allows developers to upload data to fine-tune on. It also has several methods to list all files, retrive files, and delete files. Please refer to our fine-tuning docs [here](https://docs.together.ai/docs/fine-tuning-python).

```python
from together import Together

client = Together()

client.files.upload(file="somedata.jsonl") # uploads a file
client.files.list() # lists all uploaded files
client.files.retrieve(id="file-d0d318cb-b7d9-493a-bd70-1cfe089d3815") # retrieves a specific file
client.files.retrieve_content(id="file-d0d318cb-b7d9-493a-bd70-1cfe089d3815") # retrieves content of a specific file
client.files.delete(id="file-d0d318cb-b7d9-493a-bd70-1cfe089d3815") # deletes a file
```

### Fine-tunes

The finetune API is used for fine-tuning and allows developers to create finetuning jobs. It also has several methods to list all jobs, retrive statuses and get checkpoints. Please refer to our fine-tuning docs [here](https://docs.together.ai/docs/fine-tuning-quickstart).

```python
from together import Together

client = Together()

client.fine_tuning.create(
  training_file = 'file-d0d318cb-b7d9-493a-bd70-1cfe089d3815',
  model = 'meta-llama/Llama-3.2-3B-Instruct',
  n_epochs = 3,
  n_checkpoints = 1,
  batch_size = "max",
  learning_rate = 1e-5,
  suffix = 'my-demo-finetune',
  wandb_api_key = '1a2b3c4d5e.......',
)
client.fine_tuning.list() # lists all fine-tuned jobs
client.fine_tuning.retrieve(id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b") # retrieves information on finetune event
client.fine_tuning.cancel(id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b") # Cancels a fine-tuning job
client.fine_tuning.list_events(id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b") #  Lists events of a fine-tune job
client.fine_tuning.download(id="ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b") # downloads compressed fine-tuned model or checkpoint to local disk
```

### Models

This lists all the models that Together supports.

```python
from together import Together

client = Together()

models = client.models.list()

for model in models:
    print(model)
```

## Usage – CLI

### Chat Completions

```bash
together chat.completions \
  --message "system" "You are a helpful assistant named Together" \
  --message "user" "What is your name?" \
  --model meta-llama/Llama-4-Scout-17B-16E-Instruct
```

The Chat Completions CLI enables streaming tokens to stdout by default. To disable streaming, use `--no-stream`.

### Completions

```bash
together completions \
  "Large language models are " \
  --model meta-llama/Llama-4-Scout-17B-16E-Instruct \
  --max-tokens 512 \
  --stop "."
```

The Completions CLI enables streaming tokens to stdout by default. To disable streaming, use `--no-stream`.

### Image Generations

```bash
together images generate \
  "space robots" \
  --model stabilityai/stable-diffusion-xl-base-1.0 \
  --n 4
```

The image is opened in the default image viewer by default. To disable this, use `--no-show`.

### Files

```bash
# Help
together files --help

# Check file
together files check example.jsonl

# Upload file
together files upload example.jsonl

# List files
together files list

# Retrieve file metadata
together files retrieve file-6f50f9d1-5b95-416c-9040-0799b2b4b894

# Retrieve file content
together files retrieve-content file-6f50f9d1-5b95-416c-9040-0799b2b4b894

# Delete remote file
together files delete file-6f50f9d1-5b95-416c-9040-0799b2b4b894
```

### Fine-tuning

```bash
# Help
together fine-tuning --help

# Create fine-tune job
together fine-tuning create \
  --model togethercomputer/llama-2-7b-chat \
  --training-file file-711d8724-b3e3-4ae2-b516-94841958117d

# List fine-tune jobs
together fine-tuning list

# Retrieve fine-tune job details
together fine-tuning retrieve ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b

# List fine-tune job events
together fine-tuning list-events ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b

# Cancel running job
together fine-tuning cancel ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b

# Download fine-tuned model weights
together fine-tuning download ft-c66a5c18-1d6d-43c9-94bd-32d756425b4b
```

### Models

```bash
# Help
together models --help

# List models
together models list
```

## Contributing

Refer to the [Contributing Guide](CONTRIBUTING.md)
