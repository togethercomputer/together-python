# Session constants
TIMEOUT_SECS = 600
MAX_SESSION_LIFETIME_SECS = 180
MAX_CONNECTION_RETRIES = 2

# API defaults
BASE_URL = "https://api.together.xyz/v1"

# Download defaults
DOWNLOAD_BLOCK_SIZE = 10 * 1024 * 1024  # 10 MB
DOWNLOAD_CONCURRENCY = 32
DISABLE_TQDM = False

# Messages
MISSING_API_KEY_MESSAGE = """TOGETHER_API_KEY not found.
Please set it as an environment variable or set it as together.api_key
Find your TOGETHER_API_KEY at https://api.together.xyz/settings/api-keys"""
