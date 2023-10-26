import os
import sys
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

MISSING_API_KEY_MESSAGE = """TOGETHER_API_KEY not found.
Please set it as an environment variable or set it as together.api_key
Find your TOGETHER_API_KEY at https://api.together.xyz/settings/api-keys"""

MAX_CONNECTION_RETRIES = 2
BACKOFF_FACTOR = 0.2

min_samples = 100

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
    "MAX_CONNECTION_RETRIES",
    "MISSING_API_KEY_MESSAGE",
    "BACKOFF_FACTOR",
    "min_samples",
]
