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
{   'args': {   'logprobs': None,
                'max_tokens': 70,
                'model': 'togethercomputer/LLaMA-2-7B-32K',
                'prompt': "Isaac Asimov's Three Laws of Robotics are: \n\n1.",
                'repetition_penalty': 1.2,
                'stop': ['</s>'],
                'temperature': 0.6,
                'top_k': 90,
                'top_p': 0.8},
    'model': 'togethercomputer/LLaMA-2-7B-32K',
    'model_owner': '',
    'num_returns': 1,
    'output': {   'choices': [   {   'finish_reason': 'length',
                                     'index': 0,
                                     'text': 'A robot may not injure a human '
                                             'being or, through inaction, '
                                             'allow a human being to come to '
                                             'harm.\n'
                                             '2. A robot must obey the orders '
                                             'given it by human beings except '
                                             'where such orders would conflict '
                                             'with the First Law.\n'
                                             '3. A robot must protect its own '
                                             'existence as long as such '
                                             'protection does not conflict '
                                             'with the'}],
                  'raw_compute_time': 1.9681874650996178,
                  'result_type': 'language-model-inference'},
    'prompt': ["Isaac Asimov's Three Laws of Robotics are: \n\n1."],
    'status': 'finished',
    'subjobs': [],
    'tags': {}}
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

We included an example dataset that comes with `together` to help you get a feel for the data format. Let's look at the first 5 lines of this 100 line dataset:

```python
together.jokes_list[:5]
```

```
[{'text': '<human>: Why is this joke funny? Q: What does a computer do when it is tired? A: It crashes!\nRosey: Did your computer ever stop working (freeze) or turn itself off when you wanted to use it? If it did, you can say your computer crashed. Computer crashes are frustrating because you cannot get your work done, and sometimes you lose the work you finished most recently, unless you saved it. Thankfully, they do not happen too often.'},
 {'text': "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Where can you go to practice math on New Year’s Eve? A: Times Square!\nRosey: To get better at math, people often people often practice addition (+) or subtraction (-) problems; then they work on multiplication (x) and division (÷), and all the way through calculus and beyond. Practicing multiplication is also known as practicing your times tables. You can say what is seven times nine (7 x 9), or you can can say what is seven multiplied by nine. They mean the same thing, times or multiplied by."},
 {'text': '<human>: Explain this joke: Q: When does it rain money? A: When there is change in the weather!\nRosey: “The rain in Spain falls mainly on the plain,” according to the song from My Fair Lady. In Peru, they just wish it would rain! But nowhere does it rain money. Rain is water that falls from the sky as part of the evaporation/water cycle. When it is sunny outside, and then the weather changes to cloudy or rainy, we say that there is a change in the weather.'},
 {'text': '<human>: Q: What happens when winter arrives? A: Autumn leaves! Why is this joke funny?\nRosey: In the northern hemisphere winter officially starts on December 21 (winter solstice, astronomical winter), but for many places in the north, it is already cold. Did you know that there is more than one way to mark the start of winter? Meteorologists, people who study the weather, talk about meteorological winter which starts on December 1. When talking about seasons, winter comes after fall; fall is also known as autumn.'},
 {'text': '<human>: Q: Where do roses sleep? A: In a flower bed! Why is this joke funny?\nRosey: According to many surveys, roses are one of the most popular flowers. Although they have thorns, some people say that they are not that hard to grow.'}]
```

Use the `together.Files.save_jsonl` function to save this python list of dictionaries into a jsonl file locally that has the correct formatting where each line is a json with single "text" field:

```python
together.Files.save_jsonl(together.jokes_list, "jokes.jsonl")
```

Use `together.Files.check` to check if your jsonl file has the correct format. Also take a look at it with the editor of your choice. 

```python
resp = together.Files.check(file="jokes.jsonl")
print(resp)
```

If the file format is correct, the `is_check_passed` field will be True

```
{'is_check_passed': True, 'model_special_tokens': 'we are not yet checking end of sentence tokens for this model', 'file_present': 'File found', 'file_size': 'File size 0.0 GB', 'num_samples': 100, 'num_samples_w_eos_token': 0}
```

To check if your data contains `model_special_tokens` (we are still expanding this to include more models and tokens) use:

```python
together.Files.check(file="jokes.jsonl",model="togethercomputer/RedPajama-INCITE-Chat-3B-v1")
```

The json checker is applied at the time of file upload unless `check = False` is passed as an argument to `together.Files.upload`. In the below example we attempt to upload a bad file, just to see an example checker output for an invalid file with a list of reasons file was invalid:

```python
resp = together.Files.upload(file="/file/path/to/bad.jsonl")
print(resp)
```

