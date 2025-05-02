import os
import logging
import sys
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from ._configuration import Configuration
from app.services.api_manager import APIManager

load_dotenv('.env', override=True)

info_log_file = os.path.join("logs", "worker_info.log")
error_log_file = os.path.join("logs", "worker_error.log")

if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure the info file handler to log info and above
info_handler = RotatingFileHandler(
    info_log_file,
    maxBytes=10 ** 6,
    backupCount=5,
    encoding='utf-8'
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)

# Configure the error file handler to log only errors
error_handler = RotatingFileHandler(
    error_log_file, maxBytes=10 ** 6, backupCount=5, encoding='utf-8'
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
)

# Configure the stream handler to log all levels to the console
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[info_handler, error_handler, stream_handler]
)

config = Configuration(
    APP_ID=os.getenv('APP_ID'),
    APP_SECRET=os.getenv('APP_SECRET'),
    BITABLE_TOKEN=os.getenv('BITABLE_TOKEN'),
    UNPROCESSED_TABLE_ID=os.getenv('UNPROCESSED_TABLE_ID'),
    VERSION=os.getenv('VERSION'),
    ENVIRONMENT=os.getenv('ENV')
)

groq_api_keys = [
    os.getenv("GROQ_API_KEY"),
]

groq_api_keys_manager = APIManager(groq_api_keys)
