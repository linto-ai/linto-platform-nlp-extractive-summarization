from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Article(BaseModel):
    # Schema for a single article in a batch of articles to process
    text: str


class RequestModel(BaseModel):
    # Schema for a request consisting a batch of articles, and component configuration
    articles: List[Article]
    component_cfg: Optional[Dict[str, Dict[str, Any]]] = None


class ExtsummResponseModel(BaseModel):
    # This is the schema of the expected response and depends on what you
    # return from get_data.

    class Batch(BaseModel):
        text: str
        extractive_summary: List[str] = []

    extsumm: List[Batch]
