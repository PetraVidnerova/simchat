from ollama import Client                                                                                   

import json
import numpy as np
import  requests
import time

import logging

import cohere

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import numpy as np

from utils import create_logger

logger = create_logger(__name__, filename="chat_debug.log", level=logging.DEBUG, console_output=False)

class OllamaChat():

    def __init__(self):
        self.theta = 0.4
        self.client = Client(host='http://localhost:11434')
        
    def complete(self, prompt):
        
        logger.debug(prompt)
        
        response = self.client.chat(model='jean-luc/tiger-gemma-9b-v3:fp16', messages=[                                  
            {                                                                                                         
                'content': prompt,                                                                      
                'role': 'user',                                                                                         
            },                                                                                                        
        ])                                                                                                          
                                                                                                            
        return response["message"]["content"]

    def get_embedding(self, sentence):
       response = self.client.embed(model='jean-luc/tiger-gemma-9b-v3:fp16', input=sentence)
       res = [float(x) for x in response["embeddings"][0]]
       return np.array(res, dtype=float)



class Chat():

    def __init__(self):
        self.theta = 0.23
    
    def complete(self, prompt):
        
        query  = {"prompt": prompt}
        res = requests.post("http://127.0.0.1:5000/query", json=query)

        json_res = res.json()
        if "response" not in json_res:
            print(json_res)
            raise NotImplementedError
        
        return json_res["response"]


    def get_embedding(self, sentence):
        
        if not sentence:                                                                                              
            sentence = "this is blank"                                                                                  
                                                                                                            
        query = {"sentences": [sentence]}                                                                             
        res = requests.post("http://127.0.0.1:5000/embed", json=query)                                            
        completion = res.json()["embeddings"]                                                                     
        return np.array(completion[0], dtype=float)

    
class CoChat():
        
    def __init__(self):
        
        with open("api_key2.txt", "r") as f:
            openai_api_key = f.read().strip()

        self.co = cohere.Client(openai_api_key)
        self.theta = 0.5 
        
    def complete(self, prompt):

        for _ in range(10):
            try:
                completion = self.co.chat( 
                    message=prompt
                )
            except:
                print("chat error - sleeping")
                time.sleep(10)
                continue
    
            return completion.text
        else:
            raise ValueError("chat error")

    def get_embedding(self, sentence):

        for _ in range(10):
            try:
                result = self.co.embed(
                    texts = [sentence],
                    model = "embed-english-v3.0",
                    input_type = "classification" #todo what is the best
                )
            except:
                print("chat error - sleeping")
                time.sleep(10)
                continue
            return result.embeddings[0]
        else:
            raise ValueError("chat error")


def get_chat_interface(cohere=False):
    if cohere:
        chat = CoChat()
    else:
        chat = OllamaChat()
    
    return chat
