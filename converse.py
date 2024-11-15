
import numpy as np

from chat_interface import get_chat_interface

THETA = 0.23


class ConversationModule():

    def __init__(self,
                 ending_phrases=["See you later.", "Good bye!"],
                 theta=THETA):
        self.theta = theta
        self.chat = get_chat_interface()
        self.ending_phrases = list(
            map(self.chat.get_embedding, ending_phrases))

    def generate_conversation(self, agent1, agent2):

        prompt = ""
        prompt += agent1.introduce_yourself()
        prompt += "\n"
        prompt += agent2.introduce_yourself()
        
        prompt += f"""
        Generate conversation between {agent1.name} and
        {agent2.name}. 
        Output format:
        {agent1.name.upper()}: [FILL IN]
        {agent2.name.upper()}: [FILL IN]
        {agent1.name.upper()}: [FILL IN]
        {agent2.name.upper()}: [FILL IN]
        ...
        """ 
        #    prompt += f"{agent1.name.upper()}: "
    
    
        return self.chat.complete(prompt) 

    def _clean_fact(self, fact):
        fact = fact.strip()
        while fact and fact[0] in "0123456789.":
            fact = fact[1:]
        return fact 
        
    def summary_message(self, conversation, agent_name):
        prompt = f"""Summarize into a short fact what {agent_name} said: 
        {conversation}. Use one sentence, be brief.
        """
        return self.chat.complete(prompt)

    def summary(self, conversation, agent):

        prompt = f"""List three short facts that {agent.name}  
        has learnt from this conversation: {conversation}.
        """
        facts =  self.chat.complete(prompt)
        facts = facts.split("\n")
        facts = [self._clean_fact(fact) for fact in facts]
        facts = [fact for fact in facts if fact and len(fact)>0]
        return facts

    def partner_knowledge(self, conversation, agent):
        prompt = f"""Here is a dialogue: 
        {conversation}
        Write one fact about {agent.name.upper()}:"""

        return self.chat.complete(prompt)
    
    def _distance(self, a, b):
        """ cosine similarity """ 
        return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

    def is_ending(self, conv):
    
        last_sentence = conv.split(".")[-1]
        
        emb = self.chat.get_embedding(last_sentence)
        
        dist = max([
            self._distance(emb, x)
            for x in self.ending_phrases
        ])
        print(dist)        
        
        if dist > self.chat.theta:
            return True
        else:
            return False

    
    def answer_to_bool(self, answer):
        if "*YES*" in answer and "*NO*" not in answer:
            return True
        if "*NO*" in answer and "*YES*" not in answer:
            return False
        if answer.strip()[:3].upper() == "YES":
            return True
        if answer.strip()[:2].upper() == "NO":
            return False
        return None
