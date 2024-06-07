import os
import random
import logging
import sys 

import pandas as pd

from agent import Agent 
from converse import ConversationModule


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

agent_names  = next(os.walk(BASEDIR))[1]
agent_dirs = [f"{BASEDIR}{agent_name}/" for agent_name in agent_names]



agents = {
    name: Agent(d)
    for name, d in zip(agent_names, agent_dirs)
}


# for a in agents:
#     print(a.introduce_yourself())

# exit()

person1, person2, person3 = agents.values()

cm = ConversationModule()
print(cm)



def run(steps):
    i = 1
    for _ in range(steps):

        print("*"*(steps+1-i))
              
        i += 1
        
        if i%2:
            agent1, agent2 = random.sample([person1, person2], 2)
        else:
            agent1, agent2 = random.sample([person2, person3], 2)
        

        conv = agent1.start_conversation(agent2.name)
            
        logger.info(f"{agent1.name} meets  {agent2.name}")
        logger.info(conv)
        
        fact = cm.summary_message(conv, agent1)
        agent2.memory.memory.append(fact)

        for _ in range(6):
            agent1, agent2 = agent2, agent1

            answer = agent1.converse(agent2.name, conv)
            logger.info(answer)
            conv += "\n"+answer

            fact = cm.summary_message(answer, agent1)
            agent2.memory.memory.append(fact)
        
            if cm.is_ending(answer):
                break
        
        # for a in agent1, agent2:     
        #     asum = cm.summary(conv, a)
        #     logger.info(asum)
        #     a.memory.memory.extend(asum)

        aboutsum = cm.partner_knowledge(conv, agent1)
        agent2.memory.add_agent_knowledge(agent1.name, aboutsum)

        aboutsum = cm.partner_knowledge(conv, agent2)
        agent1.memory.add_agent_knowledge(agent2.name, aboutsum)

def ask():
    ret = {} 
    for name, a in agents.items():
        question = f""" Does {a.name} know about Valentines party? 
Output format examples: 
*YES*
*NO* 
Return '*YES*' if yes, else return '*NO*'.
        """
        answer = a.inquiry(question) 
        logger.info(f"{a.name.upper()} answers: {answer}")
        bool_answer = cm.answer_to_bool(answer) 
        ret[a.name] = bool_answer
    return ret 

def interactive_mode():
    while True:
        command = input("> ").strip()

        if command.startswith("run"):
            _, number = command.split()
            number = int(number)
            run(number)

        elif command.startswith("memory"):
            _, name = command.split()
            print(agents[name].memory.memory)


        elif command == "ask":
            ask()

        elif command == "exit":
            break


def experiment1():
    global filename
    
    ret_list = []
    ret_list.append(ask())

    for _ in range(5):
        run(2)
        ret_list.append(ask())

    df = pd.DataFrame(ret_list)
    df.to_csv(f"{filename}.csv")



experiment1() 

    
