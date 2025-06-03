from dotenv import load_dotenv
load_dotenv()
from core.title import show_title
from core.menus import (
    clear_screen,
    initial_menu,
    select_feature,
    ensure_api_keys
)
from core.generate import (
    generate_base_image_bfl,
    edit_base_image_bfl,
    poll_image_bfl
)
from typing import Dict
from datetime import datetime as dt
import random as rn
import os

def choose_features():
    chosen_features = {}
    for filename in sorted(os.listdir("features/selectable")):
        if filename.endswith(".txt"):
            feature_name = filename.removesuffix(".txt")
            feature_options = open(f"features/selectable/{filename}").read().splitlines()
            chosen_feature = select_feature(feature_name.replace('_', ' ').capitalize(), feature_options)
            chosen_features[feature_name] = chosen_feature
    return chosen_features

def create_base_prompt(chosen_features):
    base_prompt = open("prompts/base.md", "r", encoding="utf-8").read()
    formatted_base_prompt = base_prompt.format(**chosen_features)
    return formatted_base_prompt

def create_random_prompts(chosen_features: Dict[str, str], n: int = 15):
    random_prompt = open("prompts/random.md", "r", encoding="utf-8").read()
    instruct_prompt = open("prompts/instruct.md", "r", encoding="utf-8").read()
    random_feature_options = {}
    for filename in sorted(os.listdir("features/random")):
        if filename.endswith(".txt"):
            feature_name = filename.removesuffix(".txt")
            feature_options = open(f"features/random/{filename}").read().splitlines()
            random_feature_options[feature_name] = rn.sample(feature_options, k=n)
    random_prompts = []
    instruct_prompts = []
    for i in range(n):
        all_features = {**chosen_features, **{feature: options[i] for feature, options in random_feature_options.items()}}
        formatted_random_prompt = random_prompt.format(
            **all_features
        )
        formatted_instruct_prompt = instruct_prompt.format(
            **all_features
        )
        random_prompts.append(formatted_random_prompt)
        instruct_prompts.append(formatted_instruct_prompt)
    return random_prompts, instruct_prompts

def main():
    ensure_api_keys()
    while True:
        clear_screen()
        show_title()
        action = initial_menu()
        if action == "Create a new character":
            chosen_features = choose_features()
            base_prompt = create_base_prompt(chosen_features)
            random_prompts, instruct_prompts = create_random_prompts(chosen_features)
            job_id = chosen_features['character_name'] + "_" + dt.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs(f"outputs/{job_id}/instruct", exist_ok=True)
            print(f"Creating character with ID: {job_id}")
            print("Generating base image...")
            base_image_id = generate_base_image_bfl(base_prompt)
            base_image = poll_image_bfl(base_image_id)
            with open(f"outputs/{job_id}/base.txt", "w", encoding="utf-8") as f:
                f.write(base_prompt)
            for i, (prompt, instruct_prompt) in enumerate(zip(random_prompts, instruct_prompts)):
                i_image_id = edit_base_image_bfl(base_image, instruct_prompt)
                i_image = poll_image_bfl(i_image_id)
                i_image.save(f"outputs/{job_id}/{i+1}.jpg")
                with open(f"outputs/{job_id}/{i+1}.txt", "w", encoding="utf-8") as f:
                    f.write(prompt)
                with open(f"outputs/{job_id}/instruct/{i+1}_instruct.txt", "w", encoding="utf-8") as f:
                    f.write(instruct_prompt)
            print(f"Character creation completed. All files saved in outputs/{job_id}/")
            input("Press Enter to return to the main menu...")

        elif action == "Exit":
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()