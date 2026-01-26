from fastapi import FastAPI
from .options import configure_cors


def setup_middleware(app: FastAPI) -> None:
    configure_cors(app)
