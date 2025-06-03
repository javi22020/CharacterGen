# CharacterGen
CharacterGen is a tool designed to generate series of identity-consistent images based on an initial description, using the Black Forest Labs or Replicate APIs.

## Example
<p align="center">
  <img src="assets/base.png" alt="Base Image" width="50%"/>
  <br/>
  <em>Original character description</em>
</p>

<p align="center">
  <img src="assets/image_1.png" alt="Generated Image 1" width="50%"/>
  <br/>
  <em>Generated consistent character (image 1)</em>
</p>

<p align="center">
  <img src="assets/image_2.png" alt="Generated Image 2" width="50%"/>
  <br/>
  <em>Generated consistent character (image 2)</em>
</p>

## Features
Under the hood, CharacterGen uses both Flux 1.1 Pro Ultra and Flux.1 Kontext to create several images keeping the same identity. This allows for quick data generation for character LoRA training or other purposes.

## Usage
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