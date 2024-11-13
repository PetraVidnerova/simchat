import logging 
import random
import os

def extract_json(answer):

    # print("RAW")
    # print(answer)
    # print("END-RAW")
    
    start = answer.find(r"```json")
    end = answer[start+7:].find(r"```")

    if start != -1 and end != -1:
        return answer[start+7:end+7]

    start = answer.find("{")
    end = answer.find("}")

    if start != -1 and end != -1:
        return answer[start:end+1]

    return None

    
def random_order(*args):
    elements = list(args)
    random.shuffle(elements)

    return elements

def nice_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return hours, minutes, seconds


def create_logger(name, filename=None, level=None, console_output=True):
    logger = logging.getLogger(name)
    if level is None:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if filename is None:
        experiment_id = os.environ["EXP_ID"]
        filename = f"{experiment_id}.log"
    
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
