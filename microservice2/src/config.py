import os

from dotenv import load_dotenv

load_dotenv()

INFURA_ENDPOINT: str = os.getenv("INFURA_ENDPOINT")
GRPC_ADDRESS: str = os.getenv("GRPC_ADDRESS")
