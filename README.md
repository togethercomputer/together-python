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

In the example below we provide a link for you to download a jsonl file locally that serves as an example of the correct file formatting. In your terminal or commandline, navigate to the folder you want to download the file, paste the command below and hit enter.

```console
curl https://huggingface.co/datasets/clam004/antihallucination_dataset/resolve/main/antihallucination.jsonl -o antihallucination.jsonl
```

This will download the dataset to a file called `antihallucination.jsonl`. Below are two examples of lines you will find in this `.jsonl` file. 

```Text JSONL
{"text": "<truth>Wilhelm Windelband (May 11, 1848 - October 22, 1915) was a German philosopher of the Baden School. Windelband is now mainly remembered for the terms \"nomothetic\" and \"idiographic\", which he introduced. These have currency in psychology and other areas, though not necessarily in line with his original meanings. Windelband was a Neo-Kantian who protested other Neo-Kantians of his time and maintained that \"to understand Kant rightly means to go beyond him\". Against his positivist contemporaries, Windelband argued that philosophy should engage in humanistic dialogue with the natural sciences rather than uncritically appropriating its methodologies. His interests in psychology and cultural sciences represented an opposition to psychologism and historicism schools by a critical philosophic system. Windelband relied in his effort to reach beyond Kant on such philosophers as Georg Wilhelm Friedrich Hegel, Johann Friedrich Herbart, and Hermann Lotze. Closely associated with Windelband was Heinrich Rickert. Windelband's disciples were not only noted philosophers, but sociologists like Max Weber and theologians like Ernst Troeltsch and Albert Schweitzer.<generated>Wilhelm Windelband (15 March 1848 – 18 September 1915) was a German philosopher of the late 19th and early 20th centuries. He is now remembered mainly for the terms \"nomothetic\" and \"idiographic,\" which he introduced. He also wrote on history, psychology, the philosophy of religion, values, and other topics. He was a neo-Kantian who protested other neo-Kantians of his time and maintained a critical position towards psychologism. Windelband is known as one of the founders of the \"Baden School\" of neo-Kantianism. He was a student of Kuno Fischer and Franz Brentano. His students included Edmund Husserl, Adolf Reinach, Carl Stumpf, and Richard von Mises.<eval>Wilhelm Windelband (15 March 1848 – 18 September 1915) was a German philosopher of the late 19th and early 20th centuries.<minor_inaccurate>He is now remembered mainly for the terms \"nomothetic\" and \"idiographic,\" which he introduced.<accurate>He also wrote on history, psychology, the philosophy of religion, values, and other topics.<accurate>He was a neo-Kantian who protested other neo-Kantians of his time and maintained a critical position towards psychologism.<accurate>Windelband is known as one of the founders of the \"Baden School\" of neo-Kantianism.<accurate>He was a student of Kuno Fischer and Franz Brentano.<major_inaccurate>His students included Edmund Husserl, Adolf Reinach, Carl Stumpf, and Richard von Mises.<major_inaccurate><stop>"}
{"text": "<truth>Admiral of the Fleet Matthew Aylmer, 1st Baron Aylmer (ca. 1650 - 18 August 1720) was a Royal Navy officer. He was one of the captains who sent a letter to Prince William of Orange, who had just landed at Torbay, assuring the Prince of the captains' support; the Prince's response ultimately led to the Royal Navy switching allegiance to the Prince and the Glorious Revolution of November 1688. Aylmer saw action at the Battle of Bantry Bay in May 1689, at the Battle of Beachy Head in July 1690, and again at the Battle of Barfleur in May 1692 during the Nine Years' War. Aylmer became Commander-in-Chief of the Navy on 12 November 1709. However, when Aylmer met a French squadron and convoy, he was only able to capture one merchantman and the 56-gun \"Superbe\": the new Harley ministry used this failure as an excuse to remove him as Commander-in-Chief and did so a few months later. Following the accession of George I and the appointment of the Townshend ministry, Aylmer was reappointed Commander-in-Chief on 5 November 1714. He was also appointed Governor of Greenwich Hospital: in this post he founded the Royal Hospital School for the sons of seamen.<generated>Matthew Aylmer, 1st Baron Aylmer (1708–1794) was an Irish soldier and colonial administrator. He was born in Dublin, the son of a barrister, and was educated at Trinity College, Dublin. He joined the British Army in 1727 and served in the War of the Austrian Succession and the Seven Years' War. He was promoted to lieutenant-general in 1772 and was appointed Governor of Gibraltar in 1775. He was made a baron in 1782 and was appointed Commander-in-Chief of the British forces in North America in 1783. He was recalled in 1790 and died in London in 1794. He was buried in Westminster Abbey.<eval>Matthew Aylmer, 1st Baron Aylmer (1708–1794) was an Irish soldier and colonial administrator.<minor_inaccurate>He was born in Dublin, the son of a barrister, and was educated at Trinity College, Dublin.<minor_inaccurate>He joined the British Army in 1727 and served in the War of the Austrian Succession and the Seven Years' War.<minor_inaccurate>He was promoted to lieutenant-general in 1772 and was appointed Governor of Gibraltar in 1775.<major_inaccurate>He was made a baron in 1782 and was appointed Commander-in-Chief of the British forces in North America in 1783.<major_inaccurate>He was recalled in 1790 and died in London in 1794.<major_inaccurate>He was buried in Westminster Abbey.<major_inaccurate><stop>"}
```

