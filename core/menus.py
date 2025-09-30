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
        "Settings",
        "Exit"
    ]
    question = [
        inq.List("action", message="What would you like to do?", choices=options, carousel=True)
    ]
    answer = inq.prompt(question)["action"]
    return answer

def select_number_of_images() -> int:
    question = [
        inq.List("num_images", message="Images to generate", choices=["4", "8", "12", "16", "20", "24", "28", "32"], carousel=True)
    ]
    answer = inq.prompt(question)["num_images"]
    return int(answer)

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_api_keys():
    bfl_api_key = os.getenv("BFL_API_KEY")
    replicate_api_key = os.getenv("REPLICATE_API_KEY")
    bytedance_api_key = os.getenv("BYTEDANCE_API_KEY")
    if not bfl_api_key and not replicate_api_key and not bytedance_api_key:
        print("Please set at least one API key: BFL_API_KEY, REPLICATE_API_KEY, or BYTEDANCE_API_KEY.")
        print("You can find instructions in the README.md file.")
        time.sleep(5)
        exit(1)


def provider_settings(current_provider: str) -> str:
    """Menu to select the image generation provider."""
    options = [
        ("Black Forest Labs", "BFL"),
        ("Replicate", "REPLICATE"),
        ("Seedream 4 (Replicate)", "SEEDREAM4"),
    ]
    
    # Check if ByteDance API key is available
    if os.getenv("BYTEDANCE_API_KEY"):
        options.append(("Seedream 4 (ByteDance)", "SEEDREAM4_BYTEDANCE"))
    
    question = [
        inq.List(
            "provider",
            message="Select default provider",
            choices=[opt[0] for opt in options],
            carousel=True,
            default=next((opt[0] for opt in options if opt[1] == current_provider), options[0][0]),
        )
    ]
    answer = inq.prompt(question)["provider"]
    for label, value in options:
        if label == answer:
            return value
    return current_provider
