import os
import random
import logging
import sys

import pandas as pd

from agent import Agent 
from converse import ConversationModule
from utils import random_order

BASEDIR="./agents/"


logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

filename = sys.argv[1]
file_handler = logging.FileHandler(f'{filename}.log')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

agent_names  = ["Isabella", "Klaus", "Maria"] #next(os.walk(BASEDIR))[1]
agent_dirs = [f"{BASEDIR}{agent_name}/" for agent_name in agent_names]



agents = {
    name: Agent(d)
    for name, d in zip(agent_names, agent_dirs)
}

# for a in agents.values():
#     print(a.introduce_yourself())
#     print()


def have_conversation(agent1, agent2):
    conversation = ""

    print(f"{agent1.name.upper()} meets {agent2.name.upper()}")
    sentence = agent1.start_conversation(agent2.name)
    print(sentence)

    chats = 6
    while chats:
        conversation += sentence
        print(f"{agent2.name.upper()} SPEAKS:")
        sentence = agent2.converse(agent1.name, conversation)
        print(sentence)
        chats -= 1
        agent1, agent2 = agent2, agent1
        if cm.is_ending(sentence):
            break
    print("CONVERSATION ENDS")
     

Isabella = agents["Isabella"]
Klaus = agents["Klaus"]
Maria = agents["Maria"]
    
cm = ConversationModule()


have_conversation(*random_order(Isabella, Klaus))
have_conversation(*random_order(Klaus, Maria))
