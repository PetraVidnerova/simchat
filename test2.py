import logging
import sys
import time

import pandas as pd

from agent import Agent
from converse import ConversationModule
from utils import random_order, nice_time, create_logger

BASEDIR = "./agents/"


logger = create_logger(__name__)

agent_names = ["Isabella", "Klaus", "Maria"]  # next(os.walk(BASEDIR))[1]
agent_dirs = [f"{BASEDIR}{agent_name}/" for agent_name in agent_names]


agents = {
    name: Agent(d)
    for name, d in zip(agent_names, agent_dirs)
}


def interactive_mode():
    while True:
        
        fields = input("> ").strip().split()

        if not fields:
            continue
        
        command = fields[0]

        if command == "c":
            have_conversation(
                agents[fields[1]],
                agents[fields[2]]
            )
            
        elif command == "m":
            print(agents[fields[1]].memory.memory)

        elif command == "a":
            ret = ask(agents[fields[1]])
            if ret is None:
                print("UGH")
            else:
                print(ret)

        elif command == "e":
            break

def ask(agent):
    ret = {} 
    question = f""" Am I aware about Valentines party? 
Output only one word.
Output format examples: 
*YES*
*NO* 
Return '*YES*' if yes, else return '*NO*'.
        """
    for trial in range(3):
        answer = agent.inquiry(question) 
        logger.info(f"{agent.name.upper()} answers: {answer}")
        bool_answer = cm.answer_to_bool(answer) 
        if bool_answer is not None:
            return bool_answer            
    return None


        
def have_conversation(agent1, agent2):
    conversation = ""

    logger.info(f"{agent1.name.upper()} meets {agent2.name.upper()}")
    sentence = agent1.start_conversation(agent2.name)
    logger.info(f"{sentence}")

    fact = cm.summary_message(sentence, agent1.name)
    agent2.memory.memory.append(fact)
    if agent1 in agent2.memory.other_agents:
        agent2.memory.other_agents[agent1.name].append(fact)
    else:
        agent2.memory.other_agents[agent1.name] = [fact]
        


    
    chats = 6
    while chats:
        conversation += sentence
        logger.info(f"{agent2.name.upper()} SPEAKS:")
        sentence = agent2.converse(agent1.name, conversation)
        logger.info(sentence)

        fact = cm.summary_message(sentence, agent2.name)
        agent1.memory.memory.append(fact)
        if agent2 in agent1.memory.other_agents:
            agent1.memory.other_agents[agent2.name].append(fact)
        else:
            agent1.memory.other_agents[agent2.name] = [fact]
        
        chats -= 1
        agent1, agent2 = agent2, agent1
        if cm.is_ending(sentence):
            break
    print("CONVERSATION ENDS")

# Isabella = agents["Isabella"]
# Klaus = agents["Klaus"]
# Maria = agents["Maria"]
    
cm = ConversationModule()

# s = time.time()
# for i in range(10):
#     have_conversation(*random_order(Isabella, Klaus))
#     have_conversation(*random_order(Klaus, Maria))
# e = time.time()

# h, m, s = nice_time(e-s)

# print(f"Time: {h}h {m}m {s}s")

interactive_mode()
