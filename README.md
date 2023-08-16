The [Together Python Library](https://pypi.org/project/together/) is the official Python client for Together's API platform, providing a convenient way for interacting with the Together APIs and enables easy integration of the inference API with your applications.

# Installation

To install Together CLI , simply run:

```shell Shell
pip install --upgrade together
```

# Activate

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

# Usage

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

## Complete

The `complete` command can be used to inference with all the models available in the Together Playground. This is recommended for custom applications and raw queries. It provides all the functions you need to run inference on all the leading open-source models available with the Together API. You can use these functions by interacting with the command line utility from your terminal or for usage in your custom Python applications.

Refer to the [Complete docs](https://docs.together.ai/docs/python-complete) on how you can query these models.

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

## Files

Files are used for uploading training and validation datasets that are used for [fine-tuning](https://docs.together.ai/docs/python-fine-tuning).

Refer to the [Files docs](https://docs.together.ai/docs/python-files) on the correct way to prepare your files and managing them.

Files uploaded for training, fine-tuning and validation must be in [jsonlines](https://jsonlines.org/) format.

As an example, use the `together.Files.save_jsonl` function to save this python list of dictionaries into a jsonl file locally that has the correct formatting where each line is a json with single "text" field:

```python
sample_jsonl = [
{"text": "<human>: Hi!\n<bot>: Hi! How can I assist you today?<|endoftext|>"},
{"text": "<human>: Hi there!\n<bot>: Hello! How can I assist you today?<|endoftext|>"},
{"text": "<human>: Hey!\n<bot>: Hi there! How can I help you?<|endoftext|>"},
{"text": "<human>: Greetings!\n<bot>: Hello! How may I be of assistance?<|endoftext|>"},
{"text": "<human>: Good day!\n<bot>: Good day to you too! How may I assist you today?<|endoftext|>"},
{"text": "<human>: Salutations!\n<bot>: Salutations to you as well! How can I help you today?<|endoftext|>"},
{"text": "<human>: Hiya!\n<bot>: Hiya! How may I assist you?<|endoftext|>"},
{"text": "<human>: What's up?\n<bot>: Hi! How can I assist you today?<|endoftext|>"},
{"text": "<human>: Hi\n<bot>: Hi! How can I assist you today?<|endoftext|>"},
{"text": "<human>: Hi there\n<bot>: Hello! How can I assist you today?<|endoftext|>"},
{"text": "<human>: Hey\n<bot>: Hi there! How can I help you?<|endoftext|>"},
{"text": "<human>: Greetings\n<bot>: Hello! How may I be of assistance?<|endoftext|>"},
{"text": "<human>: Good day\n<bot>: Good day to you too! How may I assist you today?<|endoftext|>"},
{"text": "<human>: Salutations\n<bot>: Salutations to you as well! How can I help you today?<|endoftext|>"},
]

together.Files.save_jsonl(sample_jsonl, "sample_jsonl.jsonl")
```

Use `together.Files.check` to check if your jsonl file has the correct format. 

``python
resp = together.Files.check(file="sample_jsonl.jsonl")
print(resp)
```

If the file format is correct, the `is_check_passed` field will be True and the `error_list` will be empty.

```
{'is_check_passed': True, 'error_list': []}
```

To check of your data contains the correct model specific special tokens (under construction):

```python
together.Files.check(file="sample_jsonl.jsonl",model="togethercomputer/RedPajama-INCITE-Chat-3B-v1")
```

The json checker is applied at the time of file upload unless `do_check = False` is passed as an argument to `together.Files.upload`. In the example you attempt to upload a bad file.

```python
resp = together.Files.upload(file="/file/path/to/bad.jsonl")
print(resp)
```

The checker will look at the jsonl file to see if:

- each line of the file is a valid json object
- the expected key is that json object (i.e. "text")
- the type of each key is the expected type (i.e. str)
- minimum number of samples is met

An example checker output for an invalid file with a list of reasons file was invalid:
```
{'is_check_passed': False, 'error_list': ['No "text" field was found in one or more lines in JSONL file. see https://docs.together.ai/docs/fine-tuning. The first line where this occurs is line 3, where 1 is the first line. {"ext": {"1":1} ,"extra_key":"stuff"}\n', 'Processing /data/bad.jsonl resulted in only 3 samples. Our minimum is 4 samples. ']}
```

Next lets upload a good file

```python
together.Files.upload(file="sample_jsonl.jsonl")
```

You will get back the file `id` of the file you just uploaded

```
{'filename': 'sample_jsonl.jsonl','id': 'file-d0d318cb-b7d9-493a-bd70-1cfe089d3815','object': 'file'}
```

You will get back the file `id` of the file you just uploaded, but if you forget it, you can get the `id`'s of all the files you have uploaded using ` together.Files.list()`. You'll need these `id`'s that start with `file-960be810-4d....` in order to start a fine-tuning job

```python
files_list = together.Files.list()
files_list['data']
```

```
[{'filename': 'jokes.jsonl',
  'bytes': 40805,
  'created_at': 1691710036,
  'id': 'file-960be810-4d33-449a-885a-9f69bd8fd0e2',
  'purpose': 'fine-tune',
  'object': 'file',
  'LineCount': 0,
  'Processed': True},
 {'filename': 'sample_jsonl.jsonl',
  'bytes': 1235,
  'created_at': 1692190883,
  'id': 'file-d0d318cb-b7d9-493a-bd70-1cfe089d3815',
  'purpose': 'fine-tune',
  'object': 'file',
  'LineCount': 0,
  'Processed': True}]
```

## Fine-tuning

Run and manage your fine-tuning jobs, enabling you to tune all model layers, control hyper-parameters, download the weights and checkpoints.

Refer to the [Fine-tuning docs](https://docs.together.ai/docs/python-fine-tuning) on how to get started.

```python
resp = together.Finetune.create(
  training_file = 'file-960be810-4d33-449a-885a-9f69bd8fd0e2',
  model = 'togethercomputer/LLaMA-2-7B-32K',
  n_epochs = 1,
  n_checkpoints = 1,
  batch_size = 4,
  learning_rate = 1e-5,
  suffix = 'my-demo-finetune',
  wandb_api_key = '1a2b3c4d....',
)
```

## Chat

The `chat` command is a CLI-based chat application that can be used for back-and-forth conversations with models in a pre-defined format.

Refer to the [Chat docs](https://docs.together.ai/docs/python-chat) on how to chat with your favorite models.

## Image

The `image` command can be used to generate images from the leading open-source image generation models available with the Together API. You can use these functions by interacting with the command line utility from your terminal or for usage in your custom Python applications.

Refer to the [Image docs](https://docs.together.ai/docs/python-image) on how you can generate images.

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
