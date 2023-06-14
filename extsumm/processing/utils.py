from typing import Dict, Any

from spacy.tokens import Doc

def get_data(doc: Doc) -> Dict[str, Any]:
    """Extract the data to return from the REST API given a Doc object. Modify
    this function to include other data."""
    
    return {"text": doc.text, "extractive_summary": doc._.extractive_summary}
    