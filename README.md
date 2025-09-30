# CharacterGen
CharacterGen is a tool designed to generate series of identity-consistent images based on an initial description, using the Black Forest Labs, Replicate, or Google Gemini APIs.

## Example
<p align="center">
  <img src="assets/base.png" alt="Base Image" width="75%"/>
  <br/>
  <em>Original character description</em>
</p>

<p align="center">
   <img src="assets/image_1.png" alt="Generated Image 1" width="40%" style="display: inline-block; margin-right: 10px;"/>
   <img src="assets/image_2.png" alt="Generated Image 2" width="40%" style="display: inline-block;"/>
   <br/>
   <em>Generated consistent character images</em>
</p>

## Features
Under the hood, CharacterGen supports multiple AI providers:
- **Black Forest Labs**: Uses Flux 1.1 Pro Ultra and Flux.1 Kontext for high-quality image generation
- **Replicate**: Alternative access to the same Flux models via Replicate's platform
- **Google Gemini (Nano Banana)**: Uses Gemini for enhanced prompting and image analysis (demo implementation with placeholder images)

All providers create several images while keeping the same character identity. This allows for quick data generation for character LoRA training or other purposes.

> [!NOTE]
> The Google Gemini integration is currently a demonstration implementation. Gemini excels at text generation and image analysis but does not directly generate images. For actual image generation, Google's Imagen API would be required. This implementation shows the integration pattern and uses Gemini for prompt enhancement.

## Usage
First, you need to set up your API keys for at least one provider (Black Forest Labs, Replicate, or Google Gemini). You can do this by copying + renaming the `.env.example` file to `.env` and filling in your API keys.

### Supported Providers:
- **Black Forest Labs**: Direct access to Flux models (requires BFL_API_KEY)
- **Replicate**: Access Flux models via Replicate platform (requires REPLICATE_API_KEY)
- **Google Gemini (Nano Banana)**: Enhanced prompting and image analysis demo (requires GOOGLE_API_KEY)

> [!NOTE]
> The Google Gemini provider is currently a demonstration that shows enhanced prompting capabilities. It generates placeholder images with enhanced descriptions. For production use with Google's image generation, you would need access to Google's Imagen API.

After setting up your API keys, you can run the script to generate images.
You can change the default generation provider at any time from the **Settings**
menu of the application.

**Recommended**: double click the `CharacterGen.bat` file to run the script. This will automatically set up the environment and run the script.
> [!NOTE]
> Sometimes, Windows Defender may flag the script as a potential threat. If this happens, you can safely ignore the warning and allow the script to run.

**Manual**:If you prefer to run the script manually, follow these steps:
1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
   Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
    ```bash
    python main.py
    ```

## Configuration
You can customize the generation process by changing the prompts and variables of the script.
### Prompts
The script uses three different prompts.
- Base Prompt: This is the prompt fed to the model to generate the base image. You can add anything you want to include in the character description.
Template: `prompts/base.md`
> [!NOTE]
> If you add new variables to the base prompt, make sure to add a `.txt` file with the variable name in the `prompts/selectable` directory. This is necessary for the script to recognize the new variable.
- Instruct Prompt: This is the prompt used to generate the secondary images following the base image identity. It is designed to keep the identity of the character while changing the context. Template: `prompts/instruct.md`
> [!NOTE]
> If you add new variables to the instruct prompt, make sure to add a `.txt` file with the variable name in the `prompts/random` directory. This is necessary for the script to recognize the new variable.
- Random Prompt: The same as the instruct prompt, but in a different tone. This is used to "pre-caption" the images, making them more suitable for training. Template: `prompts/random.md`

### Variables
Each variable file has the same structure, with each line representing a different value for the variable. The script will randomly select one of these values when generating the images.

## Contributing
If you want to contribute to CharacterGen, feel free to open a pull request or issue. Contributions are welcome!