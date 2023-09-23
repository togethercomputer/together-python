import os
import urllib.parse

from .config import (
    finetune_model_names,
    jokes_list,
    min_samples,
    model_info_dict,
)
from .version import VERSION


version = VERSION
# print(version)
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

from .complete import Complete
from .error import *
from .files import Files
from .finetune import Finetune
from .image import Image
from .models import Models


__all__ = [
    "api_key",
    "api_base",
    "api_base_complete",
    "api_base_files",
    "api_base_finetune",
    "api_base_instances",
    "default_text_model",
    "default_image_model",
    "Models",
    "Complete",
    "Files",
    "Finetune",
    "Image",
    "model_info_dict",
    "finetune_model_names",
    "min_samples",
    "jokes_list",
]
