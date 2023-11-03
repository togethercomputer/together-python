import os
import sys
import urllib.parse

from .version import VERSION

import requests
from typing import Optional, Union, Callable

version = VERSION

api_key = os.environ.get("TOGETHER_API_KEY", None)

api_base = "https://api.together.xyz/"
api_complete_path = "/api/inference"
api_files_path = "/v1/files/"
api_finetune_path = "/v1/fine-tunes/"
api_instances_path = "instances/"

default_text_model = "togethercomputer/RedPajama-INCITE-7B-Chat"
default_image_model = "runwayml/stable-diffusion-v1-5"

requestssession: Optional[
    Union["requests.Session", Callable[[], "requests.Session"]]
] = None # Provide a requests.Session or Session factory.

min_samples = 100

from .complete import Complete
from .files import Files
from .finetune import Finetune
from .image import Image
from .models import Models


__all__ = [
    "api_key",
    "api_base",
    "api_complete_path",
    "api_files_path",
    "api_finetune_path",
    "api_instances_path",
    "default_text_model",
    "default_image_model",
    "Models",
    "Complete",
    "Files",
    "Finetune",
    "Image",
    "min_samples",
    "requestssession",
]
