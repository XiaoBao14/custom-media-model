#!/usr/bin/env python3
"""
Custom Video Generation Script
Supports any custom video generation API with configurable parameters
"""
import os
import sys
import json
import base64
import httpx
import time
from pathlib import Path

# Load config from environment variables
BASE_URL = os.environ.get("MEDIA_GEN_VIDEO_BASE_URL", "")
API_KEY = os.environ.get("MEDIA_GEN_VIDEO_API_KEY", "")
DEFAULT_MODEL = os.environ.get("MEDIA_GEN_VIDEO_DEFAULT_MODEL", "seeddance-1.5-turbo")
DEFAULT_DURATION = int(os.environ.get("MEDIA_GEN_VIDEO_DEFAULT_DURATION", "5"))
DEFAULT_RESOLUTION = os.environ.get("MEDIA_GEN_VIDEO_DEFAULT_RESOLUTION", "1080p")
AUTH_HEADER = os.environ.get("MEDIA_GEN_VIDEO_AUTH_HEADER", "Bearer")

def generate_video(prompt: str, image_path: str = None, model: str = None, duration: int = None, 
                  resolution: str = None, output_path: str = None) -> str:
    """Generate video from text prompt or image"""
    
    if not BASE_URL or not API_KEY:
        print("ERROR: MEDIA_GEN_VIDEO_BASE_URL and MEDIA_GEN_VIDEO_API_KEY must be set", file=sys.stderr)
        sys.exit(1)
    
    model = model or DEFAULT_MODEL
    duration = duration or DEFAULT_DURATION
    resolution = resolution or DEFAULT_RESOLUTION
    
    # Build headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{AUTH_HEADER} {API_KEY}" if AUTH_HEADER else API_KEY,
    }
    
    # Build payload
    payload = {
        "model": model,
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution,
        "fps": 30,
        "response_format": "b64_json"
    }
    
    # Add image if provided (image to video)
    if image_path and Path(image_path).exists():
        with open(image_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        payload["image"] = img_base64
        print(f"Using input image: {image_path}", file=sys.stderr)
    
    print(f"Generating video with model: {model}", file=sys.stderr)
    print(f"Prompt: {prompt[:100]}...", file=sys.stderr)
    print(f"Duration: {duration}s, Resolution: {resolution}", file=sys.stderr)
    
    try:
        with httpx.Client(timeout=300.0) as client:
            # Submit task
            response = client.post(BASE_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
    except Exception as e:
        print(f"ERROR: API call failed: {e}", file=sys.stderr)
        if 'response' in locals():
            print(f"Response status: {response.status_code}", file=sys.stderr)
            print(f"Response content: {response.text}", file=sys.stderr)
        sys.exit(1)
    
    # Handle async task polling (common for video generation)
    task_id = None
    if "task_id" in result or "id" in result:
        task_id = result.get("task_id") or result.get("id")
        print(f"Task submitted, ID: {task_id}", file=sys.stderr)
        
        # Poll for result
        poll_url = f"{BASE_URL.rsplit('/', 1)[0]}/tasks/{task_id}" if "/" in BASE_URL else f"{BASE_URL}/tasks/{task_id}"
        while True:
            time.sleep(3)
            try:
                poll_resp = client.get(poll_url, headers=headers)
                poll_resp.raise_for_status()
                poll_result = poll_resp.json()
                
                status = poll_result.get("status", "").lower()
                if status in ["completed", "success", "done"]:
                    result = poll_result
                    break
                elif status in ["failed", "error"]:
                    error_msg = poll_result.get("error", "Unknown error")
                    print(f"Task failed: {error_msg}", file=sys.stderr)
                    sys.exit(1)
                else:
                    progress = poll_result.get("progress", 0)
                    print(f"Task in progress: {progress}%", file=sys.stderr)
            except Exception as e:
                print(f"Poll error: {e}, retrying...", file=sys.stderr)
    
    # Extract video from response
    video_data = None
    
    # Standard formats
    if "data" in result and len(result["data"]) > 0:
        if "b64_json" in result["data"][0]:
            video_data = result["data"][0]["b64_json"]
        elif "url" in result["data"][0]:
            video_url = result["data"][0]["url"]
            print(f"Downloading video from URL: {video_url}", file=sys.stderr)
            video_resp = httpx.get(video_url, timeout=120)
            video_resp.raise_for_status()
            video_data = base64.b64encode(video_resp.content).decode()
    elif "video" in result:
        video_data = result["video"]
    elif "base64" in result:
        video_data = result["base64"]
    elif "b64" in result:
        video_data = result["b64"]
    elif "video_url" in result:
        video_url = result["video_url"]
        print(f"Downloading video from URL: {video_url}", file=sys.stderr)
        video_resp = httpx.get(video_url, timeout=120)
        video_resp.raise_for_status()
        video_data = base64.b64encode(video_resp.content).decode()
    
    if not video_data:
        print(f"No video found in response. Full response: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)
    
    # Decode and save video
    try:
        video_bytes = base64.b64decode(video_data)
    except:
        video_bytes = video_data
    
    ext = "mp4"
    
    if output_path:
        out_file = Path(output_path)
    else:
        out_file = Path.cwd() / f"generated_video_{int(os.times()[4])}.{ext}"
    
    out_file.write_bytes(video_bytes)
    print(f"✅ Video saved to: {out_file}", file=sys.stderr)
    print(f"ℹ️ Duration: {duration}s, Size: {len(video_bytes)/1024/1024:.2f}MB", file=sys.stderr)
    
    print(str(out_file))
    return str(out_file)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate video with custom API")
    parser.add_argument("prompt", help="Text prompt for video generation")
    parser.add_argument("--image", "-i", help="Input image path for image to video")
    parser.add_argument("--model", "-m", help="Model to use")
    parser.add_argument("--duration", "-d", type=int, help="Video duration in seconds")
    parser.add_argument("--resolution", "-r", help="Video resolution (e.g. 1080p, 720p, 4k)")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()
    
    generate_video(args.prompt, args.image, args.model, args.duration, args.resolution, args.output)
