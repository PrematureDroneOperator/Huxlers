import requests
from PIL import Image
from huggingface_hub import InferenceClient

HF_TOKEN = "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"

def generate_image_with_huggingface(prompt, save_path="generated_image.png"):
    client = InferenceClient(
        provider="nebius",
        api_key=HF_TOKEN,
    )

    # Generate image (output is a PIL.Image.Image)
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )
    if isinstance(image, Image.Image):
        image.save(save_path)
        print(f"Image saved as {save_path}")
        return save_path
    else:
        print("Image generation failed.")
        return None

# Example usage
res = generate_image_with_huggingface("orange chubby cat cooking fish kerala cat", "cat.png")
print(f"Hello , path {res} has been forwarded to PORT - 5173 VIA TCP.\nReturn to Render immediately!!!")