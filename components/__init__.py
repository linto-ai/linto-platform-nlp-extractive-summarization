import spacy
from spacy.language import Language
from typing import List, Union, Tuple
from sentence_transformers import SentenceTransformer
from thinc.api import Config
from components.extractive_summarizer import ExtractiveSummarizer

# Load components' defaut configuration
config = Config().from_disk("components/config.cfg")

@Language.factory("extsumm", default_config=config["components"]["extsumm"])
def make_extractive_summarizer(
    nlp: Language,
    name: str,
    model: SentenceTransformer,
    ratio: float = 0.2,
    use_first: bool = False,
    algorithm: str = 'kmeans',
    num_sentences: int = None,
    return_as_list: bool = True
    ):

    kwargs = locals()
    del kwargs['nlp']
    del kwargs['name']
    del kwargs['model']

    return ExtractiveSummarizer(model, **kwargs)

