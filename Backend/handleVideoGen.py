import os
from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import base64
import time

app = FastAPI()

GOOGLE_APPLICATION_CREDENTIALS = "add-your-security.json"

class RequestBody:
    def __init__(self, prompt, image_path):
        self.prompt = prompt
        self.image_path = image_path

def get_access_token():
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_APPLICATION_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    creds.refresh(Request())
    return creds.token

import base64
import time
import requests

def poll_veo_operation(operation_name, access_token, max_attempts=20, poll_interval=30, output_file="output.mp4"):
    endpoint = (
        "https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT-ID/locations/us-central1/publishers/google/models/veo-3.0-generate-preview:fetchPredictOperation"
    )

    payload = {
        "operationName": operation_name
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }

    for attempt in range(max_attempts):
        try:
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            print(f"[Attempt {attempt+1}] HTTP {resp.status_code}")
            if resp.status_code != 200:
                print("Error:", resp.text)
                if resp.status_code in (401, 403):
                    return {"error": "Authentication failed or permission denied.", "details": resp.text}
                elif resp.status_code == 429:
                    print("Quota exceeded, doubling interval.")
                    time.sleep(poll_interval * 2)
                else:
                    time.sleep(poll_interval)
                continue

            result = resp.json()
            if "error" in result:
                print("API error:", result["error"])
                return {"error": result["error"]}

            # print("Operation response:", result)
            # Check for nested done
            if result.get("done") or ("response" in result and result["response"].get("done")):
                # Drill down to "videos"
                response_obj = None
                if "response" in result and isinstance(result["response"], dict):
                    # Sometimes nested: result["response"]["response"]
                    if "response" in result["response"]:
                        response_obj = result["response"]["response"]
                    else:
                        response_obj = result["response"]
                else:
                    response_obj = result  # fallback

                if response_obj and "videos" in response_obj and response_obj["videos"]:
                    video_obj = response_obj["videos"][0]  # Always first video
                    # Check for GCS
                    if "gcsUri" in video_obj and video_obj["gcsUri"].startswith("gs://"):
                        print("Video available at:", video_obj["gcsUri"])
                        return {"done": True, "gcsUri": video_obj["gcsUri"], "mimeType": video_obj.get("mimeType", "video/mp4")}
                    # Check for base64 video
                    elif "bytesBase64Encoded" in video_obj:
                        print("Base64 video found, writing to:", output_file)
                        with open(output_file, "wb") as f:
                            f.write(base64.b64decode(video_obj["bytesBase64Encoded"]))
                        print("Saved video to:", output_file)
                        return {"done": True, "file": output_file, "mimeType": video_obj.get("mimeType", "video/mp4")}
                    else:
                        print("Video object does not contain usable fields.", video_obj)
                        return {"done": True, "error": "No gcsUri or base64 in video object.", "video_obj": video_obj}
                else:
                    print("Videos list is empty or missing.")
                    return {"done": True, "error": "No videos returned", "response": response_obj}
            else:
                print("Operation still running...")
                time.sleep(poll_interval)
        except requests.RequestException as e:
            print("Network/request error:", e)
            time.sleep(poll_interval)
        except Exception as e:
            print("Unexpected error:", e)
            time.sleep(poll_interval)

    print("Finished polling after max attempts, operation may still be running.")
    return {"done": False, "error": "Polling stopped, max attempts reached."}


def generate_content(prompt, image_path, output_file="output.mp4"):
    try:
        print(">>> Authenticating with service account...", flush=True)
        access_token = get_access_token()

        # Load image as base64
        if not os.path.exists(image_path):
            print("Image not found:", image_path, flush=True)
            return {"error": "Image file not found"}

        with open(image_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Model endpoint (Veo with image + text support)
        endpoint = "https://aiplatform.googleapis.com/v1/projects/PROJECT-ID/locations/us-central1/publishers/google/models/veo-3.0-generate-preview:predictLongRunning"

        payload = {
            "instances": [
                {
                    "prompt": prompt,
                    "input_image": {
                        "mimeType": "image/jpeg",  # Change to "image/png" if your file is PNG
                        "bytesBase64Encoded": img_b64
                    }
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, headers=headers, json=payload)
        print(">>> GOOGLE API STATUS:", response.status_code, flush=True)
        print(">>> GOOGLE API RAW RESPONSE:", response.text, flush=True)

        if response.status_code != 200:
            return {"error": response.text}

        operation_name = response.json()["name"].strip()
        poll_result = poll_veo_operation(operation_name, access_token, output_file=output_file)
        print(">>> POLL RESULT:", poll_result, flush=True)

        # Check for video URIs or base64 video results
        if isinstance(poll_result, dict) and "response" in poll_result:
            response_obj = poll_result["response"]
            # Handle response schema with nested videos
            if (
                isinstance(response_obj, dict)
                and "response" in response_obj
                and "videos" in response_obj["response"]
            ):
                videos = response_obj["response"]["videos"]
                if videos and "gcsUri" in videos[0]:
                    return {"output_uri": videos[0]["gcsUri"]}
                elif videos and "bytesBase64Encoded" in videos[0]:
                    base64_video = videos[0]["bytesBase64Encoded"]
                    with open(output_file, "wb") as f:
                        f.write(base64.b64decode(base64_video))
                    print(f">>> Saved {output_file}", flush=True)
                    return {"file": output_file}
        # Fallback for flat schema
        elif "bytesBase64Encoded" in poll_result:
            base64_video = poll_result["bytesBase64Encoded"]
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(base64_video))
            print(f">>> Saved {output_file}", flush=True)
            return {"file": output_file}

        return poll_result

    except Exception as e:
        print(">>> EXCEPTION:", e, flush=True)
        return {"error": str(e)}
import base64

def save_base64_video_from_poll(poll_result, filename="output.mp4"):
    """
    Save video from base64 in poll_result['response']['videos'][0]['data'] to a file.
    """
    try:
        if (
            "response" in poll_result
            and "videos" in poll_result["response"]
            and len(poll_result["response"]["videos"]) > 0
            and "data" in poll_result["response"]["videos"][0]
        ):
            base64_video = poll_result["response"]["videos"][0]["data"]
            with open(filename, "wb") as f:
                f.write(base64.b64decode(base64_video))
            print(f"Saved video to {filename}")
            return {"file": filename}
        else:
            print("No video data found in API response.")
            return {"error": "No base64 video found in poll_result"}
    except Exception as e:
        print("Error saving video:", e)
        return {"error": str(e)}
    