This dataset teaches your model a special task using special sequences not found elsewhere. It teaches your model how to check another model's generated text against a ground truth and annotate the generated text for hallucinations. We made up special sequences `<truth>`, `<generated>`, `<eval>` and `<stop>` in order to do this. Read more about how to come up with your own special sequences [here](https://docs.together.ai/docs/fine-tuning-task-specific-sequences).   

Use `together.Files.check` to check if your jsonl file has the correct format. Also take a look at it with the editor of your choice. 

```python
resp = together.Files.check(file="antihallucination.jsonl")
print(resp)
```

If the file format is correct, the `is_check_passed` field will be True

```
{'is_check_passed': True,
 'model_special_tokens': 'we are not yet checking end of sentence tokens for this model',
 'file_present': 'File found',
 'file_size': 'File size 0.001 GB',
 'num_samples': 238}
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
resp = together.Files.upload(file="antihallucination.jsonl")
file_id = resp["id"]
```

You will get back the file `id` of the file you just uploaded

```
{'filename': 'antihallucination.jsonl',
 'id': 'file-33ecca00-17ea-4968-ada2-9f82ef2f4cb8',
 'object': 'file',
 'report_dict': {'is_check_passed': True,
  'model_special_tokens': 'we are not yet checking end of sentence tokens for this model',
  'file_present': 'File found',
  'file_size': 'File size 0.001 GB',
  'num_samples': 238}}
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

Now that you have a valid file uploaded to together, you can finetune any of the models listed [here](https://docs.together.ai/docs/models-fine-tuning) using `together.Finetune.create`

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

Unless you set `confirm_inputs=False` in `together.Finetune.create`, or `--quiet` in the CLI, there will be a confirmation step to make sure you are aware of any defaults or arguments that needed to be reset from their original inputs for this specific finetune job. Type `y` then `Enter` to submit the job, or anything else to abort. 

```
10-02-2023 11:14:27 - together.finetune - WARNING - Batch size must be 144 for togethercomputer/llama-2-70b-chat model. Setting batch size to 144 (finetune.py:114)
Note: Some hyperparameters may have been adjusted with their minimum/maximum values for a given model.

Job creation details:
{   'batch_size': 144,
    'learning_rate': 1e-05,
    'model': 'togethercomputer/llama-2-70b-chat',
    'n_checkpoints': 1,
    'n_epochs': 4,
    'suffix': None,
    'training_file': 'file-33ecca00-17ea-4968-ada2-9f82ef2f4cb8',
    'wandb_key': 'xxxx'}

Do you want to submit the job? [y/N]
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

### Using a Downloaded Model

The model will download as a `tar.zst` file

```python
together.Finetune.download(
    fine_tune_id="ft-eb167402-98ed-4ac5-b6f5-8140c4ba146e",
    output = "my-model/model.tar.zst"
)
```

To uncompress this filetype on Mac you need to install zstd. 

```
brew install zstd
cd my-model
zstd -d model.tar.zst
tar -xvf model.tar
cd ..
```

Within the folder that you uncompress the file, you will find a set of files like this:  
`ls my-model`

```
tokenizer_config.json
special_tokens_map.json
pytorch_model.bin
generation_config.json
tokenizer.json
config.json
```

Use the folder path that contains these `.bin` and `.json` files to load your model

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("./my-model")

model = AutoModelForCausalLM.from_pretrained(
  "./my-model", 
  trust_remote_code=True, 
).to(device)

input_context = "Space Robots are"
input_ids = tokenizer.encode(input_context, return_tensors="pt")
output = model.generate(input_ids.to(device), max_length=128, temperature=0.7).cpu()
output_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(output_text)
```

```
Space Robots are a great way to get your kids interested in science. After all, they are the future!
```

## Colab Tutorial

Follow along in our Colab (Google Colaboratory) Notebook Tutorial [Example Finetuning Project](https://colab.research.google.com/drive/11DwtftycpDSgp3Z1vnV-Cy68zvkGZL4K?usp=sharing).

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
