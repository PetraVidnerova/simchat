import random
import json

from chat_interface import get_chat_interface
from utils import extract_json

class Memory():
    def __init__(self, memory_file):
        with open(memory_file, "r") as f:
            self.memory = json.load(f)

        self.other_agents = {}

    def get_random_thoughts(self, number):
        if number < len(self.memory):
            return random.sample(self.memory, number)
        else:
            return self.memory
        
    def add_agent_knowledge(self, name, knowledge):
        if name in self.other_agents:
            self.other_agents[name].append(knowledge)
        else:
            self.other_agents[name] = [knowledge]
        
class Agent():

    def __init__(self, agent_dir):

        with open(f"{agent_dir}/info.json", "r") as f:
            info = json.load(f)

        self.first_name = info["first_name"]
        self.last_name = info["last_name"]
        self.age = info["age"]
        self.sex = info["sex"]
        self.characteristic = info["innate"]
        
        self.memory = Memory(f"{agent_dir}/memory.json")

        self.chat = get_chat_interface()

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def introduce_yourself_det(self):
        intro = f"""{self.name} is  {self.age} years old.
        {self.characteristic}
        """
    
        if self.memory.memory:
            intro += f"""
            {self.name}'s memory:
            """
        
        for m in self.memory.memory:
            intro += m

        return intro
        
    
    def introduce_yourself(self):
        she_he = "She" if self.sex == "F" else "He"
        her_him = "herself" if self.sex == "F" else "himself" 
        prompt = f"""
        Write a short summary that {self.name} would tell about {her_him}. Start with "I am ...".  {she_he} is  {self.age} years old.
        {self.characteristic}
        """
        if self.memory.memory:
            prompt += f"""
            {self.name}'s memory:
            """
        
        for m in self.memory.get_random_thoughts(5):
            prompt += m

        return self.chat.complete(prompt)

    def start_conversation(self, name):

        prompt = self.introduce_yourself()
        
        if name not in self.memory.other_agents:
            partner = f"""
            Imagine, I met {name}, whom I do not know. What I tell them?"""
        else:
            partner = f"""
            Imagine, I met {name}, whom I already know. 
            My knowledge of {name}: {''.join(self.memory.other_agents[name])}
            What I tell them?
            """
        prompt += partner

        prompt += f"""
        Output your answer in JSON, example {{"{self.name}": "<output>"}}
        """

        trial = 3
        while trial:
            answer = self.chat.complete(prompt)
            extracted = extract_json(answer)
            if extracted is not None:
                return extracted
            trial -= 1
            print(" *** new trial *** ")
        else:
            return answer

    def converse(self, name, conversation):

        prompt = self.introduce_yourself()
        prompt += "\n"
        prompt += f"Imagine, I am in the middle of a conversation with {name}. "
        prompt += "Here is the conversation so far:"
        prompt += "\n"
        prompt += f"{conversation}"
        prompt += """
        Generate the next bit of conversaton. Use JSON, example of output {"{self.name}": "<output>"}. 
        Do not include the previous conversation.
        """
        
        trial = 3
        while trial:
            answer = self.chat.complete(prompt)
            extracted = extract_json(answer)
            if extracted is not None:
                return extracted
            trial -= 1
            print(" *** new trial *** ")
        else:
            return answer



    def inquiry(self, question):

        prompt = """You will be given info about a person along with their memory and details.
        """
        prompt += self.introduce_yourself_det()

        #
        #prompt += f"{self.name} memory: \n"
        #for m in self.memory.memory:
        #    prompt += f"{m}\n"

        prompt += "\n"
        prompt += """Answer a question based on this information. """
        
        prompt += question

        print(prompt)
        return self.chat.complete(prompt)
    
        
    # def new_conversation(self, name):
    #     if name not in self.memory.other_agents:            
    #         self.memory.other_agents[name] = []
    #     self.memory.other_agents[name].append("")     
    
    # def start_conversation(self, name):
        
    #     previous_conv = self.memory.other_agents[name][:-1]

    #     if not previous_conv:
        
    #         prompt = f"""
    #         {self.name} is {self.age} years old and is {self.characteristic}. She/he meets
    #         another person. What would she tell?
    #         {self.name} says: 
    #         """

    #     else:
    #         # TODO
    #         NotImplemented
    #         # prompt = f"""
    #         # You are {self.first_name} {self.last_name}, who is {self.age} years old and 
    #         # who is {self.characteristic}, meets {name}. 
    #         # Your previous  conversation with {name}: {"".join(previous_conv)}

    #         # Start conversation with {name}?
    #         # {self.first_name} {self.last_name}: 
    #         # """
            

    #     response = complete(prompt)
    #     self.memory.other_agents[name][-1] += f"{self.name}: {response}\n"
    #     return response
            
    # def answer(self, name, conv):

    #     self.memory.other_agents[name][-1] += f"{name}: {conv}\n"

    #     prompt = f"""
    #         {self.name}  is {self.age} years old and is {self.characteristic}. 
    #         She/he is having a conversation with {name}:  
    #         {self.memory.other_agents[name][-1]}
    
    #         {self.name}:"""

        
    #     response = complete(prompt)

    #     self.memory.other_agents[name][-1] += f"{self.first_name}: {response}\n"
    #     return response

    
    # def finish(self, name, conv):
    #     self.memory.other_agents[name][-1] += f"{name}: {conv}\n"
         
    #     prompt = f"""
    #         {self.name} is {self.age} years old and  is {self.characteristic}. 
    #         She/he is having a conversation with {name} which she wants to finish: 

    #         {self.memory.other_agents[name][-1]} 
            
    #     {self.name}:"""
    #     # print("***********************")
    #     # print(prompt)
    #     # print("**********************************")
        
    #     response = complete(prompt)
    #     self.memory.other_agents[name].append(response)
    #     self.memory.other_agents[name][-1] += f"{self.first_name}: {response}"        
    #     return response
    
    

            
