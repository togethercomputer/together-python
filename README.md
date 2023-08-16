The [Together Python Library](https://pypi.org/project/together/) is the official Python client for Together's API platform, providing a convenient way for interacting with the Together APIs and enables easy integration of the inference API with your applications.

# Installation

To install Together CLI , simply run:

```shell Shell
pip install --upgrade together
```

# Usage

> 🚧 You will need to create a free account with [together.ai](https://api.together.xyz/) to obtain a Together API Key.

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

Once you've provided your API key, you can browse our list of available models:

```python
import together

# set your API key
together.api_key = "xxxxx"

# see available models
model_list = together.Models.list()

print(f"{len(model_list)} models available")

# print the first 10 models on the menu
model_names = [model_dict['name'] for model_dict in model_list]
model_names[:10]
```

We are constantly updating this list, but you should expect to see something like this:

```python
64 models available
['EleutherAI/gpt-j-6b',
 'EleutherAI/gpt-neox-20b',
 'EleutherAI/pythia-12b-v0',
 'EleutherAI/pythia-1b-v0',
 'EleutherAI/pythia-2.8b-v0',
 'EleutherAI/pythia-6.9b',
 'HuggingFaceH4/starchat-alpha',
 'NousResearch/Nous-Hermes-13b',
 'NousResearch/Nous-Hermes-Llama2-13b',
 'NumbersStation/nsql-6B']
```


Let's start an instance of one of the models in the list above. You can also start an instance by clicking play on any model in the [models playground](https://api.together.xyz/playground).

```python
together.Models.start('togethercomputer/LLaMA-2-7B-32K')
```

Once you've started a model instance, you can start querying. Notice the inputs available to you to adjust the output you get and how the text is returned to you in the `choices` list.

```python
output = together.Complete.create(
  prompt = "Isaac Asimov's Three Laws of Robotics are:\n\n1. ", 
  model = "togethercomputer/LLaMA-2-7B-32K", 
  max_tokens = 70,
  temperature = 0.6,
  top_k = 90,
  top_p = 0.8,
  repetition_penalty = 1.1,
  stop = ['</s>']
)

# print generated text
print(output['prompt'][0]+output['output']['choices'][0]['text'])
```

Since the temperature is > 0.0, you will see some creative variation in the output text, here is one example:

```
Isaac Asimov's Three Laws of Robotics are: 

1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.
2. A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.
3. A robot must protect its own existence as long as such protection does not conflict with the
```

We are constantly updating the capabilities of these models and our API, but here is one example just to show you the different components of the output available to you:

```python
# print the entire output to see it's components
print(output)
```

```
{'status': 'finished', 'prompt': ["Isaac Asimov's Three Laws of Robotics are: \n\n1."], 'model': 'togethercomputer/LLaMA-2-7B-32K', 'model_owner': '', 'tags': {}, 'num_returns': 1, 'args': {'model': 'togethercomputer/LLaMA-2-7B-32K', 'prompt': "Isaac Asimov's Three Laws of Robotics are: \n\n1.", 'top_p': 0.8, 'top_k': 90, 'temperature': 0.6, 'max_tokens': 70, 'stop': ['</s>'], 'repetition_penalty': 1.2, 'logprobs': None}, 'subjobs': [], 'output': {'choices': [{'finish_reason': 'length', 'index': 0, 'text': 'A robot may not injure a human being or, through inaction, allow a human being to come to harm.\n2. A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.\n3. A robot must protect its own existence as long as such protection does not conflict with the'}], 'raw_compute_time': 1.9681874650996178, 'result_type': 'language-model-inference'}}
```

Check which models have been started or stopped:

```python
together.Models.instances()
```

To stop your model instance:

```python
together.Models.stop("togethercomputer/LLaMA-2-7B-32K")
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

# start a model
together models start togethercomputer/RedPajama-INCITE-7B-Base

# create completion
together complete "Space robots" -m togethercomputer/RedPajama-INCITE-7B-Base

# check which models are running
together models instances

# stop a model
together models stop togethercomputer/RedPajama-INCITE-7B-Base
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
