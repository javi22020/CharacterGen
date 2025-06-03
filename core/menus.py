import inquirer as inq
import os
from typing import List
import time

def select_feature(message: str, feature_options: List[str]) -> str:
    question = [
        inq.List("feature", message=message, choices=feature_options, carousel=True)
    ]
    answer = inq.prompt(question)["feature"]
    return answer

def initial_menu() -> str:
    options = [
        "Create a new character",
        "Exit"
    ]
    question = [
        inq.List("action", message="What would you like to do?", choices=options, carousel=True)
    ]
    answer = inq.prompt(question)["action"]
    return answer

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_api_keys():
    bfl_api_key = os.getenv("BFL_API_KEY")
    replicate_api_key = os.getenv("REPLICATE_API_KEY")
    if not bfl_api_key and not replicate_api_key:
        print("Please set your BFL_API_KEY and REPLICATE_API_KEY environment variables.")
        print("You can find instructions in the README.md file.")
        time.sleep(5)
        exit(1)