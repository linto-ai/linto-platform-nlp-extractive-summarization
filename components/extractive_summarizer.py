from spacy.tokens import Doc
from components.bert_extractive_summarizer.sbert import SBertSummarizer

class ExtractiveSummarizer:
    """
    Wrapper class for SBertSummarizer.
    """
    def __init__(self, model, **kwargs):
        self.model = SBertSummarizer(model)
        self.kwargs = kwargs
        if not Doc.has_extension("extractive_summary"):
            Doc.set_extension("extractive_summary", default=[])

    def __call__(self, doc, **kwargs):
        runtime_kwargs = {}
        runtime_kwargs.update(self.kwargs)
        runtime_kwargs.update(kwargs)
        sentences = [sent.text.split('|')[0].strip() for sent in doc.sents]
        doc._.extractive_summary = self.model.run(sentences, **runtime_kwargs)
        
        return doc
