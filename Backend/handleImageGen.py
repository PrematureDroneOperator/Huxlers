import os
from google import genai
from google.genai.types import GenerateImagesConfig

# Path to service account JSON
GOOGLE_SERVICE_ACCOUNT_JSON = "gen-lang-client-0148532417-b3c7b26e5085.json"
PROJECT_ID = "gen-lang-client-0148532417"
LOCATION = "us-central1"  # or your region

def generate_image_with_google(prompt, output_file="output-image.png", image_size="2K"):
    # Create Vertex AI client
    client = genai.Client(api_key="AIzaSyD9Ux3uaGffFHZIRTtKH_N2OmdCZRyoqWo")
    # Generate the image
    image = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=GenerateImagesConfig(
            image_size=image_size
        ),
    )
    # Save first generated image as PNG
    img_obj = image.generated_images[0].image
    img_obj.save(output_file)
    print("done")

