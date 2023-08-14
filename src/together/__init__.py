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
 'togethercomputer/LLaMA-2-7B-32K',
 'togethercomputer/llama-2-7b',
 'togethercomputer/llama-2-7b-chat',
 'togethercomputer/llama-2-13b-chat',
 'togethercomputer/llama-2-13b',
 'togethercomputer/RedPajama-INCITE-7B-Base',
 'togethercomputer/RedPajama-INCITE-7B-Chat',
 'togethercomputer/RedPajama-INCITE-7B-Instruct',
 'togethercomputer/RedPajama-INCITE-Base-3B-v1',
 'togethercomputer/RedPajama-INCITE-Chat-3B-v1',
 'togethercomputer/RedPajama-INCITE-Instruct-3B-v1',
 'togethercomputer/Pythia-Chat-Base-7B',
]

model_list = Models.list()
all_model_names = [model_dict['name'] for model_dict in model_list]

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
    "model_names",
    "finetune_model_names",
]