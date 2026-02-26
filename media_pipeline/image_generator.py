import requests
import time
from pathlib import Path

API_KEY = "ojHoO2KnwTFtSCy1H_oOgg"  # public key works but limited

def generate_image(prompt, output_path):
    print("🚀 Sending request to Stable Horde...")

    response = requests.post(
        "https://stablehorde.net/api/v2/generate/async",
        json={
            "prompt": prompt,
            "params": {
                "width": 640,
                "height": 640,
                "steps": 20,
                "cfg_scale": 7
            }
        },
        headers={"apikey": API_KEY}
    )

    request_id = response.json()["id"]

    # Poll until done
    while True:
        status = requests.get(
            f"https://stablehorde.net/api/v2/generate/check/{request_id}"
        ).json()

        if status["done"]:
            break
        time.sleep(3)

    result = requests.get(
        f"https://stablehorde.net/api/v2/generate/status/{request_id}"
    ).json()

    img_url = result["generations"][0]["img"]

    img_data = requests.get(img_url).content
    Path(output_path).write_bytes(img_data)

    print(f"✅ Saved → {output_path}")

if __name__ == "__main__":
    generate_image("Cat with hat", r"D:\Autonomus Youtube Channel\sample.jpg")