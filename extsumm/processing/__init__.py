import os
import sys
import spacy
from time import time

from extsumm import logger
from extsumm.processing.utils import get_data

from sentence_transformers import SentenceTransformer

__all__ = ["logger", "get_data", "LM_MAP", "MODELS", "get_model"]

logger.info("Loading language model(s)...")
start = time()

# Supported languages and corresponding model names
LM_MAP = {
    "fr": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "en": "sentence-transformers/all-MiniLM-L6-v2"
    }

try:
    MODELS = {LM_MAP[lang]: SentenceTransformer(os.environ.get("ASSETS_PATH_IN_CONTAINER") + '/' + LM_MAP[lang]) for lang in os.environ.get("APP_LANG").split(" ")}
except Exception as err:
    raise Exception("Failed to load model(s): {}".format(str(err))) from err
    sys.exit(-1)

@spacy.registry.misc("get_model")
def get_model(name):
    return MODELS[name]   

logger.info(f"(t={time() - start}s). Loaded {len(MODELS)} models: {MODELS.keys()}.")