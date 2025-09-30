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
    """Generate a base image using Google Gemini for enhanced prompting.
    
    Note: This is a conceptual implementation. Google's Gemini is primarily a text model.
    For actual image generation, you would need access to Google's Imagen API.
    This implementation demonstrates the integration pattern and generates placeholder images.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    genai.configure(api_key=api_key)
    
    try:
        # Use Gemini to enhance the prompt
        model = genai.GenerativeModel(GOOGLE_IMAGE_MODEL)
        
        enhancement_prompt = f"""
        Enhance this image generation prompt to be more detailed and specific:
        "{prompt}"
        
        Provide a detailed, vivid description that would help an image generation AI create a high-quality, detailed image.
        Focus on visual details, style, composition, and character features.
        """
        
        response = model.generate_content(enhancement_prompt)
        enhanced_prompt = response.text
        
        print(f"Enhanced prompt: {enhanced_prompt[:100]}...")
        
        # In a real implementation, this enhanced prompt would be sent to Imagen API
        # For now, we'll create a placeholder image with text indicating it's a demo
        
        # Create a placeholder image
        img = Image.new('RGB', (1024, 1024), color='#f0f0f0')
        
        # Add text to indicate this is a demo
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            # Try to use a default font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Add demo text
            demo_text = "Google Gemini Demo\n(Placeholder Image)\n\nEnhanced Prompt:\n" + enhanced_prompt[:200] + "..."
            
            # Center the text
            lines = demo_text.split('\n')
            y_start = 100
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (1024 - text_width) // 2
                y = y_start + i * 30
                draw.text((x, y), line, fill='black', font=font)
                
        except Exception as e:
            print(f"Could not add text to placeholder: {e}")
        
        return img
        
    except Exception as e:
        print(f"Google Gemini API call failed: {e}")
        
        # Create a simple error placeholder
        img = Image.new('RGB', (1024, 1024), color='lightcoral')
        
        try:
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            draw.text((50, 500), f"Google API Error: {str(e)[:100]}", fill='white')
        except:
            pass
            
        return img


def edit_base_image_google(image: Image.Image, instruct_prompt: str) -> Image.Image:
    """Edit an image using Google Gemini for enhanced prompting.
    
    Note: This is a conceptual implementation. Google's Gemini can analyze images and generate
    enhanced prompts, but doesn't directly edit images. For actual image editing, you would 
    need access to Google's Imagen API or other image editing models.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    genai.configure(api_key=api_key)
    
    # Convert image to base64 for analysis
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    
    try:
        # Use Gemini to analyze the image and create an enhanced prompt
        model = genai.GenerativeModel(GOOGLE_EDIT_MODEL)
        
        analysis_prompt = f"""
        Analyze this image and create a detailed prompt for generating a similar image with these modifications: {instruct_prompt}
        
        Describe the current image in detail, then specify how to modify it while maintaining character consistency.
        Focus on preserving the character's key features while applying the requested changes.
        """
        
        response = model.generate_content([
            analysis_prompt,
            {
                "mime_type": "image/png",
                "data": img_b64
            }
        ])
        
        enhanced_edit_prompt = response.text
        print(f"Enhanced edit prompt: {enhanced_edit_prompt[:100]}...")
        
        # In a real implementation, this would be sent to an image editing API
        # For now, create a modified placeholder image
        
        # Create a slightly different placeholder to show "editing"
        img = Image.new('RGB', (1024, 1024), color='#e8f4f8')
        
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            demo_text = "Google Gemini Demo\n(Edited Placeholder)\n\nEdit Instruction:\n" + instruct_prompt + "\n\nAnalysis Result:\n" + enhanced_edit_prompt[:150] + "..."
            
            lines = demo_text.split('\n')
            y_start = 80
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (1024 - text_width) // 2
                y = y_start + i * 25
                draw.text((x, y), line, fill='darkblue', font=font)
                
        except Exception as e:
            print(f"Could not add text to placeholder: {e}")
        
        return img
        
    except Exception as e:
        print(f"Image editing with Gemini failed: {e}")
        
        # Fallback: create a simple modified placeholder
        img = Image.new('RGB', (1024, 1024), color='lightsteelblue')
        
        try:
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            draw.text((50, 500), f"Edit: {instruct_prompt[:100]}", fill='darkblue')
            draw.text((50, 530), f"Error: {str(e)[:100]}", fill='red')
        except:
            pass
            
        return img
