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
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not bfl_api_key and not replicate_api_key and not google_api_key:
        print("Please set at least one of the following API keys:")
        print("- BFL_API_KEY (Black Forest Labs)")
        print("- REPLICATE_API_KEY (Replicate)")
        print("- GOOGLE_API_KEY (Google Gemini)")
        print("You can find instructions in the README.md file.")
        time.sleep(5)
        exit(1)


def provider_settings(current_provider: str) -> str:
    """Menu to select the image generation provider."""
    options = [
        ("Black Forest Labs", "BFL"),
        ("Replicate", "REPLICATE"),
        ("Google Gemini (Nano Banana)", "GOOGLE"),
    ]
    question = [
        inq.List(
            "provider",
            message="Select default provider",
            choices=[opt[0] for opt in options],
            carousel=True,
            default="Black Forest Labs" if current_provider == "BFL" 
                   else "Replicate" if current_provider == "REPLICATE"
                   else "Google Gemini (Nano Banana)",
        )
    ]
    answer = inq.prompt(question)["provider"]
    for label, value in options:
        if label == answer:
            return value
    return current_provider
