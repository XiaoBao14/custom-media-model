#!/usr/bin/env python3
"""
Custom Image Generation Script
Supports any custom API with configurable parameters
"""
import os
import sys
import json
import base64
import httpx
from pathlib import Path

# Load config from environment variables
BASE_URL = os.environ.get("MEDIA_GEN_IMAGE_BASE_URL", "")
API_KEY = os.environ.get("MEDIA_GEN_IMAGE_API_KEY", "")
DEFAULT_MODEL = os.environ.get("MEDIA_GEN_IMAGE_DEFAULT_MODEL", None)
DEFAULT_SIZE = os.environ.get("MEDIA_GEN_IMAGE_DEFAULT_SIZE", "1024x1024")
AUTH_HEADER = os.environ.get("MEDIA_GEN_IMAGE_AUTH_HEADER", "Bearer")

def generate_image(prompt: str, model: str = None, size: str = None, output_path: str = None) -> str:
    """Generate image from text prompt"""
    
    if not BASE_URL or not API_KEY:
        print("ERROR: MEDIA_GEN_IMAGE_BASE_URL and MEDIA_GEN_IMAGE_API_KEY must be set", file=sys.stderr)
        sys.exit(1)
    
    model = model or DEFAULT_MODEL
    if not model:
        print("ERROR: No model specified! Please either:", file=sys.stderr)
        print("  1. Set MEDIA_GEN_IMAGE_DEFAULT_MODEL environment variable (recommended for frequent use)", file=sys.stderr)
        print("  2. Pass --model <model-name> parameter when calling the script", file=sys.stderr)
        sys.exit(1)
    
    size = size or DEFAULT_SIZE
    
    # Parse size to width/height
    if "x" in size:
        width, height = map(int, size.split("x"))
    else:
        width, height = 1024, 1024
    
    # Build headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{AUTH_HEADER} {API_KEY}" if AUTH_HEADER else API_KEY,
    }
    
    # Build payload (compatible with most OpenAI-style APIs)
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "width": width,
        "height": height,
        "response_format": "b64_json"
    }
    
    print(f"Generating image with model: {model}", file=sys.stderr)
    print(f"Prompt: {prompt[:100]}...", file=sys.stderr)
    print(f"Size: {size}", file=sys.stderr)
    
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(BASE_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
    except Exception as e:
        print(f"ERROR: API call failed: {e}", file=sys.stderr)
        if 'response' in locals():
            print(f"Response status: {response.status_code}", file=sys.stderr)
            print(f"Response content: {response.text}", file=sys.stderr)
        sys.exit(1)
    
    # Extract image from response (support multiple formats)
    image_data = None
    
    # OpenAI format
    if "data" in result and len(result["data"]) > 0:
        if "b64_json" in result["data"][0]:
            image_data = result["data"][0]["b64_json"]
        elif "url" in result["data"][0]:
            # If URL is returned, download it
            img_url = result["data"][0]["url"]
            print(f"Downloading image from URL: {img_url}", file=sys.stderr)
            img_resp = httpx.get(img_url, timeout=30)
            img_resp.raise_for_status()
            image_data = base64.b64encode(img_resp.content).decode()
    
    # Direct base64 return
    elif "image" in result:
        image_data = result["image"]
    elif "base64" in result:
        image_data = result["base64"]
    elif "b64" in result:
        image_data = result["b64"]
    
    if not image_data:
        print(f"No image found in response. Full response: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)
    
    # Decode and save image
    try:
        img_bytes = base64.b64decode(image_data)
    except:
        # If already bytes
        img_bytes = image_data
    
    ext = "png"
    
    if output_path:
        out_file = Path(output_path)
    else:
        out_file = Path.cwd() / f"generated_image_{int(os.times()[4])}.{ext}"
    
    out_file.write_bytes(img_bytes)
    print(f"✅ Image saved to: {out_file}", file=sys.stderr)
    
    print(str(out_file))
    return str(out_file)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate image with custom API")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--model", "-m", help="Model to use")
    parser.add_argument("--size", "-s", help="Image size (e.g. 1024x1024, 1792x1024)")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()
    
    generate_image(args.prompt, args.model, args.size, args.output)
