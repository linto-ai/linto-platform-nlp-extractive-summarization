#!/usr/bin/env python3

import json
import logging
from time import time

import spacy
import components

from flask import Flask, request, abort, Response, json
from serving import GunicornServing
from confparser import createParser
from swagger import setupSwaggerUI

from extsumm.processing import LM_MAP, MODELS, get_model
from extsumm.processing.utils import get_data


app = Flask("__extsumm-worker__")
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger("__extsumm-worker__")

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return json.dumps({"healthcheck": "OK"}), 200

@app.route("/oas_docs", methods=['GET'])
def oas_docs():
    return "Not Implemented", 501

@app.route("/extsumm/<lang>", methods=['POST'])
def extsumm(lang: str):
    """Process a batch of articles and return the extractive summaries predicted by the
    given model. Each record in the data should have a key "text".
    """
    logger.info('ExtSumm request received')

    # Check language availability
    if lang in LM_MAP.keys():
        model_name = LM_MAP[lang]
        if model_name not in MODELS.keys():
            raise RuntimeError(f"Model {model_name} for language {lang} is not loaded.")
        nlp = spacy.blank(lang)
        nlp.add_pipe("sentencizer", config={"punct_chars": ['|']})
        nlp.add_pipe("extsumm", config={"model": {"@misc": "get_model", "name": model_name}})
    else:
        raise ValueError(f"Language {lang} is not supported.")
    
    response_body = []
    request_body = json.loads(request.data)
    texts = [article["text"] for article in request_body.get("articles", [])]
    
    component_cfg = request_body.get("component_cfg", {})

    for doc in nlp.pipe(texts, component_cfg=component_cfg):
        response_body.append(get_data(doc))

    return {"extsumm": response_body}, 200

# Rejected request handlers
@app.errorhandler(405)
def method_not_allowed(error):
    return 'The method is not allowed for the requested URL', 405

@app.errorhandler(404)
def page_not_found(error):
    return 'The requested URL was not found', 404

@app.errorhandler(500)
def server_error(error):
    logger.error(error)
    return 'Server Error', 500

if __name__ == '__main__':
    logger.info("Startup...")

    parser = createParser()
    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    try:
        # Setup SwaggerUI
        if args.swagger_path is not None:
            setupSwaggerUI(app, args)
            logger.debug("Swagger UI set.")
    except Exception as e:
        logger.warning("Could not setup swagger: {}".format(str(e)))
    
    serving = GunicornServing(app, {'bind': '{}:{}'.format("0.0.0.0", args.service_port),
                                    'workers': args.workers,})
    logger.info(args)
    try:
        serving.run()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(str(e))
        logger.critical("Service is shut down (Error)")
        exit(e)
