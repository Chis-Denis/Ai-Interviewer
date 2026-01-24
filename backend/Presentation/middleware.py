from fastapi import FastAPI
from Presentation.Options.cors import configure_cors


def setup_middleware(app: FastAPI) -> None:
    configure_cors(app)
