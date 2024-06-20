import numpy as np
import  requests
import time

import cohere 

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

# with open("api_key.txt", "r") as f:
#     openai_api_key = f.read().strip()

# co = cohere.Client(openai_api_key)

# def complete(prompt):

#     for _ in range(10):
#         try:
#             completion = co.chat( 
#                 message=prompt
#             )
#         except:
#             print("chat error - sleeping")
#             time.sleep(10)
#             continue
    
#         return completion.text
#     else:
#         raise ValueError("chat error")

# def get_embedding(sentence):

#     for _ in range(10):
#         try:
#             result = co.embed(
#                 texts = [sentence],
#                 model = "embed-english-v3.0",
#                 input_type = "classification" #todo what is the best
#             )
#         except:
#             print("chat error - sleeping")
#             time.sleep(10)
#             continue
#         return result.embeddings[0]
#     else:
#         raise ValueError("chat error")


