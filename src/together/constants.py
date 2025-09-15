import enum

# Session constants
TIMEOUT_SECS = 600
MAX_SESSION_LIFETIME_SECS = 180
MAX_CONNECTION_RETRIES = 2
MAX_RETRIES = 5
INITIAL_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 8.0

# API defaults
BASE_URL = "https://api.together.xyz/v1"

# Download defaults
DOWNLOAD_BLOCK_SIZE = 10 * 1024 * 1024  # 10 MB
DISABLE_TQDM = False

# Upload defaults
MAX_CONCURRENT_PARTS = 4  # Maximum concurrent parts for multipart upload

# Multipart upload constants
MIN_PART_SIZE_MB = 5  # Minimum part size (S3 requirement)
TARGET_PART_SIZE_MB = 100  # Target part size for optimal performance
MAX_MULTIPART_PARTS = 250  # Maximum parts per upload (S3 limit)
MULTIPART_UPLOAD_TIMEOUT = 300  # Timeout in seconds for uploading each part
MULTIPART_THRESHOLD_GB = 5.0  # threshold for switching to multipart upload

# maximum number of GB sized files we support finetuning for
MAX_FILE_SIZE_GB = 25.0


# Messages
MISSING_API_KEY_MESSAGE = """TOGETHER_API_KEY not found.
Please set it as an environment variable or set it as together.api_key
Find your TOGETHER_API_KEY at https://api.together.xyz/settings/api-keys"""

# Minimum number of samples required for fine-tuning file
MIN_SAMPLES = 1

# the number of bytes in a gigabyte, used to convert bytes to GB for readable comparison
NUM_BYTES_IN_GB = 2**30


# expected columns for Parquet files
PARQUET_EXPECTED_COLUMNS = ["input_ids", "attention_mask", "labels"]


class DatasetFormat(enum.Enum):
    """Dataset format enum."""

    GENERAL = "general"
    CONVERSATION = "conversation"
    INSTRUCTION = "instruction"
    PREFERENCE_OPENAI = "preference_openai"


JSONL_REQUIRED_COLUMNS_MAP = {
    DatasetFormat.GENERAL: ["text"],
    DatasetFormat.CONVERSATION: ["messages"],
    DatasetFormat.INSTRUCTION: ["prompt", "completion"],
    DatasetFormat.PREFERENCE_OPENAI: [
        "input",
        "preferred_output",
        "non_preferred_output",
    ],
}
REQUIRED_COLUMNS_MESSAGE = ["role", "content"]
POSSIBLE_ROLES_CONVERSATION = ["system", "user", "assistant"]
