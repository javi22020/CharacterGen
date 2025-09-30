import replicate
import requests
import time
import os
from PIL import Image
from io import BytesIO
import base64
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


def generate_base_image_seedream4_replicate(prompt: str) -> Image.Image:
    """Generate a base image using Seedream 4 via Replicate API."""
    client = replicate.Client(api_token=os.environ.get("REPLICATE_API_KEY"))
    output = client.run(
        SEEDREAM4_REPLICATE_MODEL,
        input={
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "max_images": 1
        },
    )
    if isinstance(output, list):
        output = output[0]
    response = requests.get(output)
    return Image.open(BytesIO(response.content))


def edit_base_image_seedream4_replicate(image: Image.Image, instruct_prompt: str) -> Image.Image:
    """Edit an image keeping its identity using Seedream 4 via Replicate API."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG" if IMAGE_FORMAT == "jpg" else "PNG")
    buffered.seek(0)
    client = replicate.Client(api_token=os.environ.get("REPLICATE_API_KEY"))
    output = client.run(
        SEEDREAM4_REPLICATE_MODEL,
        input={
            "prompt": instruct_prompt,
            "image_input": [buffered],
            "aspect_ratio": "match_input_image",
            "max_images": 1
        },
    )
    if isinstance(output, list):
        output = output[0]
    response = requests.get(output)
    return Image.open(BytesIO(response.content))


def generate_base_image_seedream4_bytedance(prompt: str) -> str:
    """Generate a base image using Seedream 4 via ByteDance API."""
    request = requests.post(
        f"{SEEDREAM4_BYTEDANCE_BASE_URL}/api/v1/models/seedream-4/generate",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('BYTEDANCE_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "max_images": 1
        }
    ).json()

    if "id" in request:
        return request["id"]
    else:
        raise ValueError(f"Error in ByteDance API request: {request}")


def edit_base_image_seedream4_bytedance(image: Image.Image, instruct_prompt: str) -> str:
    """Edit an image keeping its identity using Seedream 4 via ByteDance API."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG" if IMAGE_FORMAT == "jpg" else "PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    request = requests.post(
        f"{SEEDREAM4_BYTEDANCE_BASE_URL}/api/v1/models/seedream-4/edit",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('BYTEDANCE_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": instruct_prompt,
            "input_image": img_str,
            "aspect_ratio": "match_input_image",
            "max_images": 1
        }
    ).json()

    if "id" in request:
        return request["id"]
    else:
        raise ValueError(f"Error in ByteDance API request: {request}")


def poll_image_seedream4_bytedance(request_id: str):
    """Poll for image generation result from ByteDance API."""
    i = 0
    while True:
        time.sleep(2.0)
        request_json = requests.get(
            f"{SEEDREAM4_BYTEDANCE_BASE_URL}/api/v1/result/{request_id}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {os.environ.get('BYTEDANCE_API_KEY')}",
            },
        ).json()

        status = request_json.get("status")

        print(f"Waiting for Seedream 4 image {request_id}" + "."*(i % 4) + "    ", end="\r")
        i += 1

        if status == "completed":
            result = request_json.get("result", {})
            image_url = result.get("images", [None])[0]
            if image_url:
                response = requests.get(image_url)
                buffer = BytesIO(response.content)
                print()
                return Image.open(buffer)
            else:
                raise ValueError(f"No image URL in result: {request_json}")
        
        elif status in ["failed", "error"]: 
            raise ValueError(f"ByteDance API error: {request_json}")
        
        elif status not in ["processing", "queued", "pending"]:
            raise ValueError(f"Unknown status from ByteDance API: {request_json}")