```
{   'file_present': 'File found',
    'file_size': 'File size 0.0 GB',
    'is_check_passed': False,
    'key_value': 'Unexpected, value type for "text" key on line 6 of the input '
                 'file.The value type of the "text" key must be a '
                 'string.Expected format: {"text":"my sample string"}See '
                 'https://docs.together.ai/docs/fine-tuning for more '
                 'information.{"text": {"text":"<human>: Salutations!\\n<bot>: '
                 'Salutations to you as well! How can I help you today?"}}\n',
    'min_samples': 'Processing /Users/carsonlam/Projects/data/bad.jsonl '
                   'resulted in only 10 samples. Our minimum is 100 samples. ',
    'model_special_tokens': 'we are not yet checking end of sentence tokens '
                            'for this model',
    'num_samples_w_eos_token': 0,
    'text_field': 'No "text" field was found on line 7 of the the input '
                  'file.Expected format: {"text":"my sample string"}.see '
                  'https://docs.together.ai/docs/fine-tuning for more '
                  'information.{"ext": "<human>: Hiya!\\n<bot>: Hiya! How may '
                  'I assist you?"}\n'}
```

The checker will look at the jsonl file to see if:

- each line of the file is a valid json object
- the expected key is that json object (i.e. "text")
- the type of each key is the expected type (i.e. str)
- minimum number of samples is met

In the `resp`, we will report the first line where the formatting error occurs, print the line, and the data format documentation on our website. Next lets upload a good file:

```python
together.Files.upload(file="jokes.jsonl")
```

You will get back the file `id` of the file you just uploaded

```
{'filename': 'jokes.jsonl','id': 'file-d0d318cb-b7d9-493a-bd70-1cfe089d3815','object': 'file'}
```

You will get back the file `id` of the file you just uploaded, but if you forget it, you can get the `id`'s of all the files you have uploaded using `together.Files.list()`. You'll need these `id`'s that start with `file-960be810-4d....` in order to start a fine-tuning job

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

Now that you have a valid file uploaded to together, you can finetune any of the models listed [here](https://docs.together.ai/docs/models-fine-tuning) or here `together.finetune_model_names` using `together.Finetune.create`

```python
resp = together.Finetune.create(
  training_file = 'file-d0d318cb-b7d9-493a-bd70-1cfe089d3815',
  model = 'togethercomputer/RedPajama-INCITE-Chat-3B-v1',
  n_epochs = 3,
  n_checkpoints = 1,
  batch_size = 4,
  learning_rate = 1e-5,
  suffix = 'my-demo-finetune',
  wandb_api_key = '1a2b3c4d5e.......',
)

fine_tune_id = resp['id']
print(resp)
```

The response `resp` has alot of information for you that you can retrieve later with `together.Finetune.retrieve` using the `fine_tune_id` for this job. You can find this `fine_tune_id` in `resp['id']` and use it to check in on how your finetune job is doing. 

```python
print(together.Finetune.retrieve(fine_tune_id=fine_tune_id)) # retrieves information on finetune event
print(together.Finetune.get_job_status(fine_tune_id=fine_tune_id)) # pending, running, completed
print(together.Finetune.is_final_model_available(fine_tune_id=fine_tune_id)) # True, False
print(together.Finetune.get_checkpoints(fine_tune_id=fine_tune_id)) # list of checkpoints
```

The `get_job_status` should change from `pending` to `running` to `completed` as `is_final_model_available` changes from `False` to `True`. Once the final model is available, you should be able to see your new model under `together.Models.list()` with a naming convention that includes your name, the `fine_tune_id`, the date and time, like this: 

`carlton/ft-dd93c727-f35e-41c2-a370-7d55b54128fa-2023-08-16-10-15-09`

Now you can download your model using `together.Finetune.download(fine_tune_id)` or start using your model on our inference engine (may take a few minutes after finetuning to become available) by first starting your new model instance:

```
together.Models.start("carlton/ft-dd93c727-f35e-41c2-a370-7d55b54128fa-2023-08-16-10-15-09")
```

then calling it to do completions:

```
output = together.Complete.create(
  prompt = "Isaac Asimov's Three Laws of Robotics are:\n\n1. ", 
  model = "carlton/ft-dd93c727-f35e-41c2-a370-7d55b54128fa-2023-08-16-10-15-09", 
)
```

To check whether your model is finished deploying, you can use the `Models.ready` like so:

```
together.Models.ready("carlton/ft-dd93c727-f35e-41c2-a370-7d55b54128fa-2023-08-16-10-15-09")
```

```
{'ready': 'model is ready for start, status code:1'}
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
together complete "Space robots are" -m togethercomputer/RedPajama-INCITE-7B-Base

# check which models are running
together models instances

# stop a model
together models stop togethercomputer/RedPajama-INCITE-7B-Base

# check your jsonl file
together files check jokes.jsonl

# upload your jsonl file
together files upload jokes.jsonl

# upload your jsonl file and disable file checking
together files upload jokes.jsonl --no-check

# list your uploaded files
together files list

# start fine-tuning a model on your jsonl file (use the id of your file given to after upload or from together files list)
together finetune create -t file-9263d6b7-736f-43fc-8d14-b7f0efae9079 -m togethercomputer/RedPajama-INCITE-Chat-3B-v1

# download your finetuned model (with your fine_tune_id from the id key given during create or from together finetune list)
together finetune download ft-dd93c727-f35e-41c2-a370-7d55b54128fa 

# inference using your new finetuned model (with new finetuned model name from together models list)
together complete "Space robots are" -m yourname/ft-dd93c727-f35e-41c2-a370-7d55b54128fa-2023-08-16-10-15-09
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
