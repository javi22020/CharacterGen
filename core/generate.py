import replicate
import requests
import time
import os
from PIL import Image
from io import BytesIO
import base64
import google.generativeai as genai
from core.config import *

def poll_image_bfl(request_id: str):
    i = 0
    while True:
        time.sleep(1.5)
        request_json = requests.get(
            "https://api.bfl.ai/v1/get_result",
            headers={
                "accept": "application/json",
                "x-key": os.environ.get("BFL_API_KEY"),
            },
            params={"id": request_id},
        ).json()

        status = request_json.get("status")

        print(f"Waiting for image {request_id}" + "."*(i % 4) + "    ", end="\r")
        i += 1

        if status == "Ready":
            result = request_json.get("result", {})
            image_url = result.get("sample")
            response = requests.get(image_url)
            buffer = BytesIO(response.content)
            print()
            return Image.open(buffer)
        
        elif status not in ["Processing", "Queued", "Pending"]: 
            raise ValueError(f"An error or unexpected status occurred: {request_json}")

def generate_base_image_bfl(prompt: str) -> str:
    request = requests.post(
        f"https://api.bfl.ai/v1/{BFL_BASE_MODEL}",
        headers={
            "accept": "application/json",
            "x-key": os.environ.get("BFL_API_KEY"),
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "aspect_ratio": "1:1"
        }
    ).json()

    request_id = request["id"]
    return request_id

def edit_base_image_bfl(image: Image.Image, instruct_prompt: str) -> str:
    buffered = BytesIO()
    image.save(buffered, format="JPEG" if IMAGE_FORMAT == "jpg" else "PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    request = requests.post(
        f"https://api.bfl.ai/v1/{BFL_EDIT_MODEL}",
        headers={
            "accept": "application/json",
            "x-key": os.environ.get("BFL_API_KEY"),
            "Content-Type": "application/json",
        },
        json={
            "prompt": instruct_prompt,
            "input_image": img_str,
        }
    ).json()

    request_id = request["id"]
    return request_id


def generate_base_image_replicate(prompt: str) -> Image.Image:
    """Generate a base image using the Replicate API."""
    client = replicate.Client(api_token=os.environ.get("REPLICATE_API_KEY"))
    output = client.run(
        REPLICATE_BASE_MODEL,
        input={"prompt": prompt, "aspect_ratio": "1:1"},
    )
    if isinstance(output, list):
        output = output[0]
    response = requests.get(output)
    return Image.open(BytesIO(response.content))


def edit_base_image_replicate(image: Image.Image, instruct_prompt: str) -> Image.Image:
    """Edit an image keeping its identity using the Replicate API."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG" if IMAGE_FORMAT == "jpg" else "PNG")
    buffered.seek(0)
    client = replicate.Client(api_token=os.environ.get("REPLICATE_API_KEY"))
    output = client.run(
        REPLICATE_EDIT_MODEL,
        input={"prompt": instruct_prompt, "input_image": buffered},
    )
    if isinstance(output, list):
        output = output[0]
    response = requests.get(output)
    return Image.open(BytesIO(response.content))


def generate_base_image_google(prompt: str) -> Image.Image:
    """Generate a base image using the Google Gemini API (Nano Banana)."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    try:
        model = genai.GenerativeModel(GOOGLE_IMAGE_MODEL)
        response = model.generate_content(
            [prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="image/png"
            )
        )
        
        # Convert response to image
        image_data = response.parts[0].inline_data.data
        image_bytes = base64.b64decode(image_data)
        return Image.open(BytesIO(image_bytes))
    except Exception as e:
        # Fallback method using direct API call if the above doesn't work
        try:
            import google.auth
            from google.auth.transport.requests import Request
            import json
            
            # Get credentials
            credentials, project = google.auth.default()
            credentials.refresh(Request())
            
            # Make direct API call
            headers = {
                'Authorization': f'Bearer {credentials.token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'prompt': prompt,
                'aspect_ratio': '1:1',
                'output_format': 'png'
            }
            
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1/models/{GOOGLE_IMAGE_MODEL}:generateContent',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                image_data = result['candidates'][0]['content']['parts'][0]['inline_data']['data']
                image_bytes = base64.b64decode(image_data)
                return Image.open(BytesIO(image_bytes))
            else:
                raise Exception(f"Google API error: {response.status_code} - {response.text}")
        except Exception as e2:
            raise Exception(f"Failed to generate image with Google API: {str(e)} / {str(e2)}")


def edit_base_image_google(image: Image.Image, instruct_prompt: str) -> Image.Image:
    """Edit an image keeping its identity using the Google Gemini API (Nano Banana)."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    
    try:
        model = genai.GenerativeModel(GOOGLE_EDIT_MODEL)
        
        # Create prompt for image editing
        edit_prompt = f"Edit this image: {instruct_prompt}. Keep the character's identity and main features consistent."
        
        response = model.generate_content(
            [
                edit_prompt,
                {
                    "mime_type": "image/png",
                    "data": img_b64
                }
            ],
            generation_config=genai.GenerationConfig(
                response_mime_type="image/png"
            )
        )
        
        # Convert response to image
        image_data = response.parts[0].inline_data.data
        image_bytes = base64.b64decode(image_data)
        return Image.open(BytesIO(image_bytes))
        
    except Exception as e:
        # Fallback: if image editing fails, generate a new image with context
        print(f"Image editing failed, generating new image with context: {e}")
        context_prompt = f"{instruct_prompt}. Character should look similar to the provided reference image."
        return generate_base_image_google(context_prompt)
