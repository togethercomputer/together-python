The [Together Python Library](https://pypi.org/project/together/) is the official Python client for Together's API platform, providing a convenient way for interacting with the REST APIs and enables easy integrations with Python 3.8+ applications with easy to use synchronous and asynchronous clients.

# Installation

> 🚧
> The library was rewritten in v1.0.0 released in March of 2024. There were significant changes made. Find the complete migration guide [here](docs/MIGRATION_GUIDE_v1.md).

To install Together Python Library from PyPi, simply run:

```shell Shell
pip install --upgrade together
```

To install the Library from source, run:

```shell Shell
pip install git+https://github.com/togethercomputer/together.git
```

## Setting up API Key

> 🚧 You will need to create an account with [Together.ai](https://api.together.xyz/) to obtain a Together API Key.

Once logged in to the Together Playground, you can find available API keys in [this settings page](https://api.together.xyz/settings/api-keys).

### python-dotenv

The recommended way to set the API key is using [python-dotenv](https://pypi.org/project/python-dotenv/). Simply add `TOGETHER_API_KEY=xxxxx` to the `.env` file.

### Setting environment variable

```shell
export TOGETHER_API_KEY=xxxxx
```

### Using the Client

```python
from together import Together

client = Together(
    api_key="xxxxx"
)
```

# Usage

## Chat Completions

// sync example

### Async usage

### Streaming

### CLI

## Completions

// sync example

### Async usage

### Streaming

### CLI

## Embeddings

// sync example

### Async usage

### CLI

## Image Generations

// sync example

### Async usage

### CLI

## Files

// examples for upload, list, etc.

### CLI

## Fine-tunes

// examples for create, list, etc.

### CLI

## Models

// listing models

### CLI

## Contributing
Refer to the [Contributing Guide](CONTRIBUTING.md)
