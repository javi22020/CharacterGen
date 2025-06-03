# CharacterGen
CharacterGen is a tool designed to generate series of identity-consistent images based on an initial description.

## Example
![base_image](assets/base.png)
![image_1](assets/image_1.png)

## Features
Under the hood, CharacterGen uses both Flux 1.1 Pro Ultra and Flux.1 Kontext to create several images keeping the same identity. This allows for quick data generation for character LoRA training or other purposes.

## Usage
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
    ```bash
    python main.py
    ```