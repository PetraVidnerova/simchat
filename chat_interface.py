import numpy as np
import  requests


def complete(prompt):
    
    query  = {"prompt": prompt}
    res = requests.post("http://127.0.0.1:5000/query", json=query)

    return res.json()["response"]


def get_embedding(sentence):

    if not sentence:                                                                                              
        sentence = "this is blank"                                                                                  
                                                                                                            
    query = {"sentences": [sentence]}                                                                             
    res = requests.post("http://127.0.0.1:5000/embed", json=query)                                            
    completion = res.json()["embeddings"]                                                                     
    return np.array(completion[0], dtype=float)      
