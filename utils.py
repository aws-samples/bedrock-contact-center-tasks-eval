import re
import os
import json
import boto3
import logging
import numpy as np
from numpy import dot
from typing import List, Dict
from numpy.linalg import norm
from rouge_score import rouge_scorer
from tokenizer_utils import count_tokens
from bedrock_utils import get_bedrock_client

MAX_TEXT_LEN_FOR_EMBEDDING: int = 500

logger = logging.getLogger(__name__)
bedrock = None

def _get_embedding(text, modelId='amazon.titan-embed-text-v1', accept='application/json', contentType='application/json'):
    global bedrock
    if bedrock is None:
        bedrock = get_bedrock_client()
    body = json.dumps({"inputText": text[:MAX_TEXT_LEN_FOR_EMBEDDING]})
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    token_count = response_body.get('inputTextTokenCount')
    return embedding, token_count

def get_cosine_similarity(text1: str, text2: str) -> float:
    A,_ = _get_embedding(text1)
    B,_ = _get_embedding(text2)
    cosine = dot(A, B)/(norm(A)*norm(B))
    return cosine

def write_results(cve_id: str, model_id: str, metrics_dir: str, **kwargs):
    metrics = dict(cve=cve_id, model_id=model_id) | {**kwargs}
    dir_path = os.path.join(metrics_dir, cve_id)
    os.makedirs(dir_path, exist_ok=True)
    fpath = os.path.join(dir_path, f"{model_id}.json")
    with open(fpath, "w") as f:
        f.write(json.dumps(metrics, indent=2))
                            

def get_rouge_l_score(completion: str, golden: str) -> float:
    scorer = rouge_scorer.RougeScorer(['rougeL'])
    scores = scorer.score(golden, completion)
    return round(scores['rougeL'].fmeasure, 4)

def is_amazon_model(model_id: str) -> bool:
    return model_id.split(".")[0] == "amazon"

def is_amazon_model(model_id: str) -> bool:
    return model_id.split(".")[0] == "amazon"

def parse_model_response(model_id: str, resp: Dict) -> Dict:
    model_family = model_id.split(".")[0]
    if model_family == "amazon":
        return dict(completion=resp['results'][0]['outputText'],
                    prompt_token_count=resp['inputTextTokenCount'],
                    completion_token_count=resp['results'][0]['tokenCount'])
    if model_family == "cohere":
        token_count  = int(len(resp['generations'][0]['text'].split())*(1000/750))
        return dict(completion=resp['generations'][0]['text'],
                    prompt_token_count=None,
                    completion_token_count=token_count)
    if model_family == "anthropic":        
        return dict(completion=resp['completion'],
                    prompt_token_count=None,
                    completion_token_count=count_tokens(resp['completion']))
    if model_family == "meta":    
        return dict(completion=resp['generation'],
                    prompt_token_count=resp['prompt_token_count'],
                    completion_token_count=resp['generation_token_count'])
    return dict(completion=None, completion_token_count=None)
