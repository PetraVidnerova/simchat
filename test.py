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

person1, person2, person3, person4 = agents.values()

cm = ConversationModule()
print(cm)



def run(steps, agent_couples=None):
    i = 1
    for _ in range(steps):

        print("*"*(steps+1-i))
              
        i += 1

        if agent_couples is None:
            if i%2:
                agent1, agent2 = random.sample([person1, person2], 2)
            else:
                agent1, agent2 = random.sample([person2, person3], 2)
        else:
            agent1, agent2 = agent_couples[i-2]
                

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
        #     logger.info(asum)
        #     a.memory.memory.extend(asum)
        #     asum = cm.summary(conv, a)

        aboutsum = cm.partner_knowledge(conv, agent1)
        agent2.memory.add_agent_knowledge(agent1.name, aboutsum)

        aboutsum = cm.partner_knowledge(conv, agent2)
        agent1.memory.add_agent_knowledge(agent2.name, aboutsum)

def ask(target_agents=None):
    ret = {} 
    for name, a in agents.items():
        if target_agents is not None and name not in target_agents:
            continue
        question = f""" Does {a.name} know about Valentines party? 
Output format examples: 
*YES*
*NO* 
Return '*YES*' if yes, else return '*NO*'.
        """
        for trial in range(3):
            answer = a.inquiry(question) 
            logger.info(f"{a.name.upper()} answers: {answer}")
            bool_answer = cm.answer_to_bool(answer) 
            if bool_answer is not None:
                ret[a.name] = bool_answer
                break
        else:
            ret[a.name] = None
            
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

def experiment1b():
    global filename

    ret_list = []
    ret_list.append(ask(target_agents=["Isabella", "Maria", "Klaus"]))

    for _ in range(5):
        agent_couples = [
            random.sample([agents["Isabella"], agents["Maria"]], 2),
            random.sample([agents["Maria"], agents["Klaus"]], 2)
        ]
        run(2, agent_couples)
        ret_list.append(ask(target_agents=["Isabella", "Maria", "Klaus"]))

    df = pd.DataFrame(ret_list)
    df.to_csv(f"{filename}.csv")
    

def experiment2():

    ret_list = []
    ret_list.append(ask()) 
    
    for i in range(5):
        agent_couples = [ random.sample([agents["Isabella"], agents["Maria"]], 2) ]
        for x in random.sample([agents["Klaus"], agents["Julia"]], 2):
            agent_couples.append(
                random.sample([agents["Maria"], x], 2)
            )
        run(3, agent_couples)    
        ret_list.append(ask())

    df = pd.DataFrame(ret_list)
    df.to_csv(f"{filename}.csv")

def experiment3():

    ret_list = []
    ret_list.append(ask()) 
    
    for i in range(5):
        agent_couples = [ random.sample([agents["Isabella"], agents["Maria"]], 2) ]
        for x, y in random.sample([
                (agents["Maria"], agents["Klaus"]),
                (agents["Maria"], agents["Julia"]),
                (agents["Klaus"], agents["Julia"])
        ], 3):
            agent_couples.append(
                random.sample([x, y], 2)
            )
        run(4, agent_couples)    
        ret_list.append(ask())

    df = pd.DataFrame(ret_list)
    df.to_csv(f"{filename}.csv")

experiment3() 

    
