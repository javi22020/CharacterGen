from dotenv import load_dotenv
load_dotenv()
from core.title import show_title
from core.menus import (
    clear_screen,
    initial_menu,
    select_feature,
    ensure_api_keys,
    select_number_of_images,
    provider_settings,
)
from core.generate import (
    generate_base_image_bfl,
    edit_base_image_bfl,
    poll_image_bfl,
    generate_base_image_replicate,
    edit_base_image_replicate,
    generate_base_image_google,
    edit_base_image_google,
)
from core.config import *
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
            clear_screen()
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
            if len(feature_options) < n:
                random_feature_options[feature_name] = rn.choices(feature_options, k=n)
            else:
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
    provider = DEFAULT_PROVIDER
    while True:
        clear_screen()
        show_title()
        print(f"Current provider: {provider}")
        action = initial_menu()
        if action == "Create a new character":
            chosen_features = choose_features()
            n = select_number_of_images()
            base_prompt = create_base_prompt(chosen_features)
            random_prompts, instruct_prompts = create_random_prompts(chosen_features, n)
            job_id = chosen_features['character_name'] + "_" + dt.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs(f"outputs/{job_id}/instruct", exist_ok=True)
            print(f"Creating character with ID: {job_id}")
            print("Generating base image...")
            if provider == "BFL":
                base_image_id = generate_base_image_bfl(base_prompt)
                base_image = poll_image_bfl(base_image_id)
            elif provider == "REPLICATE":
                base_image = generate_base_image_replicate(base_prompt)
            else:  # GOOGLE
                base_image = generate_base_image_google(base_prompt)
            base_image.save(f"outputs/{job_id}/base.{IMAGE_FORMAT}")
            with open(f"outputs/{job_id}/base.txt", "w", encoding="utf-8") as f:
                f.write(base_prompt)
            for i, (prompt, instruct_prompt) in enumerate(zip(random_prompts, instruct_prompts)):
                try:
                    if provider == "BFL":
                        i_image_id = edit_base_image_bfl(base_image, instruct_prompt)
                        i_image = poll_image_bfl(i_image_id)
                    elif provider == "REPLICATE":
                        i_image = edit_base_image_replicate(base_image, instruct_prompt)
                    else:  # GOOGLE
                        i_image = edit_base_image_google(base_image, instruct_prompt)
                    i_image.save(f"outputs/{job_id}/{i+1}.{IMAGE_FORMAT}")
                    with open(f"outputs/{job_id}/{i+1}.txt", "w", encoding="utf-8") as f:
                        f.write(prompt)
                    with open(f"outputs/{job_id}/instruct/{i+1}_instruct.txt", "w", encoding="utf-8") as f:
                        f.write(instruct_prompt)
                except Exception as e:
                    print(f"Error generating image {i+1}: {e}")

        elif action == "Settings":
            provider = provider_settings(provider)
        elif action == "Exit":
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()