import asyncio
from random import randint
from PIL import Image
import requests
import base64
from dotenv import get_key
import os
from time import sleep
import subprocess

os.makedirs("Data", exist_ok=True)

def open_image(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        if os.path.exists(image_path):
            print(f"Opening image: {image_path}")
            subprocess.run(["open", image_path])  
            sleep(1)
        else:
            print(f"Unable to open {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# === Send request and decode base64 image ===
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)

    try:
        response.raise_for_status()
        response_json = response.json()

        if isinstance(response_json, list) and "generated_image" in response_json[0]:
            return base64.b64decode(response_json[0]["generated_image"])
        else:
            print("Unexpected response:", response_json)
            return None
    except Exception as e:
        print("API error:", e)
        print("Raw response:", response.text)
        return None

async def generate_image(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0,1000000)}"
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            filename = os.path.join("Data", f"{prompt.replace(' ', '_')}{i+1}.jpg")
            with open(filename, "wb") as f:
                f.write(image_bytes)
        else:
            print(f"Image {i+1} could not be generated.")

def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_image(prompt)
data_file_path = os.path.join("Frontend", "Files", "ImageGeneration.data")

while True:
    try:
        if not os.path.exists(data_file_path):
            sleep(1)
            continue

        with open(data_file_path, "r") as f:
            data = f.read().strip()

        if not data:
            sleep(1)
            continue

        Prompt, Status = map(str.strip, data.split(","))

        if Status == "True":
            print(f"Generating images....")
            GenerateImages(prompt=Prompt)

            with open(data_file_path, "w") as f:
                f.write(f"{Prompt}, False")
        else:
            sleep(1)
    except Exception as e:
        print("Error in main loop:", e)
        sleep(1)
