The [Together Python Library](https://pypi.org/project/together/) is the official Python client for Together's API platform, providing a convenient way for interacting with the Together APIs and enables easy integration of the inference API with your applications.

# Installation

To install Together CLI , simply run:

```shell Shell
pip install --upgrade together
```

# Usage

The Python Library requires your Together API Key to be configured. This key can be found in your Account's settings on the Playground. Simply click on and navigate to Profile Button > Settings > API Keys.

The API Key can be configured by either setting the `TOGETHER_API_KEY` environment variable, like this:

```shell
export TOGETHER_API_KEY=xxxxx
```

Or by setting `together.api_key`:

```python
import together
together.api_key = "xxxxx"
```

> 🚧 You will need to start a model instance from the Playground before you can query it from the API

Once you've started a model instance, you can start querying:

```python
import together

# set your API key
together.api_key = "xxxxx"

# list available models and descriptons
models = together.Models.list()

# print the first model's name
print(models[0]['name'])

output = together.Complete.create("Space robots", model="togethercomputer/RedPajama-INCITE-7B-Base")

# print generated text
print(output['output']['choices'][0]['text'])
```

## Chat

The `chat` command is a CLI-based chat application that can be used for back-and-forth conversations with models in a pre-defined format.

Refer to the [Chat docs](https://docs.together.ai/docs/python-chat) on how to chat with your favorite models.

## Complete

The `complete` command can be used to inference with all the models available in the Together Playground. This is recommended for custom applications and raw queries. It provides all the functions you need to run inference on all the leading open-source models available with the Together API. You can use these functions by interacting with the command line utility from your terminal or for usage in your custom Python applications.

Refer to the [Complete docs](https://docs.together.ai/docs/python-complete) on how you can query these models.

## Image

The `image` command can be used to generate images from the leading open-source image generation models available with the Together API. You can use these functions by interacting with the command line utility from your terminal or for usage in your custom Python applications.

Refer to the [Image docs](https://docs.together.ai/docs/python-image) on how you can generate images.

## Files

Files are used for uploading training and validation datasets that are used for [fine-tuning](https://docs.together.ai/docs/python-fine-tuning).

Refer to the [Files docs](https://docs.together.ai/docs/python-files) on the correct way to prepare your files and managing them.

## Fine-tuning

Run and manage your fine-tuning jobs, enabling you to tune all model layers, control hyper-parameters, download the weights and checkpoints.

Refer to the [Fine-tuning docs](https://docs.together.ai/docs/python-fine-tuning) on how to get started.

# Command-line interface

All the above commands are also available through a CLI:

```shell
# list commands
together --help

# list available models
together models list

# create completion
together complete "Space robots" -m togethercomputer/RedPajama-INCITE-7B-Base
```
## Contributing
1. Clone the repo and make your changes
2. Run `pip install together['quality']`
3. From the root of the repo, run
    - `black .`
    - `ruff .`
      - And if necessary, `ruff . --fix`
    - `mypy --strict .`
4. Create a PR
