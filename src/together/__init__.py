import os
import urllib.parse

from .version import VERSION


version = VERSION

user_agent = f"TogetherPythonOfficial/{version}"

api_key = os.environ.get("TOGETHER_API_KEY", None)

api_base = "https://api.together.xyz/"
api_base_complete = urllib.parse.urljoin(api_base, "/api/inference")
api_base_files = urllib.parse.urljoin(api_base, "/v1/files/")
api_base_finetune = urllib.parse.urljoin(api_base, "/v1/fine-tunes/")
api_base_instances = urllib.parse.urljoin(api_base, "instances/")

default_text_model = "togethercomputer/RedPajama-INCITE-7B-Chat"
default_image_model = "runwayml/stable-diffusion-v1-5"
log_level = "WARNING"

from .utils.utils import get_logger, verify_api_key, extract_time  # noqa
from .models import Models
from .complete import Complete
from .error import *
from .files import Files
from .finetune import Finetune
from .image import Image

finetune_model_names = [
    "togethercomputer/LLaMA-2-7B-32K",
    "togethercomputer/llama-2-7b",
    "togethercomputer/llama-2-7b-chat",
    "togethercomputer/llama-2-13b-chat",
    "togethercomputer/llama-2-13b",
    "togethercomputer/RedPajama-INCITE-7B-Base",
    "togethercomputer/RedPajama-INCITE-7B-Chat",
    "togethercomputer/RedPajama-INCITE-7B-Instruct",
    "togethercomputer/RedPajama-INCITE-Base-3B-v1",
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
    "togethercomputer/RedPajama-INCITE-Instruct-3B-v1",
    "togethercomputer/Pythia-Chat-Base-7B",
]

model_info_dict = {'EleutherAI/gpt-j-6b': {},
 'EleutherAI/gpt-neox-20b': {},
 'EleutherAI/pythia-12b-v0': {},
 'EleutherAI/pythia-1b-v0': {},
 'EleutherAI/pythia-2.8b-v0': {},
 'EleutherAI/pythia-6.9b': {},
 'HuggingFaceH4/starchat-alpha': {},
 'NousResearch/Nous-Hermes-13b': {},
 'NousResearch/Nous-Hermes-Llama2-13b': {},
 'NumbersStation/nsql-6B': {},
 'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5': {},
 'OpenAssistant/stablelm-7b-sft-v7-epoch-3': {},
 'bigcode/starcoder': {},
 'databricks/dolly-v2-12b': {},
 'databricks/dolly-v2-3b': {},
 'databricks/dolly-v2-7b': {},
 'google/flan-t5-xl': {},
 'huggyllama/llama-13b': {},
 'huggyllama/llama-30b': {},
 'huggyllama/llama-7b': {},
 'lmsys/fastchat-t5-3b-v1.0': {},
 'lmsys/vicuna-13b-v1.3': {},
 'lmsys/vicuna-7b-v1.3': {},
 'prompthero/openjourney': {},
 'runwayml/stable-diffusion-v1-5': {},
 'stabilityai/stable-diffusion-2-1': {},
 'stabilityai/stable-diffusion-xl-base-1.0': {},
 'stabilityai/stablelm-base-alpha-3b': {},
 'stabilityai/stablelm-base-alpha-7b': {},
 'tatsu-lab/alpaca-7b-wdiff': {},
 'timdettmers/guanaco-7b': {},
 'togethercomputer/GPT-JT-6B-v1': {},
 'togethercomputer/GPT-JT-Moderation-6B': {},
 'togethercomputer/GPT-NeoXT-Chat-Base-20B': {},
 'togethercomputer/Koala-7B': {},
 'togethercomputer/LLaMA-2-7B-32K': {'bos_token':'<s>','eos_token':'</s>'},
 'togethercomputer/Pythia-Chat-Base-7B-v0.16': {'eos_token': '<|endoftext|>'},
 "togethercomputer/Pythia-Chat-Base-7B": {'eos_token': '<|endoftext|>'},
 'togethercomputer/RedPajama-INCITE-7B-Base': {'eos_token': '<|endoftext|>'},
 'togethercomputer/RedPajama-INCITE-7B-Chat': {'eos_token': '<|endoftext|>'},
 'togethercomputer/RedPajama-INCITE-7B-Instruct': {'eos_token': '<|endoftext|>'},
 'togethercomputer/RedPajama-INCITE-Base-3B-v1': {'eos_token': '<|endoftext|>'},
 'togethercomputer/RedPajama-INCITE-Chat-3B-v1': {'eos_token': '<|endoftext|>'},
 'togethercomputer/RedPajama-INCITE-Instruct-3B-v1': {'eos_token': '<|endoftext|>'},
 'togethercomputer/codegen2-16B': {},
 'togethercomputer/codegen2-7B': {},
 'togethercomputer/falcon-40b-instruct': {},
 'togethercomputer/falcon-40b': {},
 'togethercomputer/falcon-7b-instruct': {},
 'togethercomputer/falcon-7b': {},
 'togethercomputer/llama-2-13b-chat': {'bos_token':'<s>','eos_token':'</s>'},
 'togethercomputer/llama-2-13b': {'bos_token':'<s>','eos_token':'</s>'},
 'togethercomputer/llama-2-70b-chat': {'bos_token':'<s>','eos_token':'</s>'},
 'togethercomputer/llama-2-70b': {'bos_token':'<s>','eos_token':'</s>'},
 'togethercomputer/llama-2-7b-chat': {'bos_token':'<s>','eos_token':'</s>'},
 'togethercomputer/llama-2-7b': {'bos_token':'<s>','eos_token':'</s>'},
 'togethercomputer/mpt-30b-chat': {},
 'togethercomputer/mpt-30b': {},
 'togethercomputer/mpt-7b-chat': {},
 'togethercomputer/mpt-7b-instruct': {},
 'togethercomputer/mpt-7b': {},
 'togethercomputer/replit-code-v1-3b': {}}

__all__ = [
    "api_key",
    "api_base",
    "api_base_complete",
    "api_base_files",
    "api_base_finetune",
    "api_base_instances",
    "default_text_model",
    "default_image_model",
    "get_logger",
    "verify_api_key",
    "extract_time",
    "Models",
    "Complete",
    "Files",
    "Finetune",
    "Image",
    "model_info_dict",
    "finetune_model_names",
]
